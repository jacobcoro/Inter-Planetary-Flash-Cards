<template>
    <b-container fluid id="body">
      <b-container class="card">
        <b-row >
            <b-col v-if="card.front_image">
                <b-img-lazy class="img" v-if="card.front_image" :src="card.front_image"></b-img-lazy>
            </b-col>
            <b-col >
                <b-card-text class="font-weight-bold">{{ card.front_text }}</b-card-text>
            </b-col>
        </b-row>
      </b-container>
      <b-container class="card">
        <b-row >
          <b-col v-if="card.back_image">
              <b-img-lazy class="img" :src="card.back_image"></b-img-lazy>
          </b-col>
          <b-col>
              <b-card-text> {{ card.back_text }} </b-card-text>
          </b-col>
        </b-row>
      </b-container>
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
export default {
    name: 'card-editor',
    data() {
        return {
            
        };
    },
    computed: {
        ...mapState({
            card: 'cardToEdit',
            deck: 'cardToEditsDeck'
        })
    }  
}
</script>

<style scoped>
.card {
    margin: 30px auto;
    top: 35px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 1.5em;
    padding: 25px;
    box-shadow: 0 0px 10px rgba(41, 33, 33, 0.4);
    text-align: left;
    overflow-y: auto;
    width: 90vw;
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
.img {
    object-fit: fill;
}


.flashcard:hover {
    box-shadow: 0 0px 25px rgba(0, 0, 0, 0.8);
}
</style>