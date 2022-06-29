import Vue from 'vue'
import VueRouter from 'vue-router'
import cent187 from '../views/cent187.vue'
import Home from "../components/Home";
import Login from '../views/Login.vue'
import iframeTest from '../views/iframeTest.vue'
import junitCase from '../views/junitCase.vue'

Vue.use(VueRouter)
const originalPush = VueRouter.prototype.push

VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

const routes = [
    {
        path: '/',
        name: 'index',
        redirect: {name: "Login"}
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/',
        name: 'Home',
        meta: {title: '主页', requireAuth: true},
        component: Home,
        children: [
            // {
            //     path: '/windows',
            //     name: 'windows',
            //     meta: {
            //         title: 'Windows环境',
            //     },
            //     component: windows
            // },
            // {
            //     path: '/linux',
            //     name: 'linux',
            //     meta: {
            //         title: 'Linux环境',
            //     },
            //     component: linux
            // },
            {
                path: '/cent187',
                name: 'cent187',
                meta: {
                    title: 'cent187环境',
                },
                component: cent187
            },
            // {
            //     path: '/junit',
            //     name: 'junitCase',
            //     meta: {
            //         title: 'junit',
            //     },
            //     component: junitCase
            // },
            {
                path: '/iframe',
                name: 'iframeTest',
                meta: {
                    title: 'iframe',
                },
                component: iframeTest
            },
        ]
    }

]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
