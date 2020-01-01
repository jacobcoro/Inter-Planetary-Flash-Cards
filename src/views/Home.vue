<template>
    <b-container id="review-body">
        <b-row id="top-buttons-row" class="justify-content-end">
            <a class="btn-gray"><font-awesome-icon @click="openCardEditor()" size="0.5x" icon="edit"/></a>
        </b-row>
        <b-row id="card-row" @click="flipCard()">
            <vue-flashcard 
                :isToggle= "cardFlipToggle"
                :front="currentCard.front_text" 
                :back="currentCard.back_text"
                :imgFront="currentCard.front_image"
                :imgBack="currentCard.back_image">
            </vue-flashcard>
        </b-row>
        <b-row id="buttons-row" >
            <b-col>
                <b-button class="btn-circle btn-xl" @click="incorrect()">
                    <font-awesome-icon size="2x" icon="times"/>
                </b-button>
            </b-col>
            <b-col>    
                <b-button class="btn-circle btn-xl" @click="flipCard()">
                    <font-awesome-icon size="2x" icon="sync"/>
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
import vueFlashcard from '../components/flashcard.vue';

export default {
    name: "home",
    data() {
        return {
            currentCardIndex: 0,
            cardFlipToggle: false
        };
    },
    computed: {
        ...mapState({
            reviewDeck: 'reviewDeck'
        }),
        currentCard () {
            return this.reviewDeck[this.currentCardIndex]
        },
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
        },
        correct () {
            this.currentCardIndex++
          this.cardFlipToggle = false
        }
    },
    created () {
        this.$store.dispatch('updateReviewDeck')
        this.currentCardIndex = 0
        // this.updateCurrentCard()
    },
    components: { vueFlashcard }
}
</script>

<style scoped>
/* still not centered*/

#review-body {
    max-width: 350px;
    margin: auto;
}
/* .btn-circle.btn-md { 
        width: 50px; 
        height: 50px; 
        padding: 7px 10px; 
        border-radius: 25px; 
   
        font-size: 10px; 
        text-align: center; 
    }  */
.btn-circle.btn-xl { 
    width: 70px; 
    height: 70px; 
    padding: 10px 16px; 
    margin: auto;
    border-radius: 35px; 
    font-size: 12px; 
    text-align: center; 
    color:grey;
    background-color: white;
    border: none
    } 
.btn-circle.btn-xl:hover {
    box-shadow: 0 0px 25px rgba(0, 0, 0, 0.8);
}
.btn-gray {
    color: gray
}
.btn-gray:hover{
    cursor: pointer;
  
}
.flash-card {
    text-align: center;
    padding-top: 15px;
    width: 350px; 
    height: 450px;
    margin: 10px; 
    box-shadow: 0px 0px 15px 5px rgba(0, 0, 0, 0.1);
}
#buttons-row {
    margin: auto;
    text-align: right;
}
</style>