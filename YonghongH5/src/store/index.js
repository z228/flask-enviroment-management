import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        token: localStorage.getItem("token"),
        userInfo: sessionStorage.getItem("userInfo"),
        username: sessionStorage.getItem("username")
    },
    mutations: {
        //set
        SET_TOKEN: (state, token) => {
            state.token = token
            localStorage.setItem("token", token)
        },
        SET_USERINFO: (state, userInfo) => {
            state.userInfo = userInfo
            sessionStorage.setItem("userInfo", userInfo)
        },
        SET_USERNAME: (state, username) => {
            state.username = username
            sessionStorage.setItem("username", username)
        },
        REMOVE_INFO: (state) => {
            state.token = ''
            state.userInfo = ''
            localStorage.setItem("token", '')
            sessionStorage.setItem("userInfo", '')
        }
    },
    getters: {
        getUser: (state) => {
            return this.state.userInfo
        }
    },
    actions: {},
    modules: {}
})
