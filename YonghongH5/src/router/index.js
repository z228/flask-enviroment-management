import Vue from 'vue'
import VueRouter from 'vue-router'
import windows from '../views/windows.vue'
import cent185 from '../views/cent185.vue'
import cent187 from '../views/cent187.vue'
import task from '../views/task.vue'
import iframeTest from '../views/iframeTest.vue'
import Home from "../components/Home";
import linux from "../views/linux";
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
                path: '/linux',
                name: 'linux',
                meta: {
                    title: 'Linux环境',
                },
                component: linux
            },
            {
                path: '/cent185',
                name: 'cent185',
                meta: {
                    title: 'cent185环境',
                },
                component: cent185
            },
            {
                path: '/cent187',
                name: 'cent187',
                meta: {
                    title: 'cent187环境',
                },
                component: cent187
            },
            {
                path: '/task',
                name: 'task',
                meta: {
                    title: 'Windows定时任务',
                },
                component: task
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