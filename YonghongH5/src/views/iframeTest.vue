<template>
  <div>
    <div class="url_input all">
      <el-input v-model="form.url"></el-input>
    </div>
    <div class="all">
      <el-button type="primary" @click="dialogVisible = true">跳转</el-button>
    </div>
    <div class="iframe_card">
      <el-card>
        <iframe id="db" height="700px" width="1400px" :src="form.url"></iframe>
      </el-card>
    </div>
    <el-dialog
      title="提示"
      :visible.sync="dialogVisible"
      width="600px"
      height="800px"
      :before-close="handleClose"
    >
      <div id="db1" style="height: 250px">
        <iframe height="100%" src="http://192.168.0.192:8094/bi/?proc=1&action=viewer&hback=true&db=111.db&platform=PC&browserType=chrome"></iframe>
      </div>
      <div id="db2" style="height: 250px">
        <iframe height="100%" src="http://192.168.0.192:8094/bi/?proc=1&action=viewer&hback=true&db=111.db&platform=PC&browserType=chrome"></iframe>
      </div>
      <div id="db3" style="height: 250px">
        <iframe height="100%" src="http://192.168.0.192:8094/bi/?proc=1&action=viewer&hback=true&db=111.db&platform=PC&browserType=chrome"></iframe>
      </div>
      <div id="db4" style="height: 250px">
        <iframe height="100%" src="http://192.168.0.192:8094/bi/?proc=1&action=viewer&hback=true&db=111.db&platform=PC&browserType=chrome"></iframe>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: this.$common.form,
      dialogVisible: false,
    };
  },
  methods: {
    jump() {
      window.location =
        "http://192.168.0.192:8094/bi?proc=1&action=viewer&export=excel&db=111";
    },
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