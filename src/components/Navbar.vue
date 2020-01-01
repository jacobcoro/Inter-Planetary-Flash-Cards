<template>
<div id="body">
  <b-navbar toggleable="xs" variant="primary">
  <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
  <b-link to="#" ><font-awesome-icon style="color: white;" icon="search"/></b-link>     
  <b-nav-text style="color: white;" id="session-counter">{{ navProgressCounter }}</b-nav-text>    
  <b-link to="#"><img src="../assets/add card logo.svg" alt="add"></b-link>
  <b-link to="#" class="icon"><font-awesome-icon style="color: white;" icon="cloud"/></b-link>     
  <b-collapse  id="nav-collapse" is-nav>
    <b-navbar-nav >
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

    export default {
        name: 'deck-selection',
  data () {
    return {
    }
  },
  computed: {
   navProgressCounter () {
				return this.$store.getters.navProgressCounter
				}
  },  
    }
</script>

<style scoped>

</style>