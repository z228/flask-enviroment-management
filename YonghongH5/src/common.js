import Vue from 'vue'
// 全局变量
const globalObj = {};

// 定义公共变量
globalObj.name = '小明';
globalObj.college = [];
globalObj.status = {
    hasFoundSingle: false,
    hasFoundMany: false,
    isEdit: false,
    ifEdit: false,
    add: false,
    search: false,
    update: false,
    delete: false,
    loading: true,
    student: false
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
globalObj.changeListKeyValue = function (arr,version,key,value) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i].version === version){
            Vue.set(arr[i], key, value);
          break
        }
      }
}
globalObj.formatDateStr = (str => {
      return (
          str.substring(0, 4) +
          "-" +
          str.substring(4, 6) +
          "-" +
          str.substring(6, 8)
      );
    });


export default globalObj
