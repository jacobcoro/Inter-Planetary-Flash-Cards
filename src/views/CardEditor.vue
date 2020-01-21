//https://github.com/chrisvfritz/vue-enterprise-boilerplate
//https://github.com/vuejs/awesome-vue#scaffold
<template>
    <b-container fluid id="body">
        <b-row id="main-row">
        <b-col id="main-col">
        <b-container class="card">
            <b-row  class="card-row">
                <b-col v-if="card.front_image">
                    <b-img-lazy class="img" v-if="card.front_image" :src="card.front_image"></b-img-lazy>
                </b-col>
                <b-col >
                    <b-form-textarea class="card-text-input" id="front-text-input" v-model="card.front_text"></b-form-textarea>
                </b-col>
            </b-row>
        </b-container>
        <br>
        <b-container class="card">
            <b-form-textarea class="card-text-input" id="back-text-input" v-model="card.back_text"></b-form-textarea>
            <b-img-lazy v-if="card.back_image" class="img" :src="card.back_image"></b-img-lazy>
        </b-container>
        <br>
        <b-container class="tag-chooser">
            <p class="d-inline-block tags-label">Deck:
                <b-button class="add-btn" >
                    <font-awesome-icon v-if="!addingDeck" class="d-inline add-icon" @click="toggleAddingDeck()" color="white" size="1x" icon="plus-circle"/>
                    <font-awesome-icon v-if="addingDeck" class="d-inline add-icon" @click="addNewDeck()" color="white" size="1x" icon="plus-circle"/>
                    <b-form-input class="d-inline tag-input" v-if="addingDeck" v-model="newDeckTitle" >
                    </b-form-input>
                </b-button>
            </p>
            <b-button  @click="removeCardFromDeck(deck.title)" class="tag-style-button green-btn d-inline-block"  v-for="deck in includedDecks" :key="deck.deck_id" > 
                    {{ deck.title.slice(0, 24) }}
            </b-button>
            <br>
            <b-button  @click="addCardToDeck(deck.title)" class="tag-style-button white-btn d-inline-block"  v-for="deck in unincludedDecks" :key="deck.deck_id" > 
                    {{ deck.title.slice(0, 24) }}
            </b-button>
        </b-container>
        <b-container  class="tag-chooser" id="tags-bottom">
            <p class="d-inline tags-label">Tags:
                <b-button class="add-btn" >
                    <font-awesome-icon v-if="!addingTag" class="d-inline add-icon" @click="toggleAddingTag()" color="white" size="1x" icon="plus-circle"/>
                    <font-awesome-icon v-if="addingTag" class="d-inline add-icon" @click="addNewTag()" color="white" size="1x" icon="plus-circle"/>
                    <b-form-input class="d-inline tag-input" v-if="addingTag" v-model="newTagTitle" >
                    </b-form-input>
                </b-button>
            </p>
            <b-button  @click="removeTagFromCard(tag)" class="tag-style-button green-btn d-inline"  v-for="tag in card.card_tags" :key="tag" > 
                {{ tag }}
            </b-button>
            <br>
            <b-button  @click="addTagToCard(tag)" class="tag-style-button white-btn d-inline"  v-for="tag in unincludedTags" :key="tag" > 
                {{ tag }}
            </b-button>
        </b-container >
        </b-col>
        </b-row>
        <b-row id="buttons-row">
            <b-col id="buttons-col">
                <b-container id="buttons-inner">
                    <b-row>
                    <b-col >
                        <b-button :disabled="noDeckSelected" class="btn-circle btn-md" 
                            @click="deleteCard()">
                            <font-awesome-icon size="2x" icon="trash-alt"/>
                        </b-button>
                    </b-col>
                    <b-col>
                        <b-button :disabled="leftNavDisabled" class="btn-circle btn-md" 
                            @click="previousCard()">
                            <font-awesome-icon size="2x" icon="step-backward"/>
                        </b-button>
                    </b-col>
                    <b-col>    
                        <b-button :disabled="noDeckSelected" class="btn-circle btn-md" 
                            @click="undo()">
                            <font-awesome-icon size="2x" icon="undo"/>
                        </b-button>
                    </b-col>
                    <b-col>
                        <b-button :disabled="rightNavDisabled" class="btn-circle btn-md" 
                            @click="nextCard()">
                            <font-awesome-icon size="2x" icon="step-forward"/>
                        </b-button>
                    </b-col>
                    <b-col>    
                        <b-button :disabled="noDeckSelected" class="btn-circle btn-md" 
                            @click="doneCheck()">
                            <font-awesome-icon size="2x" icon="check"/>
                        </b-button>
                    </b-col>
                    </b-row>
                </b-container>
            </b-col>
           
        </b-row>  
    </b-container>
