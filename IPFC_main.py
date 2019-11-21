#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import random
import secrets
import shutil
import sys
import time
import uuid
from pathlib import Path

import argon2
import requests
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QDialog, QApplication

# Import the UI files, made with QtDesigner
from IPFC_Deck_menu import *
from IPFC_Import import *
from IPFC_Import_options import *
from IPFC_Login import *
from IPFC_Multi_choice import *
from IPFC_Quiz_choose import *
from IPFC_Signup import *
from IPFC_Start_menu import *

program_directory = Path.cwd()
api_url = "https://ipfc-midware.herokuapp.com/"
pinata_json_url = 'https://api.pinata.cloud/pinning/pinJSONToIPFS'
pinata_file_url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
pinata_get_pinned_url = 'https://api.pinata.cloud/data/pinList?status=pinned'
pinata_api_key = ""
pinata_secret_key = ""
user_id = ""
decks_paths = []
decks_stems = []
to_convert_paths = []
to_convert_stems = []

def refresh_decks_and_files_lists():
    to_convert_dir = program_directory / 'users' / user_id / 'to_convert/'
    if not os.path.exists(to_convert_dir):
        os.mkdir(to_convert_dir)
    global decks_paths
    global decks_stems
    global to_convert_paths
    global to_convert_stems
    decks_paths = []
    decks_stems = []
    to_convert_paths = []
    to_convert_stems = []
    for itm in decks_dir.rglob('*.json'):
        decks_paths.append(itm)
        decks_stems.append(itm.stem)
    for itm in to_convert_dir.rglob('*.txt'):
        to_convert_paths.append(itm)
        to_convert_stems.append(itm.stem)


