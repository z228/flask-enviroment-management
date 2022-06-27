<template>
  <div class="login-main">
    <el-container>
      <el-header class="">
        <img
            class="m-logo"
            src="../assets/img/bk.gif"
            alt=""
        />
      </el-header>
      <el-main>
        <div class="ms-login">
          <div class="ms-title editBan">Debug环境管理系统</div>
          <el-form
              :model="ruleForm"
              :rules="rules"
              ref="ruleForm"
              label-width="0px"
              class="ms-content"
          >
            <el-form-item prop="username">
              <el-input v-model="ruleForm.userName" placeholder="username">
                <template #prepend>
                  <el-button icon="el-icon-user"></el-button>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                  type="password"
                  placeholder="password"
                  v-model="ruleForm.password"
                  @keyup.enter="submitForm()"
              >
                <template #prepend>
                  <el-button icon="el-icon-lock"></el-button>
                </template>
              </el-input>
            </el-form-item>
            <div class="login-btn">
              <el-form-item>
                <el-button type="primary" @click="submitForm()">登录</el-button>
              </el-form-item>
            </div>
            <p class="login-tips">Tips :无账户密码请联系管理员</p>
          </el-form>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: "Login.vue",
  data() {
    return {
      ruleForm: {
        userName: "",
        password: "",
      },
      rules: {
        userName: [
          {required: true, message: "请输入用户名", trigger: "blur"},
          {
            min: 3,
            max: 15,
            message: "长度在 3 到 15 个字符",
            trigger: "change",
          },
        ],
        password: [
          {required: true, message: "请输入密码", trigger: "change"},
        ],
      },
    };
  },
  methods: {
    submitForm() {
      this.$refs.ruleForm.validate((valid) => {
        if (valid) {
          const _this = this;
          this.$axios
              .post("http://192.168.0.192:5000/productJar/login", {
                username: this.ruleForm.username,
                password: this.ruleForm.password,
              })
              .then((res) => {
                if (res.data.code === 200) {
                  this.$message({
                    message: res.data.data,
                    duration: 3000,
                    showClose: true,
                    type: "success",
                  });
                  this.$store.commit("SET_USERINFO", this.ruleForm.username);
                  _this.$router.push("/windows");
                } else if (res.data.code === 205) {
                  this.$message({
                    message: res.data.data,
                    duration: 3000,
                    showClose: true,
                    type: "error",
                  });
                }
              })
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
  },
  created() {
    const _this = this;
    let jwt = this.$store.state.token;
    if (_this.$store.state.userInfo !== null) {
      if (this.$store.state.userInfo === 'admin' || this.$store.state.userInfo === '曾成龙')
        _this.$router.push("/cent187");
      else {
        if (this.$store.state.userInfo === '')
          console.log("未登录");
        else
          _this.$router.push("/cent187");
      }
    } else {
      if (_this.$store.state.userInfo === null) {
        console.log("登录已过期");
      } else {
      }
    }
  },
};
</script>

<style scoped>
.editBan {
  -moz-user-select: none; /*火狐*/
  -webkit-user-select: none; /*webkit浏览器*/
  -ms-user-select: none; /*IE10*/
  -khtml-user-select: none; /*早期浏览器*/
  -o-user-select: none; /* Opera*/
}

.el-header {
  /*background-color: #B3C0D1;*/
  background-color: rgba(155, 155, 155, 0.6);
  position: relative;
  color: #333;
  text-align: center;
  line-height: 40px;
  height: 200px;
}

.el-main {
  height: 100%;
}

.login-main {
  position: relative;
  width: 100%;
  height: 100%;
  background-image: url(../assets/img/login-bg.jpg);
  background-size: 100% 100%;
  background-repeat: no-repeat;

  margin: 0;
  padding: 0;
}

.m-logo {
  height: 100%;
  /*margin-top: 10px;*/
}

.ms-title {
  width: 100%;
  line-height: 50px;
  text-align: center;
  font-size: 20px;
  color: #183a65;
  border-bottom: 1px solid #ddd;
}

.ms-login {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 350px;
  margin: -190px 0 0 -175px;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.3);
  overflow: hidden;
}

.ms-content {
  padding: 30px 30px;
}

.login-btn {
  text-align: center;
}

.login-btn button {
  width: 100%;
  height: 36px;
  margin-bottom: 10px;
}

.login-tips {
  text-align: left;
  font-size: 12px;
  line-height: 30px;
  color: #183a65;
  margin: 0;
}
</style>