import Vue from 'vue'
import VueRouter from 'vue-router'
import cent187 from '../views/cent187.vue'
import Home from "../components/Home";
import Login from '../views/Login.vue'

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
            //     path: '/task',
            //     name: 'task',
            //     meta: {
            //         title: 'Windows定时任务',
            //     },
            //     component: task
            // },
        ]
    }

]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
