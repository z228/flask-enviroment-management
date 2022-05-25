import Vue from 'vue'
import VueRouter from 'vue-router'
import cent185 from '../views/cent185.vue'
import Home from "../components/Home";
import Login from '../views/Login.vue'

Vue.use(VueRouter)

const routes = [
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
                path: '/cent185',
                name: 'cent185',
                meta: {
                    title: 'cent185环境',
                },
                component: cent185
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
