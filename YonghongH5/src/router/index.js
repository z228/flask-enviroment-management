import Vue from "vue"
import VueRouter from "vue-router"
import cent187 from "../views/cent187.vue"
import cent185 from "../views/cent185.vue"
import mac188 from "../views/mac188.vue"
import Home from "../components/Home.vue"
import Login from "../views/Login.vue"
import iframeTest from "../views/iframeTest.vue"
import serverstatus from "../views/serverstatus.vue"
import junitCase from "../views/junitCase.vue"
import userinfo from "../views/userinfo.vue"
import userManage from "../views/userManage.vue"
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
        path: "/cent187",
        name: "cent187",
        meta: {
          title: "cent187环境",
        },
        component: cent187,
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
        path: "/mac188",
        name: "mac188",
        meta: {
          title: "mac188环境",
        },
        component: mac188,
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
        path: "/junit",
        name: "junitCase",
        meta: {
          title: "junit",
        },
        component: junitCase,
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
        path: "/userinfo",
        name: "userinfo",
        meta: {
          title: "用户信息",
        },
        component: userinfo,
      },
      {
        path: "/log",
        name: "log",
        meta: {
          title: "日志查询",
        },
        component: log,
      },
      {
        path: "/usermanage",
        name: "userManage",
        meta: {
          title: "用户管理",
        },
        component: userManage,
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
