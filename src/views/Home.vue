<template>
    <b-container id="review-body">
        <b-row id="top-buttons-row" class="justify-content-end">
            <a class="edit"><font-awesome-icon @click="editCard(currentCard, reviewDeck)" size="1x" icon="edit"/></a>
        </b-row>
        <b-row id="card-row" class="" @click="flipCard()">
            <b-col class="card-col">
               <vue-flashcard
                id="main-card"
                :isToggle= "cardFlipToggle"
                :front="currentCard.front_text" 
                :back="currentCard.back_text"
                :imgFront="currentCard.front_image"
                :imgBack="currentCard.back_image"
                >
            </vue-flashcard>
            <div id="next-card-padding-outer">
                <div id="next-card-padding">
                    <vue-flashcard 
                        id="next-card"
                        :front="nextCard.front_text" 
                        :back="nextCard.back_text"
                        :imgFront="nextCard.front_image"
                        :imgBack="nextCard.back_image"
                        >
                    </vue-flashcard>
                </div>
            </div>
            <div id="third-card-padding-outer">
                <div id="third-card-padding">
                    <vue-flashcard 
                        id="third-card" class ="card"
                        front="   stuff   " 
                        back="     stuff   "
                        :imgFront="nextCard.front_image"
                        :imgBack="nextCard.back_image"> 
                    </vue-flashcard>
                </div>
            </div>
            </b-col>
        </b-row>
        <b-row id="buttons-row" >
            <b-col>
                <b-button v-if="cardFlipToggle === true" class="btn-circle btn-xl" @click="incorrect()">
                    <font-awesome-icon size="2x" icon="times"/>
                </b-button>
            </b-col>
            <b-col>    
                <b-button class="btn-circle btn-xl" @click="flipCard()">
                    <font-awesome-icon size="2x" icon="sync"/>
                </b-button>
            </b-col>
            <b-col>    
                <b-button v-if="cardFlipToggle === true" class="btn-circle btn-xl" @click="correct()">
                    <font-awesome-icon size="2x" icon="check"/>
                </b-button>
            </b-col>
        </b-row>  
    </b-container>  
</template>

<script>
import { mapState } from 'vuex'
import vueFlashcard from '../components/flashcard.vue';

export default {
    name: "home",
    data() {
        return {
            currentCardIndex: 0,
            cardFlipToggle: false,
            cardsCompleted: 0,
            cardsTotal: 0,
        }
    },
    computed: {
        ...mapState({
            reviewDeck: 'reviewDeck'
        }),
        currentCard () {
            return this.reviewDeck.cards[this.currentCardIndex]
        },
        nextCard () {
            return this.reviewDeck.cards[this.currentCardIndex + 1]
        },
    },
    methods: {
        flipCard () {
            this.cardFlipToggle=!this.cardFlipToggle
        },
        incorrect () {
            this.currentCardIndex ++
            this.cardFlipToggle = false
            this.NavbarProgess()

        },
        correct () {
            this.currentCardIndex ++
            this.cardFlipToggle = false
            this.cardsCompleted ++
            this.NavbarProgess()
        },
        NavbarProgess() {
            this.$store.dispatch('navProgress', this.cardsCompleted)
        },
        editCard(card, reviewDeck) {
            this.$store.commit('updateCardToEditIndex', reviewDeck.cards.indexOf(card))
            this.$router.push('/card-editor')
        }
    },
    created () {
        this.$store.dispatch('updateReviewDeck')
        this.$store.dispatch('navProgress', 0)
        this.$store.dispatch('refreshLastSyncsData')
        this.$store.commit('updateCurrentDeck', this.reviewDeck)
        this.currentCardIndex = 0
    },
    components: { vueFlashcard }
}
</script>

<style scoped>
.edit {
    color: gray;
    margin: 5px;
    right: 3px;
    z-index: 1;
    position: absolute;
}
.edit:hover{
    cursor: pointer;
}

#main-card {
    margin: auto;
    margin-top: 30px;
    max-width: 600px;
}
#next-card-padding-outer{
    z-index: -1;
    position: absolute;
    top: 0px;
    left: 0px;
    width: 100%;
}
#next-card-padding {
    width: 82%;
    margin: auto;
    z-index: -1;
}
#next-card {
    z-index: -1;
    margin: auto;
    margin-top: 20px;
    max-width: 480px;
}
#third-card-padding-outer{
    z-index: -2;
    position: absolute;
    top: 0px;
    left: 0px;
    width: 100%;
}
#third-card-padding {
    width: 70%;
    margin: auto ;
    z-index: -2;
}
#third-card {
    z-index: -2;
    margin: auto;
    margin-top: 10px;
    max-width: 380px;
    border-radius: 10px;
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
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.3)

}
</style>