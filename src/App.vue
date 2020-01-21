<template>
    <div id="app">
            <Navbar id="navbar"/>
            <router-view/>
    </div>
</template>

<script>
import Navbar from './components/Navbar'
import { mapState } from 'vuex'
import _ from 'lodash';   

    export default {
        name: 'App',
        data() {
            return {
            }
        },
        mounted() {
           this.redirectIfAuth()
        },
        computed: {
            ...mapState({
                decks: 'decks',
                syncing: 'syncing'
            }),
        },
        watch: {
            decks: {
                handler: function() {
                    console.log('watched decks for syncing')
                    this.sync()
                },
                deep: true
            }, 
            syncing: function() {
                if (this.syncing === false) {
                    console.log('watched syncing for syncing')
                    this.sync()
                }
            }
        },
        methods: {
            sync: _.debounce(function(){
                 console.log('debounced sync')
                this.$store.dispatch('sync')  
            }, 60000),
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
        background-color: #F6F6F6;
        margin: 0;
        margin-top: 55px;
    }
    h1 {
        padding: 0;
        margin-top: 0;
    }
    #navbar {
    position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  z-index: 2000;
    }
</style>