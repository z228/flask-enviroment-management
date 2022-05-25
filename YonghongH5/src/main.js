import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Element from 'element-ui'
import "element-ui/lib/theme-chalk/index.css"
import axios from 'axios'
import "./axios"
import './assets/css/global.css'
import './assets/iconfont/iconfont.css'
import './assets/iconfont/iconfont'
import common from './common'   // 引入全局文件common.js

// 引入jshint用于实现js自动补全提示 
import jshint from "jshint";
window.JSHINT = jshint.JSHINT;

// 引入代码编辑器 
import { codemirror } from "vue-codemirror";
import "codemirror/lib/codemirror.css";

Vue.config.productionTip = false
Vue.use(codemirror);
Vue.use(Element)
Vue.prototype.$axios = axios //
Vue.prototype.$common = common;


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
