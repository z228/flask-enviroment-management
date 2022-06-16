<template>
  <div class="m-contain">
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-centos"></i>cent187(服务器ip：192.168.0.187)
          <el-button
            type="success"
            icon="el-icon-refresh"
            circle
            size="mini"
            @click="refresh()"
          ></el-button
          >刷新环境状态
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="url_input all">
      <el-select v-model="branch" placeholder="请选择">
        <el-option
          v-for="item in branchs"
          :key="item"
          :label="item"
          :value="item"
        >
        </el-option>
      </el-select>
    </div>
    <div class="all">
      <el-button type="primary" @click="getData()">获取</el-button>
    </div>
    <div v-show="this.status.hasFound">
      <el-card class="box-card all">
        <el-table
          :data="tableData"
          style="width: 100%; margin-bottom: 20px"
          row-key="id"
          border
          default-expand-all
          max-height="500"
        >
          <el-table-column type="selection" width="55"> </el-table-column>
          <el-table-column prop="module" label="模块" width="300">
          </el-table-column>
          <el-table-column prop="folder" label="目录" width="300">
          </el-table-column>
          <el-table-column prop="file" label="文件"> </el-table-column>
        </el-table>
      </el-card>
    </div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <p>tips：</p>
          <br />
          <p>
            1.上传jar包只要文件名中包含：api、product、third、product-swf
            即可自动完成替换
          </p>
          <br />
          <p>
            2.切换bihome，打开下拉选择，选中后，点击应用即可切换(没有启动环境不会自动启动环境，已启动的会自动重启)
          </p>
          <br />
          <p>3.Hover在版本列的标签上会显示环境中jar包的信息</p>
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import bus from "../components/bus";

export default {
  name: "junitCase",

  data() {
    return {
      status: {
        hasFound: true,
        msg: "",
      },
      tableData: [],
      v86_tableData: [],
      v90_tableData: [],
      v921_tableData: [],
      v94_tableData: [],
      trunk_tableData: [],
      branchs: ["v8.6", "v9.0", "v9.2.1", "v9.4", "trunk"],
      branch: "v9.4",
      multipleSelection: [],
    };
  },
  created() {},
  methods: {
    getData() {
      let _this = this;
      this.$axios
        .post("http://192.168.0.187:5000/productJar/junitfail", {
          version: _this.branch,
        })
        .then((res) => {
          this.tableData = res.data.data;
          // console.log(res.data);
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
  /* float: left; */
}
.iframe_card {
  float: left;
  margin-top: 10px;
}
</style>