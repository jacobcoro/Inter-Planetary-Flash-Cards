<template>
  <div class="deck-selection">
    <h3>Deck Selection</h3>
    <b-list-group>
    <b-list-group-item v-for="deckMeta in decksMeta" :key="deckMeta.edited">{{ deckMeta.title }}</b-list-group-item>
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
  }
}
</script>