import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        token: localStorage.getItem("token"),
        userInfo: sessionStorage.getItem("userInfo")
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
