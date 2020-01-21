<template>
<div id="body">
  <b-navbar toggleable="xs" type="dark" variant="primary">
  <b-navbar-toggle  target="nav-collapse"></b-navbar-toggle>
  <b-link to="#" ><font-awesome-icon style="color: white;" icon="search"/></b-link>     
  <b-nav-text style="color: white;" id="session-counter">{{ navProgressCounter }}</b-nav-text>    
  <b-link @click="newCard()" :disabled="navNewCardDisabled" ><img src="../assets/add card logo.svg" alt="add"></b-link>
  <b-link to="#" class="icon"><font-awesome-icon style="color: white;" icon="cloud"/></b-link>     
  <b-collapse id="nav-collapse" is-nav>
    <b-navbar-nav  >
    <b-nav-item to="/home">Review</b-nav-item>
    <b-nav-item to="/Settings">Settings</b-nav-item>
    <b-nav-item to="/deck-selection">Decks</b-nav-item>
    <b-nav-item to="#" disabled>Lessons</b-nav-item>
    <b-nav-item to="#" disabled>Classes</b-nav-item>
    <b-nav-form>
    <b-form-input size="sm" class="mr-sm-1" placeholder="find decks and classes"></b-form-input>
      <b-button size="sm" type="submit">Search</b-button>
    </b-nav-form>   
    </b-navbar-nav> 
  </b-collapse> 
</b-navbar>  
</div>
</template>

<script>
const uuidv4 = require('uuid/v4');

import { mapState } from 'vuex'
export default {
  name: 'navbar',
  data () {
    return {
    }
  },
  computed: {
    navProgressCounter () {
				return this.$store.getters.navProgressCounter
				},
    ...mapState({
            currentDeck: 'currentDeck',
            navNewCardDisabled: 'navNewCardDisabled'
        }),
  },
  methods: {
    newCard() {
      this.$store.dispatch('navNewCardClicked')
      let newCard = {
          back_text:"",
          card_id: uuidv4(),
          card_tags: ["Daily Review"],
          front_text: ""
      }
            //.cards
      this.currentDeck.cards.push(newCard)
      // if coming from the home screen, it won't have a current deck. we want to make a new card, but not assigned to any deck yet
      this.$store.commit('updateCardToEditIndex', this.currentDeck.cards.length -1)
      if (this.$route.name !== 'card-editor' ) {
        this.$router.push('/card-editor')
      }
        
    }
  }  
    }
</script>

<style scoped>

</style>