<template>
  <div>
    <div class="url_input all">
      <el-input v-model="form.url"></el-input>
    </div>
    <div class="all">
      <el-button type="primary" @click="jump">跳转</el-button>
    </div>
    <div class="iframe_card">
      <el-card >
        <iframe height="600px" width="1200px" :src="form.url"></iframe>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        url: "",
      },
    };
  },
  methods: {
    jump() {},
  },
};
</script>

<style scoped>
.url_input {
  width: 500px;
}
.all {
  margin: 10px;
  float: left;
}
.iframe_card {
  float: left;
  margin-top: 60px;
}
</style>