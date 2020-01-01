<template>
    <b-container fluid id="body">
        <b-row >
        <h3 style="margin-left: 30px; margin-top: 10px;" >{{ deck.title }}</h3>
        </b-row >
        <b-row align-h="start">
        <b-col cols="11">
        <b-card 
        v-for="card in deck.cards" :key="card.card_id"
        style="max-width: 400px; margin: 10px; box-shadow: 0px 0px 15px 5px rgba(0, 0, 0, 0.1);">
            <b-container>
            <b-row >
                <b-col v-if="card.front_image" cols="5">
                    <b-img-lazy v-if="card.front_image" :src="card.front_image"></b-img-lazy>
                </b-col>
                <b-col >
                    <b-card-text class="font-weight-bold">{{ card.front_text }}</b-card-text>
                </b-col>
                <b-col cols="1">
                    <font-awesome-icon icon="edit" />
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
    </b-container>
</template>

<script>
import { mapState } from 'vuex'
export default {
    name: 'deck-editor',
    data() {
        return {
            
        };
    },
    computed: {
        ...mapState({
            deck: 'currentDeck'
        })
    }  
}
</script>

<style scoped>
</style>