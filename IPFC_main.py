# TO DO:
#
# add images, gifs, videos, audio to cards. fix formatting issue in multi choice
# deck viewer and card flipper reviewer
# add other quiz modes
# Deck editor
# in deck converter/editor: Language type, alphabetize, Deck tags, description, editable_by, viewable by
# add SRS functions, at least start with marking incorrect guessed answer, anki SRS imput.
#   make game/quiz based on SRS data,
#   share with services like gimkit how they could use SRS data to create a game session.

import sys
import os
from pathlib import Path
import json
import random
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
import uuid
import argon2
import requests
import secrets

# Import the UI files
from IPFC_Start_menu import *
from IPFC_Deck_menu import *
from IPFC_Quiz_choose import *
from IPFC_Multi_choice import *
from IPFC_Login import *
from IPFC_Signup import *
from IPFC_Import import *
from IPFC_Import_options import *


def deck_menu_constructor(paths):
    """
    Takes a list of file paths and returns a three part tuple with a label number,
the truncated filename, and the file path.

    :param list paths: a list of file file paths, must be json files containing dictionaries
    :return: a list of three part tuples (number, filename, file path)
    """
    output_list = []
    counter = 1
    for path in paths:
        file_name_w_ext = os.path.basename(path)
        file_name, file_ext = os.path.splitext(file_name_w_ext)
        tup = (counter, file_name, path)
        counter += 1
        output_list.append(tup)
    return output_list


def refresh_decks_and_files_lists():
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


decks_paths = []
decks_stems = []
to_convert_paths = []
to_convert_stems = []
program_directory = Path.cwd()
decks_dir = program_directory / 'decks/'
to_convert_dir = program_directory / 'to_convert/'
refresh_decks_and_files_lists()

user_id = ""

api_url = "https://ipfcmidware.azurewebsites.net/"




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

    def get_userid(self, email):
        url = api_url + "getuserid"
        form_data = {"email": email}
        req = requests.get(url, data=form_data)
        api_response = json.loads(req.text)
        global user_id
        user_id = api_response

    def verify_login(self):
        entered_email = self.ui.lineEditEmail.text()
        entered_password = self.ui.lineEditPassword.text()
        stored_salt = self.get_salt(entered_email)
        trial_key = argon2.argon2_hash(password=entered_password, salt=stored_salt, t=16, m=512, p=2, buflen=64).hex()
        url = api_url + "verifylogin"
        form_data = {"email": entered_email, "key": str(trial_key)}
        req = requests.get(url, data=form_data)
        api_response = json.loads(req.text)
        if not api_response:
            self.ui.labelResponse.setText('Incorrect login information.')
            return False
        if api_response:
            self.open_start_menu()
            self.get_userid(entered_email)
            return True

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
        elif "@" not in new_email and "." not in new_email:
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
                "cards": cards
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
    def __init__(self, deck):
        super().__init__()
        self.ui = Ui_DeckMenu()
        self.ui.setupUi(self)
        self.deck = deck
        self.ui.pushButtonQuit.clicked.connect(self.close)
        self.ui.pushButtonQuizzes.clicked.connect(self.open_quiz_choose)
        self.ui.pushButtonImporter.clicked.connect(self.open_start_menu)
        self.show()

    def open_quiz_choose(self):
        self.dialog = QuizChoose(deck=self.deck)
        self.close()
        self.dialog.show()

    def open_start_menu(self):
        self.dialog = StartMenu()
        self.close()
        self.dialog.show()


class QuizChoose(QDialog):
    def __init__(self, deck):
        super().__init__()
        self.ui = Ui_QuizChoose()
        self.ui.setupUi(self)
        self.deck = deck
        deck_path = "decks/" + self.deck + ".json"
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
            self.dialog = MultiChoice(self.deck, self.quiz_direction, self.quiz_length)
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
        deck_path = "decks/" + self.deck_name + ".json"
        file_to_open = open(deck_path, 'r')
        self.deck = json.loads(file_to_open.read())
        file_to_open.close()
        # Converts dict into list of key/value tuples

#        initial_pairs = [pair for pair in self.deck_dict.items()]
        # Add as many questions to the quiz as the user had specified
        self.game_pairs = []
        while len(self.game_pairs) < int(quiz_length):
            quest_to_add = self.deck['cards'][random.randrange(len(self.deck['cards']))]
            print(self.deck['cards'][random.randrange(len(self.deck))])
            if quest_to_add not in self.game_pairs:
                self.game_pairs.append(quest_to_add)
        # Cause our default mode is "f" so lets let f's backs and fronts be correct
        self.front = 'front_text'
        self.back = 'back_text'
        self.front_image = 'front_image'
        self.back_image = 'back_image'

        # And "b" will be flipped
        if direction == "b":
            self.front = 'back_text'
            self.back = 'front_text'
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
            self.multi_dict[random.randrange(0, 4)] = self.random_card[self.back]
            # Display front of card(key) in prompt, and self.answer must be its value
            self.answer = self.multi_dict.index(self.random_card[self.back])
            print('multi dict\n')
            print(self.multi_dict)
            # Build the list from the whole deck
            # Generate the random index for where to insert, skip if the same as the answer index
            for pair in self.deck['cards']:
                print(pair)
                fill_location = random.randrange(0, 4)
                if self.multi_dict.count(" ") == 0:
                    break
                else:
                    if pair[self.back] not in self.multi_dict:
                        if fill_location != self.answer and self.multi_dict[fill_location] == " ":
                            self.multi_dict[fill_location] = pair[self.back]
            self.ui.QLabelCard.setText(self.random_card[self.front])
            self.ui.QlabelCorrect.setText("      ")
            self.ui.QLabelA.setText(self.multi_dict[0])
            self.ui.QLabelA.setStyleSheet("background-color: white")
            self.ui.QLabelB.setText(self.multi_dict[1])
            self.ui.QLabelB.setStyleSheet("background-color: white")
            self.ui.QLabelC.setText(self.multi_dict[2])
            self.ui.QLabelC.setStyleSheet("background-color: white")
            self.ui.QLabelD.setText(self.multi_dict[3])
            self.ui.QLabelD.setStyleSheet("background-color: white")
            self.repaint()
            self.wrong_first_guess = False
            self.right_first_guess = False
        else:
            return None

    def to_answer_checker_a(self):
        self.answer_checker(self.multi_dict[0], self.ui.QLabelA)

    def to_answer_checker_b(self):
        self.answer_checker(self.multi_dict[1], self.ui.QLabelB)

    def to_answer_checker_c(self):
        self.answer_checker(self.multi_dict[2], self.ui.QLabelC)

    def to_answer_checker_d(self):
        self.answer_checker(self.multi_dict[3], self.ui.QLabelD)

    def answer_checker(self, guess, guess_label):
        if guess == self.random_card[self.back]:
            self.right_first_guess = True
            guess_label.setStyleSheet("background-color: green")
            if not self.wrong_first_guess:
                self.ui.QlabelCorrect.setText("Correct")
                self.score += 1

        elif guess != self.random_card[self.back]:
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
        self.ui.QlabelCorrect.setText(f"Your score was {str(round(100 * self.score / self.top_score, 2))}%. "
                                      f"You got {str(self.score)} / {str(self.top_score)} cards correct.")

    def quit(self):
        self.dialog = DeckMenu(self.deck_name)
        self.close()
        self.dialog.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())