</template>

<script>
import _ from 'lodash';   
const uuidv4 = require('uuid/v4');

import { mapState } from 'vuex'
export default {
    name: 'card-editor',
    data() {
        return {
            initialDeckState : null,
            addingDeck: false,
            addingTag: false,
            newDeckTitle: "",
            newTagTitle: "",
        };
    },
    computed: {
        ...mapState({
            userCollection: 'userCollection',
            cardToEditIndex: 'cardToEditIndex',
            decksMeta: 'decksMeta',
            decks: 'decks',
            currentDeck: 'currentDeck',
            jwt: 'jwt',
            navNewCardClicked: 'navNewCardClicked'
        }),
        card() {
            return this.currentDeck.cards[this.cardIndex]
        },
        cardIndex () {
            return this.cardToEditIndex

        },
        includedDecks () {
            var card = this.card
            return this.decks.filter(function (deck) {
                if (deck != undefined){ 
                   return deck.cards.indexOf(card)>-1
                }
            })
        },
        unincludedDecks () {
            var card = this.card
            return this.decks.filter(function (deck) {
                return !deck.cards.includes(card)
            }) 
        },
        unincludedTags () {
            let allTagsList = []
            for (let deck of this.decks) {
                for (let card of deck.cards) {
                   for (let tag of card.card_tags) {
                        if (!allTagsList.includes(tag)){
                            allTagsList.push(tag)
                        }
                   }
                }
            }
            let unincludedTagsList = []
            for (let tag of allTagsList) {
                if (!this.card.card_tags.includes(tag)) {
                    unincludedTagsList.push(tag)
                }
            }
            return unincludedTagsList
        },
        leftNavDisabled () {
            if (this.cardToEditIndex === 0 || this.noDeckSelected === true){ 
            return true                        
            }
            else {
                return false
            }
        },
        rightNavDisabled () {
            if (this.cardToEditIndex === this.currentDeck.cards.length -1 || this.noDeckSelected === true) {
            return true } 
            else {
                return false
            }
        },
        noDeckSelected () {
            if (this.includedDecks.length < 1) {
                return true
            } else {
                return false
            }
        },
        unChanged () {
            let card = this.card
            let result = true
            if (card !== null && this.initialDeckState !== null) {
                for (let initialDeckCard of this.initialDeckState.cards) {
                    if (card.card_id === initialDeckCard.card_id) {
                        if ( !_.isEqual(initialDeckCard, card)) {
                            result = false
                        } else {
                            result = true
                        }
                    }
                }
            }
            return result
        }
    },
    methods: {
        deleteCard () {
            // for each of the included decks, filter out the current card from its .cards
            let changedDecks = this.unincludedDecks
            for (let deck of this.includedDecks) {
                let card = this.card
                let updatedDeckCards = deck.cards.filter(function (cards) {
                    return cards.card_id != card.card_id
                    }) 
                deck.cards = updatedDeckCards
                deck.edited = Math.round(new Date().getTime() / 1000);
                changedDecks.push(deck)
            }
            this.$store.commit('updateDecks', changedDecks)
            this.$store.dispatch('refreshDecksMeta')
            this.$router.go(-1)
        },
        previousCard() {
             if (this.unChanged === false) {
                    this.submit()
            }    
            this.$store.commit('updateCardToEditIndex', this.cardToEditIndex - 1)
        },
        undo () {
            return null
        },
        nextCard() {
            if (this.unChanged === false) {
                    this.submit()
            }    
            this.$store.commit('updateCardToEditIndex', this.cardToEditIndex + 1)
        },
        doneCheck () {
            this.submit()
            this.$router.go(-1)
        },
        submit () {
            for (let deck of this.includedDecks) {
                let card = this.card
                // get original index, as to insert in original position
                let cardInCurrentDeck = deck.cards.filter(function (cardToCheck){
                    return cardToCheck.card_id === card.card_id
                })
                let indexOfCard = deck.cards.indexOf(cardInCurrentDeck)

                // filter out the old version card from .cards
                let updatedDeckCards = deck.cards.filter(function (cardToCheck) {
                    return cardToCheck.card_id != card.card_id
                    })
                // then add new one back
                updatedDeckCards.splice(indexOfCard, 0, card)
                deck.cards = updatedDeckCards
                deck.edited = Math.round(new Date().getTime() / 1000);
                this.$store.commit('updateDeck', deck)
            }
            this.$store.dispatch('refreshDecksMeta')
        },
        removeCardFromDeck (title) {
            // console.log('removing from deck ' + title)
            for (let deck of this.decks) {
                let card = this.card
                if (deck.title === title){
                let updatedDeckCards = deck.cards.filter(function (cards) {
                    return cards.card_id != card.card_id
                    }) 
                deck.cards = updatedDeckCards
                deck.edited = Math.round(new Date().getTime() / 1000);
                this.$store.commit('updateDeck', deck)
                this.$store.dispatch('refreshDecksMeta')

                }
            }
        },
        addCardToDeck (title) {
            // console.log('adding to deck ' + title)
            for (let deck of this.decks) {
                let card = this.card
                if (deck.title == title){
                    deck.cards.push(card)
                }
            deck.edited = Math.round(new Date().getTime() / 1000);
            this.$store.commit('updateDeck', deck)
            this.$store.dispatch('refreshDecksMeta')

            }
        },
        removeTagFromCard(tag){
            this.card.card_tags.splice(this.card.card_tags.indexOf(tag),1)
            this.submit()
        },
        addTagToCard(tag){
            this.card.card_tags.unshift(tag)
            this.submit()
        },
        toggleAddingDeck () {
            this.addingDeck = !this.addingDeck
        },
        toggleAddingTag () {
            this.addingTag = !this.addingTag
        },
        addNewDeck () {
            if (this.newDeckTitle === "" || this.newDeckTitle === " ") {
                this.toggleAddingDeck()
            } else{
                let decks = this.decks
                let emptyDeck = {
                    cards: [this.card],
                    created_by: this.userCollection.user_id,
                    deck_id: uuidv4(),
                    deck_tags: [],
                    description: null,
                    editable_by: "only_me",
                    edited: Math.round(new Date().getTime() / 1000),
                    has_html:false,
                    has_media: false,
                    lang_back:"en",
                    lang_front:"en",
                    term_count: 1,
                    title: this.newDeckTitle,
                    visibility:"public",
                    icon_color: this.generateRandomHslaColor()
                    }
                decks.unshift(emptyDeck)
                this.$store.commit('updateDecks', decks)
                this.toggleAddingDeck()
            }
        },
        generateRandomHslaColor (){
            // round to an interval of 20, 0-360
            let hue = Math.round(Math.random() * 360 / 20) * 20
            let color = `hsla(${hue}, 100%, 50%, 1)`
            return color
        },
        addNewTag () {
            let allTags = this.unincludedTags.concat(this.card.card_tags)
            if (allTags.includes(this.newTagTitle) || this.newTagTitle === "" || this.newTagTitle === " ") {
                this.toggleAddingTag()
            }else {
                this.card.card_tags.unshift(this.newTagTitle)
                this.submit()
                this.toggleAddingTag()
            }
        }
        
    },
    created () {
        this.$store.commit('toggleNavNewCardDisabled', true)
        // deep copy so it doesnt change
        this.initialDeckState = JSON.parse(JSON.stringify(this.currentDeck))
    },
    watch: {
        navNewCardClicked: function() {
            this.submit()
        },
        unChanged: function () {
            this.$store.commit('toggleNavNewCardDisabled', this.unChanged || this.noDeckSelected)
        },
        noDeckSelected: function() {
            this.$store.commit('toggleNavNewCardDisabled', this.unChanged || this.noDeckSelected)
        }
    },

}
</script>

