<template>
  <div>
    <div class="iframe_card">
      <el-card>
        <el-form ref="userinfo" :model="userinfo" label-width="80px" >
          <el-form-item label="用户名" class="inputForm" prop="username">
            <el-input v-model="userinfo.username" class="inputForm" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="passwd">
            <el-input v-model="userinfo.password" class="inputForm"></el-input>
          </el-form-item>
          <el-form-item label="别名" prop="alias">
            <el-input v-model="userinfo.alias" class="inputForm"></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="userinfo.email" class="inputForm"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="updateUserinfo">修改信息</el-button>
<!--            <el-button>取消</el-button>-->
          </el-form-item>
        </el-form>

      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userinfo: {
        userId:null,
        username: "",
        password: "",
        alias: "",
        email: ""
      },
      // rules: {
      //     username: [
      //       { validator: validatePass, trigger: 'blur' }
      //     ],
      //     passwd: [
      //       { validator: validatePass2, trigger: 'blur' }
      //     ],
      //     alias: [
      //       { validator: checkAge, trigger: 'blur' }
      //     ],
      //     email: [
      //       { validator: checkAge, trigger: 'blur' }
      //     ]
      //   }
    }
        ;
  },
  created() {
    this.getUserinfo()
  },
  methods: {
    getUserinfo() {
      this.$axios
          .post("http://192.168.0.187:5000/productJar/getuserinfo", {
            username: this.$store.state.username,
          })
          .then((res) => {
            let info = res.data.data
            if (res.data.code === 200) {
              this.userinfo.userId = info.id
              this.userinfo.username = info.username
              this.userinfo.password = info.password
              this.userinfo.alias = info.alias
              this.userinfo.email = info.email
            }
          })
    },
    updateUserinfo() {
      this.$axios
          .post("http://192.168.0.187:5000/productJar/updateuserinfo", {
            userId:this.userinfo.userId,
            username: this.userinfo.username,
            password: this.userinfo.password,
            alias: this.userinfo.alias,
            email: this.userinfo.email,
          })
          .then((res) => {
            let info = res.data.data
            if (res.data.code === 200) {
              this.$message({
                message: info,
                duration: 10 * 1000,
                showClose: true,
                type: "success",
              });
            } else {
                this.$message({
                  message: info,
                  duration: 10 * 1000,
                  showClose: true,
                  type: "info",
                });
            }
          })
    },
    deleteUser() {
      this.$axios
          .post("http://192.168.0.187:5000/productJar/updateuserinfo", {
            username: this.userinfo.username,
            password: this.userinfo.password,
            alias: this.userinfo.alias,
            email: this.userinfo.email,
          })
          .then((res) => {
            let info = res.data.data
            if (res.data.code === 200) {
              this.$message({
                message: info,
                duration: 10 * 1000,
                showClose: true,
                type: "success",
              });
            } else {
              if (res.data.code === 200) {
                this.$message({
                  message: info,
                  duration: 10 * 1000,
                  showClose: true,
                  type: "info",
                });
              }
            }
          })
    }
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

.inputForm {
  width: 300px;
}
</style>