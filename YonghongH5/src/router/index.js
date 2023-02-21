import Vue from "vue"
import VueRouter from "vue-router"
import windows from "../views/windows.vue"
import cent185 from "../views/cent185.vue"
import cent187 from "../views/cent187.vue"
import mac188 from "../views/mac188.vue"
import win172 from "../views/win172.vue"
import task from "../views/task.vue"
import iframeTest from "../views/iframeTest.vue"
import serverstatus from "../views/serverstatus.vue"
import Home from "../components/Home"
import linux from "../views/linux"
import Login from "../views/Login.vue"
import log from "../views/log.vue"

Vue.use(VueRouter)
const originalPush = VueRouter.prototype.push

VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch((err) => err)
}

const routes = [
  {
    path: "/",
    name: "index",
    redirect: { name: "Login" },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/",
    name: "Home",
    meta: { title: "主页", requireAuth: true },
    component: Home,
    children: [
      {
        path: "/windows",
        name: "windows",
        meta: {
          title: "Windows环境",
        },
        component: windows,
      },
      {
        path: "/linux",
        name: "linux",
        meta: {
          title: "Linux环境",
        },
        component: linux,
      },
      {
        path: "/cent185",
        name: "cent185",
        meta: {
          title: "cent185环境",
        },
        component: cent185,
      },
      {
        path: "/cent187",
        name: "cent187",
        meta: {
          title: "cent187环境",
        },
        component: cent187,
      },
      {
        path: "/win172",
        name: "win172",
        meta: {
          title: "北京win172",
        },
        component: win172,
      },
      {
        path: "/mac188",
        name: "mac188",
        meta: {
          title: "mac188环境",
        },
        component: mac188,
      },
      {
        path: "/task",
        name: "task",
        meta: {
          title: "Windows定时任务",
        },
        component: task,
      },
      {
        path: "/iframe",
        name: "iframeTest",
        meta: {
          title: "iframe",
        },
        component: iframeTest,
      },
      {
        path: "/serverstatus",
        name: "serverstatus",
        meta: {
          title: "serverstatus",
        },
        component: serverstatus,
      },
      {
        path: "/log",
        name: "log",
        meta: {
          title: "日志查询",
        },
        component: log,
      },
    ],
  },
]

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
})

export default router
