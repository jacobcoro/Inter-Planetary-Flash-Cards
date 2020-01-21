<template>
    <b-container id="main">
        <b-row id="main-row">
            <b-col id="main-col">
                <b-row id="title-row">
                    <b-col id="icon-col" cols="2" class="align-self-center">
                        <div id="icon" :style="{ backgroundColor: deck.icon_color}" > 
                            <p id="deck-abrev"><strong>{{ getTitleAbrev(deck.title)}}</strong></p>
                        </div>
                    </b-col>
                    <b-col id="text-col">
                        <p v-if="!editingDeckTitle" class="text title" @click="toggleEditDeckTitle()" >{{ deck.title }}</p> 
                        <b-input v-if="editingDeckTitle"  @keyup.enter="commitDeckTitle()" v-model="newDeckTitle"></b-input> 
                        <p class="text card-count">
                        {{ deck.cards.length }} card{{cardOrCards(deck.cards.length)}}
                        </p>   
                        <div id="underline"></div>
                    </b-col>
               
          </b-row>
                <b-row id="cards-row">
                    <b-col cols="12" id="cards-col" style="padding: 0;">
                        <b-card id="card" v-for="card in deck.cards" :key="card.card_id">
                            <b-container style="padding: 0;">
                                <b-row >
                                    <b-col v-if="card.front_image" cols="5">
                                        <b-img-lazy v-if="card.front_image" :src="card.front_image"></b-img-lazy>
                                    </b-col>
                                    <b-col >
                                        <b-card-text class="font-weight-bold">{{ card.front_text }}</b-card-text>
                                    </b-col>
                                    <b-col cols="1">
                                        <font-awesome-icon icon="edit" class="edit" @click="editCard(card)"/>
                                    </b-col>
                                </b-row>
                                <hr class="divider">
                                <b-row >
                                    <b-col v-if="card.back_image">
                                        <b-img-lazy :src="card.back_image"></b-img-lazy>
                                    </b-col>
                                    <b-col>
                                        <b-card-text> {{ card.back_text }} </b-card-text>
                                    </b-col>
                                </b-row>
                            </b-container>
                        </b-card>
                    </b-col>
                </b-row >
            </b-col>
        </b-row>
       
    </b-container>
</template>

<script>
import { mapState } from 'vuex'
export default {
    name: 'deck-editor',
    data() {
        return {
            editingDeckTitle: false,
            newDeckTitle: ""
        };
    },
    computed: {
        ...mapState({
            deck: 'currentDeck'
        }),
    },
    methods: {
        toggleEditDeckTitle(){
            this.newDeckTitle = this.deck.title
            this.editingDeckTitle = !this.editingDeckTitle
        },
        commitDeckTitle() {
            this.deck.title = this.newDeckTitle
            this.deck.edited = Math.round(new Date().getTime() / 1000);
            this.$store.commit('updateDeck', this.deck)
            this.$store.dispatch('refreshDecksMeta')
            this.toggleEditDeckTitle()
        },
        editCard(card) {
            this.$store.commit('updateCardToEditIndex', this.deck.cards.indexOf(card))
            this.$router.push('/card-editor')
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
        }
    },
    created () {
        this.$store.commit('toggleNavNewCardDisabled', false)
    }
}
</script>

<style scoped>
#card {
    max-width: 600px;
    margin: 10px auto;
    box-shadow: 0px 0px 15px 5px
    rgba(0, 0, 0, 0.1);
}
.edit {
    color: gray;
}
.edit:hover{
    cursor: pointer;
    color: black;

}
#main{
  padding: 15px 15px 0px 10px;
}

#main-col {
    margin: auto;
    max-width: 600px;
    width: 100%;
    padding: 0;
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

</style>