class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.ui.pushButtonSignIn.clicked.connect(self.verify_login)
        self.ui.pushButtonSignUp.clicked.connect(self.to_signup)
        self.show()

    def to_signup(self):
        self.dialog = Signup()
        self.close()
        self.dialog.show()

    def get_salt(self, email):
        url = api_url + "getsalt"
        form_data = {"email": email}
        req = requests.get(url, data=form_data)
        api_response = json.loads(req.text)
        return api_response

    def verify_login(self):
        self.entered_email = self.ui.lineEditEmail.text()
        entered_password = self.ui.lineEditPassword.text()
        stored_salt = self.get_salt(self.entered_email)
        trial_key = argon2.argon2_hash(password=entered_password, salt=stored_salt, t=16, m=512, p=2, buflen=64).hex()
        url = api_url + "verifylogin"
        form_data = {"email": self.entered_email, "key": str(trial_key)}
        req = requests.get(url, data=form_data)
        api_response = json.loads(req.text)
        if api_response is False:
            self.ui.labelResponse.setText('Incorrect login information.')
            return False
        else:
            global user_id
            user_id = api_response[0]
            global pinata_api_key
            pinata_api_key = api_response[4]
            global pinata_secret_key
            pinata_secret_key = api_response[5]
            self.starting_sync()
            self.open_start_menu()
            return True

    def media_downloader(self, deck_file_path):
        # In the future, make this optional to do every time or not
        print("downloading media files")
        with open(deck_file_path) as fileobj:
            deck = json.loads(fileobj.read())
        deck_id = deck['deck_id']
        media_folder = str(decks_dir) + '/' + 'media_' + deck_id + '/'
        if not os.path.exists(media_folder):
            os.mkdir(media_folder)
        counter = 1
        for card in deck['cards']:
            for item in card.items():
                #item[0] will be front or back image
                media_write_file_path = media_folder + card['card_id'] + ';' + item[0] + '.jpg'
                url = item[1]
                try:
                    if not os.path.exists(media_write_file_path):
                        if 'https://ipfs.io' in item[1] or 'https://gateway.pinata.cloud/ipfs/' in url:
                            response = requests.get(url, stream=True)
                            print("     downloading media file: " + str(counter))
                            counter += 1
                            with open(media_write_file_path, 'wb') as out_file:
                                shutil.copyfileobj(response.raw, out_file)
                            del response
                        elif 'http' in url:
                            response = requests.get(url, stream=True)
                            print("     downloading media file: " + str(counter))
                            counter += 1
                            with open(media_write_file_path, 'wb') as out_file:
                                shutil.copyfileobj(response.raw, out_file)
                            del response
                except:
                    print("Error downloading media")


    def media_IPFS_uploader(self, deck_file_path, uploaded_file_names, replace_links='no'):
        # In the future, make this optional to do every time or not
        """upload all local media files to the IPFS. The returning CIDS will be stored in in media folder as
        <deck_id>media_cids.json.  the json will be {‘media_file_name_from_app’: ‘CID’}
        optional: change all the media links in the original deck to IPFS links (test ipfs.io vs pinata speed)"""
        print("uploading media files to IPFS")
        pinata_api_headers = {"Content-Type": "application/json", "pinata_api_key": pinata_api_key,
                              "pinata_secret_api_key": pinata_secret_key}
        with open(deck_file_path) as fileobj:
            deck = json.loads(fileobj.read())
        media_cids_json = {}
        media_cids_json_file_path = str(decks_dir) + '/' + 'media_' + deck['deck_id'] + '/' + deck['deck_id']\
                                    + '_media_cids.json'
        if os.path.exists(media_cids_json_file_path):
            with open(media_cids_json_file_path) as fileobj:
                media_cids_json = json.loads(fileobj.read())

        for card in deck['cards']:
            for item in card.items():
                media_file_path = str(decks_dir) + '/' + 'media_' + deck['deck_id'] + '/' + card['card_id']\
                                  + ';' + item[0] + '.jpg'
                file_name = card['card_id'] + ';' + item[0] + '.jpg'
                if file_name not in uploaded_file_names:
                    if os.path.exists(media_file_path):
                        file = {"file": (file_name, open(media_file_path, 'rb'))}
                        req = requests.post(pinata_file_url, headers=pinata_api_headers, files=file)
                        pastebin_text = json.loads(req.text)
                        media_file_cid = pastebin_text['IpfsHash']
                        media_cids_json[file_name] = media_file_cid

                        if replace_links == 'yes':
                            new_url = "https://gateway.pinata.cloud/ipfs/" + media_file_cid
                            card[item[0]] = new_url

        write_to_file = open(media_cids_json_file_path, 'w+')
        write_to_file.write(json.dumps(media_cids_json, sort_keys=True, indent=4))
        write_to_file.close()

        if replace_links == 'yes':
            write_to_file = open(deck_file_path, 'w+')
            write_to_file.write(json.dumps(deck, sort_keys=True, indent=4))
            write_to_file.close()

    def starting_sync(self):
        """after login, check the database for the users decks:
             goal is that all decks and media in the local file are in the db and vice versa, and that the ones left have the newest
             timestamp. After that make sure that they are all on pinata, and that the CID list(version list) is current."""
        self.ui.labelResponse.setText('Starting sync')
        pinata_api_headers = {"Content-Type": "application/json", "pinata_api_key": pinata_api_key,
                              "pinata_secret_api_key": pinata_secret_key}
        # build the local_decks list by iterating through all the files in the decks folder
        users_folder = program_directory / 'users'
        if not os.path.exists(users_folder):
            os.mkdir(users_folder)
        user_dir = program_directory / 'users' / user_id
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
        global decks_dir
        decks_dir = user_dir / 'decks'
        if not os.path.exists(decks_dir):
            os.mkdir(decks_dir)
        local_decks = []
        local_decks_path_list = Path(decks_dir).glob('**/*.json')
        for path in local_decks_path_list:
            path_in_str = str(path)
            # to do: add more tests here to make sure the decks are in the proper format.
            with open(path_in_str) as fileobj:
                deck = json.loads(fileobj.read())
                local_decks.append(deck)
        # get the db user_collection list of deck_ids
        url = api_url + "usercollection"
        form_data = {"user_id": user_id}
        req = requests.get(url, data=form_data)
        print('get user collection', req.status_code)
        self.ui.labelResponse.setText('Starting sync')

        db_user_collec_deck_ids = json.loads(req.text)[2]
        # check the local user_collection file
        local_user_collection_file_path = str(user_dir) + '/' + "user_collection.json"
        # if it exists, add the db decks that weren't in it already
        local_user_collection = {'deck_ids': []}
        if os.path.exists(local_user_collection_file_path):
            with open(local_user_collection_file_path) as fileobj:
                local_user_collection = json.loads(fileobj.read())
        local_user_collec_deck_ids = []
        # Some local decks might be in the deck folder, but not in the local user_collections file. add them:
        for local_deck in local_decks:
            if local_deck['deck_id'] not in local_user_collec_deck_ids:
                local_user_collec_deck_ids.append(local_deck['deck_id'])

        # union-ify the two lists
        combined_user_collection_deck_ids = list(set().union(db_user_collec_deck_ids, local_user_collec_deck_ids))
        in_db_not_in_local = list(set(db_user_collec_deck_ids).difference(local_user_collec_deck_ids))
        in_local_not_in_db = list(set(local_user_collec_deck_ids).difference(db_user_collec_deck_ids))
        in_local_and_db = list(set(db_user_collec_deck_ids).intersection(local_user_collec_deck_ids))

        # build the db_decks list by downloading from the db
        url = api_url + "getdecks"
        form_data = {"deck_ids": json.dumps(db_user_collec_deck_ids)}
        req = requests.get(url, data=form_data)
        print('get decks', req.status_code)
        db_decks = json.loads(req.text)

        # As we compare versions and only keep the newest versions in both local and db,
        # we need to keep a running list of the final list of decks to use later.
        combined_decks = []
        for local_deck in local_decks:
            if local_deck['deck_id'] in in_local_and_db:
                for db_deck in db_decks:
                    # if the decks have the same ID, store whichever is newer in the local and cloud
                    if local_deck['deck_id'] == db_deck['deck_id']:
                        if local_deck['edited'] == db_deck['edited']:
                            # neither needs to be updated, but we still need the deck in our combined deck list for later
                            combined_decks.append(db_deck)
                        # if the deck in local storage is older and its edited timestamp is smaller; overwrite it
                        elif local_deck['edited'] < db_deck['edited']:
                            # if the deck name has been changed, we also need to delete the original file
                            if local_deck['title'] != db_deck['title']:
                                deck_file_path = str(decks_dir) + '/' + local_deck['title'] + ".json"
                                os.remove(deck_file_path)
                            print('overwriting older version in local folder. deck: ', local_deck['title'])
                            deck_file_path = str(decks_dir) + '/' + db_deck['title'] + ".json"
                            write_to_file = open(deck_file_path, 'w+')
                            write_to_file.write(json.dumps(db_deck, sort_keys=True, indent=4))
                            write_to_file.close()
                            # finally add to combined decks
                            combined_decks.append(db_deck)
                        # if the local deck is newer, it must be uploaded to the db to overwrite the previous one
                        elif local_deck['edited'] > db_deck['edited']:
                            # we'll do a put/update, because the entry already exists
                            print('updating database with changes made locally')
                            url = api_url + "putdeck"
                            form_data = {"deck_id": local_deck['deck_id'], "title": local_deck['title'],
                                         "edited": local_deck['edited'], "deck": json.dumps(local_deck),
                                         "deck_cid": "empty"}
                            req = requests.put(url, data=form_data)
                            print('putdeck', req.status_code)
                            # finally add to combined decks
                            combined_decks.append(local_deck)
            elif local_deck['deck_id'] in in_local_not_in_db:
                # we'll do a post/insert, because the entry doesn't exist in the database
                url = api_url + "postdeck"
                form_data = {"deck_id": local_deck['deck_id'], "title": local_deck['title'],
                             "edited": local_deck['edited'], "deck": json.dumps(local_deck)}
                req = requests.post(url, data=form_data)
                print('postdeck', local_deck['deck_id'], req.status_code)
                # add these directly to combined decks
                combined_decks.append(local_deck)

        for db_deck in db_decks:
            # If the database deck isn't in local storage, store it there
            if db_deck['deck_id'] in in_db_not_in_local:
                print('storing deck to local folder. deck: ', db_deck['title'])
                deck_file_path = str(decks_dir) + '/' + db_deck['title'] + ".json"
                write_to_file = open(deck_file_path, 'w+')
                write_to_file.write(json.dumps(db_deck, sort_keys=True, indent=4))
                write_to_file.close()
                # add these directly to combined decks
                combined_decks.append(db_deck)

        # for the media downloader, we need the decks' file path, make sure the recently downloaded db decks are included,
        # so refresh list
        updated_local_decks_path_list = Path(decks_dir).glob('**/*.json')
        for path in updated_local_decks_path_list:
            self.media_downloader(path)

        # Start IPFS upload sequence:
        # get previously pinned deck_ids
        req = requests.get(pinata_get_pinned_url, headers=pinata_api_headers)
        pinata_api_response = json.loads(req.text)
        uploaded_file_names = []
        # print("The pastebin text is:%s" % pinata_api_response)
        for row in pinata_api_response['rows']:
            uploaded_file_names.append(row['metadata']['name'])
        print("uploaded deck ids: ", uploaded_file_names)
        # create or open the "all_deck_cids.json" file, load it as all_deck_cids dictionary,
        all_deck_cids_file_path = str(user_dir) + '/' + "all_deck_cids.json"
        all_deck_cids = {}
        if os.path.exists(all_deck_cids_file_path):
            with open(all_deck_cids_file_path) as fileobj:
                all_deck_cids = json.loads(fileobj.read())
        # deck uploader:
        for deck in combined_decks:
            # if deck isnt in pinata (check metadata)
            deck_upload_name = "deck: " + deck['deck_id'] + "_edited:_" + str(deck['edited'])
            if deck_upload_name in uploaded_file_names:
                print("deck version has already been uploaded to IPFS: ")
                print("deck:_" + deck_upload_name)
            if deck_upload_name not in uploaded_file_names:
                # create or open the "<deck>_cids.json" file, load it as deck_cids dictionary
                deck_cids_file_path = str(user_dir) + '/' + deck['deck_id'] + "_cids.json"
                deck_cids = {}
                if os.path.exists(deck_cids_file_path):
                    with open(deck_cids_file_path) as fileobj:
                        deck_cids = json.loads(fileobj.read())
                # then pin to pinata
                print("uploading deck to IPFS: ")
                print("deck:_" + deck_upload_name)
                json_data_for_API = {}
                json_data_for_API["pinataMetadata"] = {"name": deck_upload_name}
                json_data_for_API["pinataContent"] = deck
                req = requests.post(pinata_json_url, json=json_data_for_API, headers=pinata_api_headers)
                pinata_api_response = json.loads(req.text)
                deck_cid = pinata_api_response["IpfsHash"]
                # 'edited' is deck edited time
                edited = deck['edited']
                # save the server response as 'deck_cid' and add it to deck_cids dictionary, "edited", "deck_cid"
                deck_cids[str(edited)] = deck_cid
                # save "<deck>_cids.json" locally in the user username folder
                write_to_file = open(deck_cids_file_path, 'w+')
                write_to_file.write(json.dumps(deck_cids, sort_keys=True, indent=4))
                write_to_file.close()
                # update the database public.decks, deck_cid with the most recent CID
                print('updating database with most recent IPFS CID hash')
                url = api_url + "putdeckcid"
                form_data = {"deck_id": deck['deck_id'], "deck_cid": deck_cid}
                req = requests.put(url, data=form_data)
                print('putdeckcid', req.status_code)
                # pin the "<deck>_cids.json" file to pinata
                json_data_for_API["pinataMetadata"] = {"name": "deck_cids:_" + deck['deck_id']}
                json_data_for_API["pinataContent"] = deck_cids
                req = requests.post(pinata_json_url, json=json_data_for_API, headers=pinata_api_headers)
                pinata_api_response = json.loads(req.text)
                deck_cids_cid = pinata_api_response["IpfsHash"]
                print("deck CIDS CID: ", deck_cids_cid)
                # Store the response CID in all_deck_cids dictionary 'edited' : '<deck>_cids_cid', edited is current time
                edited = str(round(time.time()))
                all_deck_cids[edited] = deck_cids_cid

        # Upload media
        for path in updated_local_decks_path_list:
            self.media_IPFS_uploader(path, uploaded_file_names)

        # write "all_deck_cids.json" file to local disk
        write_to_file = open(all_deck_cids_file_path, 'w+')
        write_to_file.write(json.dumps(all_deck_cids, sort_keys=True, indent=4))
        write_to_file.close()

        # add "all_deck_cids.json" to local user_collection.json, save to local disk
        print("all deck cids: ", all_deck_cids)
        local_user_collection["all_deck_cids"] = all_deck_cids
        local_user_collection['deck_ids'] = combined_user_collection_deck_ids
        local_user_collection['user_id'] = user_id

        # create or open the "user_collection_history.json" file, load it as user_collection_history dictionary,
        user_collection_history_file_path = str(user_dir) + '/' + "user_collection_history.json"
        user_collection_history = {}
        if os.path.exists(user_collection_history_file_path):
            with open(user_collection_history_file_path) as fileobj:
                user_collection_history = json.loads(fileobj.read())

        # pin the "user_collection.json " file to pinata
        upload_time = str(round(time.time()))
        json_data_for_API = {}
        json_data_for_API["pinataMetadata"] = {"name": "user_collection_user:_" + user_id + "_edited:_" + upload_time}
        json_data_for_API["pinataContent"] = local_user_collection
        req = requests.post(pinata_json_url, json=json_data_for_API, headers=pinata_api_headers)
        pinata_api_response = json.loads(req.text)
        user_collection_cid = pinata_api_response["IpfsHash"]
        print("user collection CID: ", user_collection_cid)
        # response CIDs stored user_collection_history dictionary: {‘edited’: ‘user_collection.json_CID,’}
        user_collection_history[upload_time] = user_collection_cid

        # save the "user_collection_history.json" file in local
        write_to_file = open(user_collection_history_file_path, 'w+')
        write_to_file.write(json.dumps(user_collection_history, sort_keys=True, indent=4))
        write_to_file.close()

        # save the "user_collection.json" file in local
        write_to_file = open(local_user_collection_file_path, 'w+')
        write_to_file.write(json.dumps(local_user_collection, sort_keys=True, indent=4))
        write_to_file.close()

        # update the database with the user collection
        url = api_url + "putusercollection"
        form_data = {'deck_ids': json.dumps(local_user_collection['deck_ids']),
                     'all_deck_cids': json.dumps(local_user_collection['all_deck_cids']),
                     'user_id': user_id}
        req = requests.put(url, data=form_data)
        print('put user collection', req.status_code)

        # # check we got em all
        # for deck in combined_decks:
        #     print(deck['deck_id'])
        # print(combined_user_collection_deck_ids)

        self.open_start_menu()

    def closing_sync(self):
        """before closing the app, upload decks to pinata and to the db, create a json file in local storage that also has the IPFC
    CID addresses"""

    def open_start_menu(self):
        self.dialog = StartMenu()
        self.close()
        self.dialog.show()


