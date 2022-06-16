import Vue from 'vue'
// 全局变量
const globalObj = {};

// 定义公共变量
globalObj.name = '小明';
globalObj.form= {
    url: "http://192.168.0.187:8080/bi?proc=0&action=index",
  };
globalObj.college = [];
globalObj.status = {

}
globalObj.userInfo = {
    roles: "",
    permission: [],
    id: null,
    userName: ""
}
globalObj.graduatesInfoTemp = {}
globalObj.employmentInfoTemp = {}
globalObj.archivesInfoTemp = {}


// 定义公共方法
globalObj.isObjectValueEqual = function (a, b) {
    let aProps = Object.getOwnPropertyNames(a);
    let bProps = Object.getOwnPropertyNames(b);

    if (aProps.length !== bProps.length) {
        return false;
    }

    for (let i = 0; i < aProps.length; i++) {
        let propName = aProps[i];
        if (propName==='__ob__'){
            continue
        }
        if (a[propName] !== b[propName]) {
            return false;
        }
    }
    return true;
};
globalObj.objectValueAtoB = function (a, b) {
    let aProps = Object.keys(a);
    for (let i = 0; i < aProps.length; i++) {
        let propName = aProps[i];
        Vue.set(b, propName, a[propName]);
    }
}
globalObj.resetObject = function (a) {
    for (let i in a) {
        a[i] = null
    }
}
export default globalObj
