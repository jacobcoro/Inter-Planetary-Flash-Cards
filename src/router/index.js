import Vue from 'vue'
import Router from 'vue-router'

import Login from "../views/Login.vue"
import Home from "../views/Home.vue"
import DeckSelection from "../views/DeckSelection.vue"
import QuizOptions from "../views/QuizOptions.vue"
import DeckEditor from "../views/DeckEditor.vue"
import Settings from "../views/Settings.vue"
import CardEditor from "../views/CardEditor.vue"

import store from "../store"

Vue.use(Router)

async function redirectIfNotAuth (to, from, next) {
    await store.dispatch('checkJwt')
    if (store.getters.isAuthenticated) {
      next()
    } else if (this.$router.path !== '/login') {
      next('/login')
    }
}



export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            redirect: {
                name: "login",
            }
        },
        {
            path: "/login",
            name: "login",
            component: Login,
        },
        {
            path: "/home",
            name: "home",
            component: Home,
            beforeEnter: redirectIfNotAuth
        },
        {
            path: "/deck-selection",
            name: "deck-selection",
            component: DeckSelection,
            beforeEnter: redirectIfNotAuth
        },
        {
            path: "/quiz-options",
            name: "quiz-options",
            component: QuizOptions,
            beforeEnter: redirectIfNotAuth
        },
        {
            path: "/deck-editor",
            name: "deck-editor",
            component: DeckEditor,
            beforeEnter: redirectIfNotAuth
        },
        {
            path: "/settings",
            name: "settings",
            component: Settings,
            beforeEnter: redirectIfNotAuth
        },
        {
            path: "/card-editor",
            name: "card-editor",
            component: CardEditor,
            beforeEnter: redirectIfNotAuth
        }
    ]
})