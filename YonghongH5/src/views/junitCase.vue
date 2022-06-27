<template>
  <div>
    <div class="url_input all">
      <el-input v-model="form.url"></el-input>
    </div>
    <div class="all">
      <el-button type="primary" @click="jump">跳转</el-button>
    </div>
    <div class="iframe_card">
      <el-card>
        <iframe height="700px" width="1400px" :src="form.junitUrl"></iframe>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: this.$common.form,
    };
  },
  mounted() {
    var testSuite = document
      .getElementsByTagName("h3")[0]
      .getInnerHTML()
      .split(" ")[1]
      .split(".")[0];
    console.log(testSuite);
    var failureCases = document.getElementsByClassName("Failure");
    var replaceBtn = document.createElement("input");
    replaceBtn.type = "button";
    replaceBtn.id = "rwl-setbtn";
    replaceBtn.value = "替换勾选case";
    failureCases[0].getElementsByTagName("td")[0].appendChild(replaceBtn);
    document.getElementById("rwl-setbtn").addEventListener("click", replaceRes);
    for (let i = 1; i < failureCases.length; i++) {
      // console.log(failureCases[i])
      let caseName = failureCases[i].getElementsByTagName("td")[0];
      //<input type="checkbox" id="modules_DataMart">
      var input = document.createElement("input");
      input.type = "checkbox";
      input.id = caseName.getInnerHTML();
      caseName.appendChild(input);
    }
  },
  methods: {
    replaceRes() {
      var caseList = {};
      caseList[testSuite] = [];
      caseList["version"] = version;
      let inputs = document.getElementsByTagName("input");
      for (var i = 0; i < inputs.length; i++) {
        var obj = inputs[i];
        //判断是否是checkbox并且已经选中
        if (obj.type == "checkbox" && obj.checked) {
          caseList[testSuite].push(obj.id);
        }
      }
      console.log(caseList);
    },
    jump() {},
  },
};
</script>

<style scoped>
.url_input {
  width: 600px;
}
.all {
  margin: 10px;
  float: left;
}
.iframe_card {
  float: left;
  margin-top: 10px;
}
</style>