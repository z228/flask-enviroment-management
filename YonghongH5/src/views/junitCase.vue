<template>
  <div class="m-contain">
    <el-card class="box-card"
      ><div class="name_input all codeEdit">
        <!-- <el-form-item label="请输入要check的服务器ip:"> -->
        <el-select v-model="version" placeholder="请选择版本">
          <el-option
            v-for="item in version_list"
            :key="item"
            :label="item"
            :value="item"
          ></el-option>
        </el-select>
      </div>
      <div class="all codeEdit">
        <el-button type="primary" @click="getFailTree">获取</el-button>
      </div>
      <div class="all codeEdit">
        <el-input
          placeholder="输入关键字进行过滤"
          v-model="filterText"
          style="width: 500px"
          prefix-icon="el-icon-search"
          clearable
        >
        </el-input>
      </div>
      <div class="all codeEdit">
        <el-button @click="exchangExp">更换Exp</el-button>
      </div>
      <div class="all codeEdit">
        <el-button @click="exchangExpDis">更换Exp_Dis</el-button>
      </div>
      <div class="" style="border: 1px solid #dcdfe6; margin-top: 60px">
        <el-tree
          class="filter-tree"
          :data="junitCases"
          show-checkbox
          :props="defaultProps"
          :filter-node-method="filterNode"
          ref="tree"
        >
        </el-tree>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      changeCases: [],
      filterText: "",
      junitCases: [],
      version_list: ["v9.0", "v9.2.1", "v9.4", "v10.0", "trunk"],
      version: "v9.4",
      defaultProps: {
        children: "children",
        label: "name",
      },
    };
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val);
    },
  },

  methods: {
    filterNode(value, data, node) {
      if (!value) {
        node.expanded = false;
        return true;
      }
      // return data.name.indexOf(value) !== -1;
      return this.checkBelongToChooseNode(value, data, node);
    },
    exchangExp() {
      let form = {
        version: this.version,
        cases: [],
        user: this.$store.state.userInfo,
      };
      for (let i of this.$refs.tree.getCheckedNodes(false, false)) {
        if (i.path !== undefined) form.cases.push(i.path);
      }
      this.$axios
        .post("http://192.168.0.187:5000/productJar/junitexp", form, {
          headers: {
            Authorization: sessionStorage.getItem("username"),
          },
        })
        .then((res) => {
          this.$message({
            message: res.data.data,
            duration: 10 * 1000,
            showClose: true,
            type: "success",
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },
    exchangExpDis() {
      let form = {
        version: this.version,
        cases: [],
        user: this.$store.state.userInfo,
      };
      for (let i of this.$refs.tree.getCheckedNodes(false, false)) {
        if (i.path !== undefined) form.cases.push(i.path);
      }
      this.$axios
        .post("http://192.168.0.187:5000/productJar/junitdisexp", form, {
          headers: {
            Authorization: sessionStorage.getItem("username"),
          },
        })
        .then((res) => {
          this.$message({
            message: res.data.data,
            duration: 10 * 1000,
            showClose: true,
            type: "success",
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getFailTree() {
      let _this = this;
      let form = {
        version: _this.version,
      };
      this.$axios
        .post("http://192.168.0.187:5000/productJar/junitdiff", form, {
          headers: {
            Authorization: sessionStorage.getItem("username"),
          },
        })
        .then((res) => {
          _this.junitCases = res.data.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    // 判断传入的节点是不是选中节点的子节点
    checkBelongToChooseNode(value, data, node) {
      if (data.name.indexOf(value) !== -1) {
        return true;
      }
      const level = node.level;
      // 如果传入的节点本身就是一级节点就不用校验了
      if (level === 1) {
        return false;
      }
      // 先取当前节点的父节点
      let parentData = node.parent;
      // 遍历当前节点的父节点
      let index = 0;
      while (index < level - 1) {
        // 如果匹配到直接返回
        if (parentData.data.name.indexOf(value) != -1) {
          // node.text = "red";
          return true;
        }
        // 否则的话再往上一层做匹配
        parentData = parentData.parent;
        index++;
      }
      // 没匹配到返回false
      return false;
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
}
.iframe_card {
  float: left;
  margin-top: 10px;
}
.codeEdit {
  float: left;
}
.red {
  color: red;
}
</style>