<template>
    <div id="app">
            <Navbar id="navbar"/>
            <router-view/>
    </div>
</template>

<script>
import Navbar from './components/Navbar'
    export default {
        name: 'App',
        data() {
            return {
            }
        },
        mounted() {
           this.redirectIfAuth()
        },
        methods: {
            async redirectIfAuth () {
                await this.$store.dispatch('checkJwt')
                if (this.$store.getters.isAuthenticated) {
                    // but upon entry we'll need to query decks metadata and make sure we aren't missing updates
                    // if there's no internet, post the unsynced data warning AND a special login without sync warning.
                    this.$router.push('/home')
                }
            }
        },
        components: {
            Navbar
        }
    }
</script>

<style lang="scss">

  @import "assets/_custom.scss";
  @import "~bootstrap/scss/bootstrap.scss";
  @import '~bootstrap-vue/dist/bootstrap-vue.css';

    body {
        background-color: #F0F0F0;
        margin: 0;
    }
    h1 {
        padding: 0;
        margin-top: 0;
    }
    #navbar {
    position: sticky;
  top: 0;
  right: 0;
  width: 100%;
  z-index: 1000;
    }
</style>