<style scoped>
#body{
    background-color: C7C7C7;
    overflow-y: auto;   
}
#main-col {
    max-width: 600px;
    margin: auto;
}
.card {
    margin: auto;
    top: 30px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 1.5em;
    padding: 0px 20px 0px;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.51);
    text-align: left;
    overflow-y: auto;
    width: 100%;
   
}
.card::-webkit-scrollbar {
    width: .5em;
}
.card::-webkit-scrollbar-thumb {
    background-color: grey;
    border-radius: 5px;
}
.card-text-input {
    border: hidden;
    word-wrap: normal;
    margin: auto;
    margin-top: 0px;
    font-size: 1em;
    padding: 0.3em 0px 0px;
    min-height: 4.8em;
}
.card-text-input::-webkit-scrollbar {
    width: .5em;
}
.card-text-input::-webkit-scrollbar-thumb {
    background-color: lightgrey;
    border-radius: 5px;
}
.img {
    margin: auto;
    margin-top: .5em;
    object-fit: fill;
    width: 90%;
    max-height: 50vh;
}

.flashcard:hover {
    box-shadow: 0 0px 25px rgba(0, 0, 0, 0.8);
}


.tag-chooser {
    margin: 1em auto;
    margin-right: 0px;
    height: 7em;
    overflow-x: auto;
    white-space: nowrap;
    position: initial;
    padding: 0px;
}

