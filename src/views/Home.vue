<template>
    <b-container id="review-body">
        <b-row id="top-buttons-row" class="justify-content-end">
            <a class="edit"><font-awesome-icon @click="openCardEditor()" size="1x" icon="edit"/></a>
        </b-row>
        <b-row id="card-row" class="" @click="flipCard()">
            <b-col class="card-col">
               <vue-flashcard 
                id="main-card"
                class ="card"
                :isToggle= "cardFlipToggle"
                :front="currentCard.front_text" 
                :back="currentCard.back_text"
                :imgFront="currentCard.front_image"
                :imgBack="currentCard.back_image"
                :height="mainCardHeight"
                :width="mainCardWidth">
            </vue-flashcard>
            <vue-flashcard 
                id="next-card"
                class ="card"
                :front="nextCard.front_text" 
                :back="nextCard.back_text"
                :imgFront="nextCard.front_image"
                :imgBack="nextCard.back_image"
                :height="nextCardHeight"
                :width="nextCardWidth">
            </vue-flashcard>
            <vue-flashcard 
                :height="thirdCardHeight"
                :width="thirdCardWidth"
                id="third-card" class ="card"> 
            </vue-flashcard>

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
            mainCardHeight: "70vh",
            mainCardWidth: "90vw",
            nextCardHeight:  "65vh",
            nextCardWidth:  "80vw",
            thirdCardHeight:  "55vh",
            thirdCardWidth:  "70vw",
            cardsCompleted: 0,
            cardsTotal: 0,
        };
    },
    computed: {
        ...mapState({
            reviewDeck: 'reviewDeck'
        }),
        currentCard () {
            return this.reviewDeck[this.currentCardIndex]
        },
        nextCard () {
            return this.reviewDeck[this.currentCardIndex + 1]
        }
    },
    methods: {
        // updateCurrentCard () {
        //     this.currentCard = this.reviewDeck[this.currentCardIndex]
        // },
        openCardEditor(){
            this.$router.push()
        },
        flipCard () {
            this.cardFlipToggle=!this.cardFlipToggle
        },
        incorrect () {
            this.currentCardIndex++
            this.cardFlipToggle = false
            this.NavbarProgess()

        },
        correct () {
            this.currentCardIndex++
            this.cardFlipToggle = false
            this.cardsCompleted ++
            this.NavbarProgess()
        },
        NavbarProgess() {
            this.$store.dispatch('NavProgress', this.cardsCompleted)
        }
    },
    created () {
        this.$store.dispatch('updateReviewDeck')
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
    z-index: -3;
    position: absolute;
}
.edit:hover{
    cursor: pointer;
}


#main-card {
    position: absolute;
    top: 35px;
    border-radius: 10px;

}
#next-card {
    z-index: -1;
    position: absolute;
    top: 25px;
    left: 9.5vw;
    border-radius: 10px;

}
#third-card {
    z-index: -2;
    position: absolute;
    top: 15px;
    left: 16vw;
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
}
</style>