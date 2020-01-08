<template>
    <b-container fluid id="body">
        <div class="tag-chooser">
            <p class="d-inline">Deck:</p>
            <b-button  class="tag-style-button green-btn d-inline"  v-for="deck in includedDecks" :key="deck.edited" > 
                    {{ deck.title.slice(0, 24) }}
            </b-button>
            <b-button  class="tag-style-button white-btn d-inline"  v-for="deck in unincludedDecks" :key="deck.edited" > 
                    {{ deck.title.slice(0, 24) }}
            </b-button>
        </div>
      <b-container class="card">
        <b-row  class="card-row">
            <b-col v-if="card.front_image">
                <b-img-lazy class="img" v-if="card.front_image" :src="card.front_image"></b-img-lazy>
            </b-col>
            <b-col >
                <b-card-text class="font-weight-bold">{{ card.front_text }}</b-card-text>
            </b-col>
        </b-row>
      </b-container>
      <b-container class="card">
        <b-row class="card-row">
          <b-col v-if="card.back_image">
              <b-img-lazy class="img" :src="card.back_image"></b-img-lazy>
          </b-col>
          <b-col>
              <b-card-text> {{ card.back_text }} </b-card-text>
          </b-col>
        </b-row>
      </b-container>
        <div class="tag-chooser" id="tags-bottom">
            <p class="d-inline">Tags:</p>
            <b-button  class="tag-style-button green-btn d-inline"  v-for="deck in includedDecks" :key="deck.edited" > 
                {{ deck.title.slice(0, 24) }}
            </b-button>
            <b-button  class="tag-style-button white-btn d-inline"  v-for="deck in unincludedDecks" :key="deck.edited" > 
                {{ deck.title.slice(0, 24) }}
            </b-button>
        </div>
        <b-row id="buttons-row" >
            <b-col>
                <b-button class="btn-circle btn-xl" @click="incorrect()">
                    <font-awesome-icon size="2x" icon="trash-alt"/>
                </b-button>
            </b-col>
            <b-col>    
                <b-button class="btn-circle btn-xl" @click="flipCard()">
                    <font-awesome-icon size="2x" icon="undo"/>
                </b-button>
            </b-col>
            <b-col>    
                <b-button class="btn-circle btn-xl" @click="correct()">
                    <font-awesome-icon size="2x" icon="check"/>
                </b-button>
            </b-col>
        </b-row>  
    </b-container>
</template>

<script>
import { mapState } from 'vuex'
export default {
    name: 'card-editor',
    data() {
        return {
            
        };
    },
    computed: {
        ...mapState({
            card: 'cardToEdit',
            cardToEditsDeck: 'cardToEditsDeck',
            decksMeta: 'decksMeta',
            decks: 'decks'
        }),
        includedDecks () {

         var card = this.card
         return this.decks.filter(function (deck) {
                return deck.cards.indexOf(card)>-1
            })
        },
        unincludedDecks () {
         var card = this.card
             return this.decks.filter(function(deck) {
                return !deck.cards.indexOf(card)>-1
            })
        }
    }  
}
</script>

<style scoped>
#body{
    background-color: C7C7C7;
}
.card {
    margin: auto;
    margin-bottom: 30px;
    top: 35px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 1.5em;
    padding: 25px;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.51);
    text-align: left;
    overflow-y: auto;
    width: 90vw;
   
}
.card-row {
    max-height: 5em;
}

.btn-circle.btn-xl { 
    width: 60px; 
    height: 60px; 
    padding: 10px 16px; 
    margin: 10px auto;
    border-radius: 30px; 
    font-size: 12px; 
    text-align: center; 
    color:grey;
    background-color: white;
    border: none;
    box-shadow: 0 0px 5px rgba(0, 0, 0, 0.5);
    max-height: 25vh;
    } 
.btn-circle.btn-xl:hover {
    box-shadow: 0 0px 25px rgba(0, 0, 0, 0.8);
}

#buttons-row {
    margin: auto;
    text-align: center;
   
    left: 0;
    bottom: 0;
    width: 100%;
}
p {
    margin-left: 10px;
}
.img {
    object-fit: fill;
}


.flashcard:hover {
    box-shadow: 0 0px 25px rgba(0, 0, 0, 0.8);
}


.tag-chooser {
    margin-top: 5px;
    margin-left: 0px;
    max-height: 6.5em;
    overflow-y: auto;
}
#tags-bottom {
    margin: 50px 0px;
}

.tag-style-button {
    border-radius: 10px;
    margin: 5px 10px;
    border-width: 0px;
    color: black;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.51);

}
.green-btn {  background-color: rgba(185, 255, 184, 1)}
.white-btn {  background-color: white;}

</style>