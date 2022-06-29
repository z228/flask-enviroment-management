import axios from 'axios'
import Element from 'element-ui'
import router from './router'
import store from './store'

// axios.defaults.baseURL = 'http://localhost:5000'
axios.interceptors.request.use(config => {
    return config;
})

axios.interceptors.response.use(response => {
        let res = response.data;

        console.log("==========");
        // console.log(res);
        if (store.state.userInfo === '' || store.state.userInfo === null) {
            router.push("/login")
        }
        if(res.code === 405)
        {
            store.commit("REMOVE_INFO")
            Element.Message.error(res.data, {duration: 3 * 1000});
            router.push("/login")
        }
        if (res.code === 200 || res.code === 205) {
            return response;
        } else {
            Element.Message.error(res.data, {duration: 3 * 1000});
            return Promise.reject(response.data.data);
        }
    },
    error => {
        console.log(error)
        if (error.response.data) {
            error.message = error.response.data.msg;
        }
        if (error.response.status === 401) {
            store.commit("REMOVE_INFO")
            router.push("/login")
        }
        Element.Message.error(error.message, {duration: 3 * 1000});
        return Promise.reject(error);
    }
)