class Signup(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Signup()
        self.ui.setupUi(self)
        self.ui.pushButtonSignup.clicked.connect(self.verify_signup)
        self.ui.pushButtonPinata.clicked.connect(self.pinata_link)
        self.ui.pushButtonBack.clicked.connect(self.to_login)
        self.show()

    def verify_signup(self):
        new_email = self.ui.lineEditEmail.text()
        password = self.ui.lineEditPassword.text()
        repeat_password = self.ui.lineEditPassword.text()
        pinata_api = self.ui.lineEditPinataAPI.text()
        pinata_key = self.ui.lineEditPinataKey.text()
        new_user_id = uuid.uuid4().hex
        new_salt = secrets.token_hex(32)
        key = argon2.argon2_hash(password=password, salt=new_salt, t=16, m=512, p=2, buflen=64).hex()
        if new_email == "" or password == "" or repeat_password == "" or pinata_api == "" or pinata_key == "":
            self.ui.labelResponse.setText("All fields are required")
            return
        elif "@" not in new_email or "." not in new_email:
            self.ui.labelResponse.setText("Please input a valid email address")
            return
        elif len(password) < 8:
            self.ui.labelResponse.setText("Password must be more than 8 characters long")
            return
        elif password != repeat_password:
            self.ui.labelResponse.setText("Passwords did not match")
            return
        else:
            url = api_url + 'verifysignup'
            form_data = {"email": new_email, "new_user_id": new_user_id, "new_email": new_email, "key": key,
                         "new_salt": new_salt, "pinata_api": pinata_api, "pinata_key": pinata_key}
            req = requests.get(url, data=form_data)
            print(req)
            print(req.text)
            api_response = json.loads(req.text)
            if api_response == "email_exists":
                self.ui.labelResponse.setText("Email already already in database.")
                return
            if api_response == "success":
                self.ui.labelResponse.setText("Sign up successful!")
                # add something here to query database and see if values are all there properly?
                return
            else:
                self.ui.labelResponse.setText("Encountered error.")
                return

    def pinata_link(self):
        QDesktopServices.openUrl(QUrl('https://pinata.cloud/signup'))

    def to_login(self):
        self.dialog = Login()
        self.close()
        self.dialog.show()


class StartMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_StartMenu()
        self.ui.setupUi(self)
        refresh_decks_and_files_lists()
        for itm in decks_stems:
            self.ui.listWidgetDecks.addItem(itm)
        self.ui.pushButtonUseDeck.clicked.connect(self.open_deck_menu)
        self.ui.listWidgetDecks.doubleClicked.connect(self.open_deck_menu)
        self.ui.listWidgetDecks.currentItemChanged.connect(self.on_item_changed)
        self.ui.pushButtonDeckImporter.clicked.connect(self.open_import_menu)
        self.show()

    def on_item_changed(self, curr, prev):
        self.deck_selection = curr.text()

    def open_deck_menu(self):
        self.dialog = DeckMenu(self.deck_selection)
        self.close()
        self.dialog.show()

    def open_import_menu(self):
        self.dialog = ImportMenu()
        self.close()
        self.dialog.show()


class ImportMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ImportMenu()
        self.ui.setupUi(self)
        self.ui.pushButtonBack.clicked.connect(self.open_start_menu)
        self.ui.pushButtonImport.clicked.connect(self.open_import_options)
        refresh_decks_and_files_lists()
        for itm in decks_stems:
            self.ui.listDeckLibrary.addItem(itm)
        for itm in to_convert_stems:
            self.ui.listFiles.addItem(itm)
        self.ui.listFiles.doubleClicked.connect(self.open_import_options)
        # self.ui.listDeckLibrary.doubleClicked.connect(self.open_export_options)
        # self.deck_selection = self.ui.listDeckLibrary.currentItem().text()
        self.ui.listFiles.currentItemChanged.connect(self.on_item_changed)
        self.show()

    def on_item_changed(self, curr, prev):
        self.file_selection = curr.text()

    def open_start_menu(self):
        self.dialog = StartMenu()
        self.close()
        self.dialog.show()

    def open_import_options(self):
        self.popup = ImportOptions(self.file_selection)
        self.popup.show()


class ImportOptions(QDialog):
    def __init__(self, file_stem):
        super().__init__()
        self.ui = Ui_ImportOptions()
        self.ui.setupUi(self)
        self.ui.pushButtonConvert.clicked.connect(self.call_quizlet_importer)
        for itm in to_convert_paths:
            if itm.stem == file_stem:
                self.file_path = str(itm)
        self.file_stem = file_stem
        self.show()

    def call_quizlet_importer(self):
        if self.ui.lineEditFbSep.text() != "":
            self.f_bsep = self.ui.lineEditFbSep.text()
        else:
            self.f_bsep = "\t"
        if self.ui.lineEditCardSep.text() != "":
            self.cardsep = self.ui.lineEditCardSep.text()
        else:
            self.cardsep = "\n"
        self.quizlet_importer(self.file_path, user_id, fbsep=self.f_bsep, cardsep=self.cardsep)

    def quizlet_importer(self, file_path, author, fbsep="\t", cardsep="\n"):
        def create_deck(title, author, has_media=False, has_html=False, deck_tags=[], visibility="public",
                        editable_by="only_me", description=None, lang_front="en", lang_back="en", cards=[],
                        term_count=0):
            return {
                "deck_id": uuid.uuid4().hex,
                "title": title,
                "created_by": author,
                "term_count": term_count,
                "has_media": has_media,
                "has_html": has_html,
                "deck_tags": deck_tags,
                "visibility": visibility,
                "editable_by": editable_by,
                "description": description,
                "lang_front": lang_front,
                "lang_back": lang_back,
                "cards": cards,
                "edited": time.gmtime()
            }

        def create_card(front_text=None, front_html=None, front_image=None, front_video=None, front_gif=None,
                        front_audio=None,
                        back_text=None, back_html=None, back_image=None, back_video=None, back_gif=None,
                        back_audio=None,
                        note_text=None, note_html=None, note_image=None, note_video=None, note_gif=None,
                        note_audio=None,
                        card_tags=[]):
            card = {
                "card_id": uuid.uuid4().hex,
                "card_tags": card_tags,
                "front_text": front_text,
                "front_html": front_html,
                "front_image": front_image,
                "front_video": front_video,
                "front_gif": front_gif,
                "front_audio": front_audio,
                "back_text": back_text,
                "back_html": back_html,
                "back_image": back_image,
                "back_video": back_video,
                "back_gif": back_gif,
                "back_audio": back_audio,
                "note_text": note_text,
                "note_html": note_html,
                "note_image": note_image,
                "note_video": note_video,
                "note_gif": note_gif,
                "note_audio": note_audio
            }
            card1 = {}
            for item in card.items():
                if item[1] is not None:
                    card1[item[0]] = item[1]
            return card1

        cards = []
        with open(file_path) as fileobj:
            data0 = fileobj.readlines()
        print("fbsep\n",fbsep)
        print('cardsep\n',cardsep)
        # First combine all lines into a long string.
        data1 = ""
        for line1 in data0:
            data1 += line1
        print("data1\n", data1)
        # Then split by the cardsep
        data2 = data1.split(cardsep)
        print("data2 before join\n", data2)
        # For default setting, we must rejoin the lines that were separated by a linebreak
        if cardsep == "\n":
            clean_counter = 0
            while clean_counter < len(data2):
                print("clean counter\n", clean_counter)
                print("data2 len\n", len(data2))
                clean_counter = 0
                for itm0 in data2:
                    print(itm0.count(fbsep),"\n",itm0)
                    # if the cardsep is not in there, its a floating line. if its got a cardsep and an http, its a
                    # floating line plus an image and needs to be joined as well.
                    if itm0.count(fbsep) == 1 and 'https://' in itm0:
                        data2[data2.index(itm0) - 1] += "\n" + data2.pop(data2.index(itm0))
                        break
                    elif fbsep not in itm0 and 'https://' not in itm0:
                        data2[data2.index(itm0) - 1] += "\n" + data2.pop(data2.index(itm0))
                        break
                    elif 'https://' not in itm0 and itm0.count(fbsep) == 1 or \
                            'https://' in itm0 and itm0.count(fbsep) == 2:
                        clean_counter += 1
        print("data2 after join\n", data2)
        data3 = []
        for itm2 in data2:
            if itm2 is not "" and itm2 is not "\n" and itm2 is not "":
                data3.append(itm2.split(fbsep))
        print("data3\n", data3)
        for itm in data3:
            if len(itm) == 1:
                print(itm, "Item has a blank front or back and was not included")
            if len(itm) == 2:
                cards.append(create_card(front_text=itm[0], back_text=itm[1]))
            if len(itm) == 3:
                cards.append(create_card(front_text=itm[0], back_text=itm[1], back_image=itm[2]))
        print("cards\n", cards)
        media_check = False
        for itm3 in cards:
            if 'back_image' in itm3 or "front_image" in itm3 or "front_video" in itm3 or  \
                    "front_gif" in itm3 or "front_audio" in itm3 or "back_image" in itm3 or \
                    "back_video"  in itm3 or "back_gif" in itm3 or "back_audio" in itm3 or \
                    "note_image" in itm3 or "note_video" in itm3 or "note_gif" in itm3 or "note_audio" in itm3:
                media_check = True
        deck_length = len(cards)
        output_deck = create_deck(self.file_stem, author, cards=cards, has_media=media_check, term_count=deck_length)
        # Write the dictionary to a new file with the same name, but a .json extension
        write_file_path = str(decks_dir) + '/' + self.file_stem + ".json"
        write_to_file = open(write_file_path, 'w+')
        write_to_file.write(json.dumps(output_deck, sort_keys=True, indent=4))
        write_to_file.close()
        refresh_decks_and_files_lists()
        self.close()
        return output_deck


class DeckMenu(QDialog):
    def __init__(self, deck_name):
        super().__init__()
        self.ui = Ui_DeckMenu()
        self.ui.setupUi(self)
        self.deck_name = deck_name
        self.ui.pushButtonQuit.clicked.connect(self.close)
        self.ui.pushButtonQuizzes.clicked.connect(self.open_quiz_choose)
        self.ui.pushButtonImporter.clicked.connect(self.open_start_menu)
        self.show()

    def open_quiz_choose(self):
        self.dialog = QuizChoose(deck_name=self.deck_name)
        self.close()
        self.dialog.show()

    def open_start_menu(self):
        self.dialog = StartMenu()
        self.close()
        self.dialog.show()


class QuizChoose(QDialog):
    def __init__(self, deck_name):
        super().__init__()
        self.ui = Ui_QuizChoose()
        self.ui.setupUi(self)
        self.deck_name = deck_name
        deck_path = str(decks_dir) + '/' + self.deck_name + ".json"
        file_to_open = open(deck_path, 'r')
        deck_dict = json.loads(file_to_open.read())
        file_to_open.close()
        self.ui.horizontalSliderQuestNum.setMaximum(len(deck_dict['cards']))
        self.ui.horizontalSliderQuestNum.valueChanged.connect(self.slider_horizontal)
        self.ui.lineEditQuestNum.textEdited.connect(self.move_slider)
        self.show()
        self.quiz_length = 0
        self.quiz_direction = "f"
        self.ui.radioButtonBtoF.toggled.connect(self.BtoF_chosen)
        self.ui.pushButtonMultiChoice.clicked.connect(self.open_multi_choice)

    def BtoF_chosen(self):
        self.quiz_direction = "b"

    def slider_horizontal(self, value):
        self.ui.lineEditQuestNum.setText(str(value))
        self.quiz_length = value

    def move_slider(self, value):
        if value.isnumeric():
            self.ui.horizontalSliderQuestNum.setValue(int(value))
            self.quiz_length = int(value)

    def open_multi_choice(self):
        if self.quiz_length > 0:
            self.dialog = MultiChoice(self.deck_name, self.quiz_direction, self.quiz_length)
            self.close()
            self.dialog.show()
        else:
            pass


class MultiChoice(QDialog):
    """
    give a flashcard quiz where quiz taker must type in the correct answer exactly as written on the card

    :param dict, deck_name: file name without extension in decks/ folder.
           should be a dictionary of word-definition pairs, must be at least 4 terms long.
    :param str, direction:  "f" for front to self.back, and "b" for self.back to front.
    :param quiz_length: int, length of the quiz
    """
    def __init__(self, deck_name, direction, quiz_length):
        super().__init__()
        self.ui = Ui_MultiChoice()
        self.ui.setupUi(self)
        self.deck_name = deck_name
        deck_path = str(decks_dir) + '/' + self.deck_name + ".json"
        file_to_open = open(deck_path, 'r')
        self.deck = json.loads(file_to_open.read())
        file_to_open.close()
        # Converts dict into list of key/value tuples

#        initial_pairs = [pair for pair in self.deck_dict.items()]
        # Add as many questions to the quiz as the user had specified
        self.game_pairs = []
        while len(self.game_pairs) < int(quiz_length):
            quest_to_add = self.deck['cards'][random.randrange(len(self.deck['cards']))]
            # print(self.deck['cards'][random.randrange(len(self.deck))])
            if quest_to_add not in self.game_pairs:
                self.game_pairs.append(quest_to_add)
        # Cause our default mode is "f" so lets let f's backs and fronts be correct
        self.front_text = 'front_text'
        self.back_text = 'back_text'
        self.front_image = 'front_image'
        self.back_image = 'back_image'
        # And "b" will be flipped
        if direction == "b":
            self.front_text = 'back_text'
            self.back_text = 'front_text'
            self.front_image = 'back_image'
            self.back_image = 'front_image'
        self.score = 0
        self.top_score = len(self.game_pairs)
        self.wrong_first_guess = False
        self.right_first_guess = False
        self.multi_dict = [" ", " ", " ", " "]
        self.random_card = None
        self.answer = None
        self.dialog = None
        self.ui.QLabelA.clicked.connect(self.to_answer_checker_a)
        self.ui.QLabelB.clicked.connect(self.to_answer_checker_b)
        self.ui.QLabelC.clicked.connect(self.to_answer_checker_c)
        self.ui.QLabelD.clicked.connect(self.to_answer_checker_d)
        self.ui.pushButtonNext.clicked.connect(self.delete_and_next_round)
        self.show()
        if len(self.game_pairs) > 0:
            self.game_round()

    def game_round(self):
        if len(self.game_pairs) > 0:
            self.multi_dict = [" ", " ", " ", " "]
            # From the tuple list, select a random index,
            # this would need to change for other formatting
            self.random_card = self.game_pairs[random.randrange(0, len(self.game_pairs))]
            # list of random card backs/fronts, including one that is the answer
            self.multi_dict[random.randrange(0, 4)] = self.random_card
            # Display front of card(key) in prompt, and self.answer must be its value
            self.answer = self.random_card[self.back_text]
            # Build the list from the whole deck
            # Generate the random index for where to insert, skip if the same as the answer index
            for card in self.deck['cards']:
                fill_location = random.randrange(0, 4)
                if self.multi_dict.count(" ") == 0:
                    break
                else:
                    if card[self.back_text] not in self.multi_dict:
                        if fill_location != self.random_card and self.multi_dict[fill_location] == " ":
                            self.multi_dict[fill_location] = card
            self.ui.QLabelCard.setText(self.random_card[self.front_text])
            # need to add image to top here as well
            self.ui.QlabelCorrect.setText("      ")
            print('multi dict\n')
            print(self.multi_dict)
            if self.back_image in self.multi_dict[0]:
                # will have to change this to deal with image names in the deck that weren't originally jpg
                self.image_locA = str(decks_dir) + '/' + 'media_' + self.deck['deck_id'] + '/' + \
                            self.multi_dict[0]['card_id'] + ';' + self.back_image + '.jpg'
                print(self.image_locA)
                self.ui.ImgLabelA.setStyleSheet("border-image: url(" + self.image_locA + "); min-height: 50px; min-width: 100px")
                print('can see theres an image')
            else:
                self.ui.ImgLabelA.setStyleSheet("")
                print('couldnt find an image')
            if self.back_image in self.multi_dict[1]:
                self.image_locB = str(decks_dir) + '/' + 'media_' + self.deck['deck_id'] + '/' + \
                            self.multi_dict[1]['card_id'] + ';' + self.back_image + '.jpg'
                print(self.image_locB)
                self.ui.ImgLabelB.setStyleSheet("#ImgLabelB {border-image: url(" + self.image_locB + "); min-height: 50px; min-width: 100px}")
                print('can see theres an image')
            else:
                self.ui.ImgLabelB.setStyleSheet("")
                print('couldnt find an image')
            if self.back_image in self.multi_dict[2]:
                print('can see theres an image')

                self.image_locC = str(decks_dir) + '/' + 'media_' + self.deck['deck_id'] + '/' + \
                            self.multi_dict[2]['card_id'] + ';' + self.back_image + '.jpg'
                print(self.image_locC)
                self.ui.ImgLabelC.setStyleSheet("border-image: url(" + self.image_locC + "); min-height: 50px; min-width: 100px")
            else:
                self.ui.ImgLabelC.setStyleSheet("")
                print('couldnt find an image')
            if self.back_image in self.multi_dict[3]:

                self.image_locD = str(decks_dir) + '/' + 'media_' + self.deck['deck_id'] + '/' + \
                            self.multi_dict[3]['card_id'] + ';' + self.back_image + '.jpg'
                print(self.image_locD)

                self.ui.ImgLabelD.setStyleSheet("border-image: url(" + self.image_locD + "); min-height: 50px; min-width: 100px")
                print('can see theres an image')
            else:
                self.ui.ImgLabelD.setStyleSheet("")
                print('couldnt find an image')
            self.ui.horizontalWidget_A.setStyleSheet("#horizontalWidget_A {border-image: url(/Users/chenlu/"
                                                "PycharmProjects/experiments1/IPFC/PyQT_App/card_graphic_bottom.jpg)}")
            self.ui.horizontalWidget_B.setStyleSheet("#horizontalWidget_B {border-image: url(/Users/chenlu/"
                                                "PycharmProjects/experiments1/IPFC/PyQT_App/card_graphic_bottom.jpg)}")
            self.ui.horizontalWidget_C.setStyleSheet("#horizontalWidget_C {border-image: url(/Users/chenlu/"
                                                "PycharmProjects/experiments1/IPFC/PyQT_App/card_graphic_bottom.jpg)}")
            self.ui.horizontalWidget_D.setStyleSheet("#horizontalWidget_D {border-image: url(/Users/chenlu/"
                                                "PycharmProjects/experiments1/IPFC/PyQT_App/card_graphic_bottom.jpg)}")
            self.ui.QLabelA.setText(self.multi_dict[0][self.back_text])
            self.ui.QLabelA.setStyleSheet("background-color: white")
            self.ui.QLabelB.setText(self.multi_dict[1][self.back_text])
            self.ui.QLabelB.setStyleSheet("background-color: white")
            self.ui.QLabelC.setText(self.multi_dict[2][self.back_text])
            self.ui.QLabelC.setStyleSheet("background-color: white")
            self.ui.QLabelD.setText(self.multi_dict[3][self.back_text])
            self.ui.QLabelD.setStyleSheet("background-color: white")
            self.repaint()
            self.wrong_first_guess = False
            self.right_first_guess = False
        else:
            return None

    def to_answer_checker_a(self):
        self.answer_checker(self.multi_dict[0][self.back_text], self.ui.horizontalWidget_A)

    def to_answer_checker_b(self):
        self.answer_checker(self.multi_dict[1][self.back_text], self.ui.horizontalWidget_B)

    def to_answer_checker_c(self):
        self.answer_checker(self.multi_dict[2][self.back_text], self.ui.horizontalWidget_C)

    def to_answer_checker_d(self):
        self.answer_checker(self.multi_dict[3][self.back_text], self.ui.horizontalWidget_D)

    def answer_checker(self, guess, guess_label):
        if guess == self.answer:
            self.right_first_guess = True
            guess_label.setStyleSheet("background-color: green")
            if not self.wrong_first_guess:
                self.ui.QlabelCorrect.setText("Correct")
                self.score += 1

        elif guess != self.answer:
            self.wrong_first_guess = True
            guess_label.setStyleSheet("background-color: red")
            if not self.right_first_guess:
                self.ui.QlabelCorrect.setText("Incorrect")

    def delete_and_next_round(self):
        if len(self.game_pairs) <= 1:
            self.ui.pushButtonNext.setText("Finish Quiz")
            self.game_over()
        elif self.random_card in self.game_pairs:
            self.game_pairs.remove(self.random_card)
            self.game_round()

    def game_over(self):
        self.ui.pushButtonNext.clicked.connect(self.quit)
        #self.ui.QlabelCorrect.setText(f"Your score was {str(round(100 * self.score / self.top_score, 2))}%. " /
        #                              f"You got {str(self.score)} / {str(self.top_score)} cards correct.")

    def quit(self):
        self.dialog = DeckMenu(self.deck_name)
        self.close()
        self.dialog.show()


# refresh_decks_and_files_lists()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())
