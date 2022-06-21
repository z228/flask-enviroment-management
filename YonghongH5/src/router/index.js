import Vue from 'vue'
import VueRouter from 'vue-router'
import windows from '../views/windows.vue'
import iframeTest from '../views/iframeTest.vue'
import Home from "../components/Home";
import Login from '../views/Login.vue'
import log from '../views/log.vue'

Vue.use(VueRouter)

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
            {
                path: '/windows',
                name: 'windows',
                meta: {
                    title: 'Windows环境',
                },
                component: windows
            },
            {
                path: '/iframe',
                name: 'iframeTest',
                meta: {
                    title: 'iframe',
                },
                component: iframeTest
            },
            {
                path: '/log',
                name: 'log',
                meta: {
                    title: '日志查询',
                },
                component: log
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
