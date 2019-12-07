import Vue from 'vue'
import Router from 'vue-router'
import Login from "../views/Login.vue"
import DeckSelection from "../views/DeckSelection.vue"
import QuizOptions from "../views/QuizOptions.vue"
import DeckEditor from "../views/DeckEditor.vue"
import SelfSelectQuiz from "../views/SelfSelectQuiz.vue"
import store from "../store"

Vue.use(Router)

async function redirectIfNotAuth (to, from, next) {
    await store.dispatch('checkJwt')
    if (store.getters.isAuthenticated) {
      next()
    } else if (this.$router.path !== '/') {
      next('/')
    }
}

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            redirect: {
                name: "login"
            }
        },
        {
            path: "/login",
            name: "login",
            component: Login
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
            path: "/self-select-quiz",
            name: "self-select-quiz",
            component: SelfSelectQuiz,
            beforeEnter: redirectIfNotAuth
        }
    ]
})