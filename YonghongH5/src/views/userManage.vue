<template>
  <div id="iframe_card" v-if="this.$store.state.username === 'admin' || this.$store.state.username === 'zcl'">
    <el-card>
      <el-button
          type="primary"
          size="mini"
          @click="addUserBtn()"
          style="margin-bottom: 5px"
      >添加用户
      </el-button
      >
      <el-table :data="users" border stripe style="width: 100%">
        <el-table-column prop="username" label="用户名" width="180">
        </el-table-column>
        <el-table-column prop="alias" label="别名" width="400">
          <template slot-scope="scope" v-if="scope.row.alias !== '' && scope.row.alias != null">
            <el-tag
                v-for="alia in scope.row.alias.split(/[,\s]/)"
                :key="alia"
                type="success"
                style="margin: 2px"
            >
              {{ alia }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱">
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <el-button
                type="text"
                size="small"
                @click="editUserInfo(scope.row)"
            >编辑
            </el-button
            >
            <el-button
                @click="deleteUser(scope.row, scope.$index)"
                type="text"
                size="small"
                style="color: red"
            >删除
            </el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <el-dialog
          title="编辑用户信息"
          :visible="isEdit || isAddUser"
          width="500px"
          :before-close="editUserInfoClose"
          :close-on-click-modal="false">
        <el-form ref="userInfoTemp" :inline="true" label-width="80px" :model="userInfoTemp">
          <el-form-item label="用户名" prop="username">
            <el-input
                class="infoInput"
                v-model="userInfoTemp.username"
            ></el-input>
          </el-form-item>
          <el-form-item label="别名">
            <el-input
                class="infoInput"
                v-model="userInfoTemp.alias"
            ></el-input>
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input
                class="infoInput"
                v-model="userInfoTemp.email"
            ></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
                class="infoInput"
                v-model="userInfoTemp.password"
            ></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="editUserInfoClose()">取 消</el-button>
          <el-button
              type="primary"
              @click="isEdit ? updateUserInfo() : addUser()">确 定
          </el-button>
        </div>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isEdit: false,
      isAddUser: false,
      users: [],
      userInfoTemp: {
        alias: null,
        username: null,
        email: null,
        password: null
      },
    };
  },
  created() {
    this.getAllUserinfo();
  },
  methods: {
    editUserInfoClose() {
      this.isEdit = false
      this.isAddUser = false
      this.$common.resetObject(this.userInfoTemp)
    },
    editUserInfo(user) {
      this.isEdit = true
      this.$common.objectValueAtoB(user, this.userInfoTemp);
    },
    addUserBtn() {
      this.isAddUser = true
      // this.$common.objectValueAtoB(user, this.userInfoTemp);
    },
    addUser() {
      if (this.userInfoTemp.alias !== null)
        this.userInfoTemp.alias = this.userInfoTemp.alias.replace(/[,;\s]+/g, " ").trim();
      this.$axios
          .post("http://192.168.0.187:5000/productJar/adduser", this.userInfoTemp)
          .then((res) => {
            let info = res.data.data;
            if (res.data.code === 200) {
              this.getAllUserinfo();
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
          });
      this.editUserInfoClose();
    },
    updateUserInfo() {
      if (this.userInfoTemp.alias !== null)
        this.userInfoTemp.alias = this.userInfoTemp.alias.replace(/[,;\s]+/g, " ").trim();
      this.$axios
          .post(
              "http://192.168.0.187:5000/productJar/updateuserinfo",
              this.userInfoTemp
          )
          .then((res) => {
            let info = res.data.data;
            if (res.data.code === 200) {
              this.getAllUserinfo();
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
          });
      this.editUserInfoClose();
    },
    getAllUserinfo() {
      this.users.length = 0;
      this.$common.resetObject(this.users)
      this.$axios
          .get("http://192.168.0.187:5000/productJar/alluserinfo")
          .then((res) => {
            let info = res.data.data;
            if (res.data.code === 200) {
              this.$common.objectValueAtoB(info, this.users);
            }
          });
    },
    deleteUser(user, index) {
      this.$confirm("确认删除？")
          .then((_) => {
            this.$axios
                .post("http://192.168.0.187:5000/productJar/deleteuser", {
                  username: user.username,
                })
                .then((res) => {
                  let info = res.data.data;
                  if (res.data.code === 200) {
                    this.$message({
                      message: info,
                      duration: 3 * 1000,
                      showClose: true,
                      type: "success",
                    });
                    this.users.splice(index, 1)
                  } else {
                    this.$message({
                      message: info,
                      duration: 3 * 1000,
                      showClose: true,
                      type: "info",
                    });
                  }
                });
            this.getAllUserinfo();
          })
          .catch((_) => {
          });
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

.infoInput {
  width: 300px;
}
</style>