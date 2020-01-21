<template>
  <div id="main">
      <!-- <h3>Decks</h3> -->
    <b-list-group >
    <b-list-group-item id="list-group-item" v-for="deckMeta in decksMeta" :key="deckMeta.deck_id" > 
      <b-container id="list-group-item-container">
        <b-row id="list-group-item-row">
         <b-col id="icon-col" cols="1" class="align-self-center">
           <div id="icon" :style="{ backgroundColor: deckMeta.icon_color}" > 
             <p id="deck-abrev"><strong>{{ getTitleAbrev(deckMeta.title)}}</strong></p>
           </div>
         </b-col>
         <b-col id="text-and-edit-col" cols="11">
          <b-row>
            <b-col id="text-col" @click="openDeck(deckMeta.deck_id)">
              <p class="text title" >{{ deckMeta.title }}</p> 
              <p class="text card-count">
                {{ deckMeta.deck_length }} card{{cardOrCards(deckMeta.deck_length)}}
              </p>     
            </b-col>
            <b-col id="edit-col" cols="1">
               <b-dropdown class="deck-options" dropleft size="lg" left variant= "link" 
                toggle-class="text-decoration-none" no-caret>
                <template v-slot:button-content>
                  <font-awesome-icon class="deck-options" color="grey" 
                  size="1x" icon="ellipsis-h"/> 
                  <span class="sr-only">Search</span>
                </template>
                <b-dropdown-item-button @click="deleteDeck(deckMeta.deck_id)">Delete</b-dropdown-item-button>
                <b-dropdown-item-button disabled href="#">Export</b-dropdown-item-button>
              </b-dropdown>
            </b-col>
          </b-row>
          <b-row>
            <div id="underline"></div>
          </b-row>
         </b-col>
       </b-row>
     </b-container>
  </b-list-group-item>
    </b-list-group>
    </div>
</template>


<script>
import { mapState } from 'vuex'
export default {
  name: 'deck-selection',
  data () {
    return {
    }
  },
  computed: {
    ...mapState([
      'decksMeta'
    ])
  },  
  methods: {
    openDeck (id) {
      var deck
      for (deck of this.$store.getters.getDecks) {
        if (deck.deck_id === id) {
          this.$store.commit('updateCurrentDeck', deck)
        }
      }
      this.$router.push('/deck-editor')
    },
    cardOrCards (deckLength) {
      if (deckLength === 1) {
        return ""
      } else {
        return "s"
      }
    },
    getTitleAbrev(title) {
        // There shouldn't be any empty title decks, but we can leave this validation here just in case
      if (title === "") {
        return ""
      } else {
        let split = title.split(" ")[0]
        let abrev
        if (split.length === 1) {
          abrev = split[0].charAt(0) + split[0].charAt(1)
        } else {
          abrev = split[0].charAt(0) + split[1].charAt(0)
        }
        return abrev
      }
    },
    deleteDeck(id) {
      let decks = this.$store.state.decks
      let updatedDecks = decks.filter(function (deckToCheck) {
          return deckToCheck.deck_id !== id
          }) 
      this.$store.commit('updateDecks', updatedDecks)
      this.$store.dispatch('refreshDecksMeta')
    }
  },
  created () {
    this.$store.dispatch('refreshDecksMeta')
    this.$store.commit('toggleNavNewCardDisabled', false)
  }
}
</script>
<style scoped>
#main{
  padding: 15px 15px 0px 10px;
}

#list-group-item{
  margin: auto;
  margin-bottom: 5px;
  padding: 0px;
  background-color: transparent;
  max-width: 600px;
  border: transparent;
  width: 100%;
}
#text-col{
  padding: 0px 0px 10px 20px ;
}
#underline{
  position: absolute;
  bottom: 0px;
  left: 20px;
  height: 1px;
  width: 75%;
  background-color: rgba(0, 0, 0, 0.5);
}
#edit-col{
  padding: 0;
  margin: auto;
  width: 10px;
}
#icon-col{
  width: 50px;
  padding: 0px; 
  height: 50px;
}
#icon:hover{
  cursor: pointer;
}
#icon{
  width: 46px;
  height: 46px;
  border-radius: 23px;
  text-align: center;
  font-size: 28px;
  padding-top: 1px;
  color: white;
  margin: auto;
}
#deck-abrev{
  margin: 0;
}
.text{
  padding: 0px 0px 0px 10px;
  margin: 0px
}
.text:hover{
  cursor: pointer;
}
.card-count{
  font-size: .8em;
  color: dimgray;
}
.title{
  font-size: 1.2em;
}
.deck-options-button{
  padding: 0;
}
.deck-options:hover{
  color: black;
  padding: 0;
}
</style>