.tag-chooser::-webkit-scrollbar {
    height: .5em;
} 
.tag-chooser::-webkit-scrollbar-thumb {
    background-color: lightgrey;
    border-radius: 5px;
}
.tags-label {
    margin: 0px 0px 5px 0px;
    padding: 0px;
}

.tag-style-button {
    border-radius: 10px;
    margin: 5px 10px;
    border-width: 0px;
    color: grey;
    padding: 0.4em;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.51);

}
.green-btn {  background-color: rgba(185, 255, 184, 1)}
.white-btn {  background-color: white;}

#tags-bottom {
    margin-bottom: 80px;
}
.add-btn {
    border-radius: 10px;
    background-color: grey;
    padding: 0px 0px;
    overflow-x: hidden;
    display: inline-flex;
}
.add-icon{
    margin: .58em;
    height: 1em;
}
.tag-input{
    height: 2em;
}

.btn-circle.btn-md { 
    width: 40px; 
    height: 40px; 
    padding: 0px 11px; 
    margin: 5px auto;
    border-radius: 20px; 
    font-size: 10px; 
    text-align: center; 
    color:grey;
    background-color: white;
    border: none;
    box-shadow: 0 0px 5px rgba(0, 0, 0, 0.5);
    max-height: 25vh;
    } 
.btn-circle.btn-md:hover {
    box-shadow: 0 0px 25px rgba(0, 0, 0, 0.8);
}

#buttons-row {
    text-align: center;
    position: fixed;
    bottom: 0;
    width: 100vw;
    z-index: 1000;
    background-color: rgba(63, 47, 47, 0.3)
}
#buttons-col {
    max-width: 600px;
    margin: auto;
}


</style>