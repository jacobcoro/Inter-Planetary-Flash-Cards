<template>
  <div class="deck-selection">
    <b-container fluid>
      <h3 style="margin-left: 20px;">Deck Selection</h3>
    <b-list-group>
    <b-list-group-item v-for="deckMeta in decksMeta" :key="deckMeta.edited" button @click="openDeck(deckMeta.deck_id)">{{ deckMeta.title }}</b-list-group-item>
    </b-list-group>
    </b-container>
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
    }
  },
  created () {
    this.$store.dispatch('refreshDecksMeta')
  }
}
</script>