<template>
  <div>
    <div class="iframe_card">
      <el-card >
        <iframe height="700px" width="1200px" src="http://192.168.0.187:88/#"></iframe>
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
  margin-top: 10px;
}
</style>