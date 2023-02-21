<template>
  <div
    class="m-contain"
    v-if="
      this.$store.state.userInfo === 'admin' ||
      this.$store.state.userInfo === '曾成龙' ||
      this.$store.state.userInfo === 'zcl'
    "
  >
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-ubuntu"></i>Linux
          <el-button
            type="success"
            icon="el-icon-refresh"
            circle
            size="mini"
            @click="refresh()"
          ></el-button>
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div v-show="!this.status.hasFound">
      <el-card>
        <el-skeleton :rows="6" animated />
      </el-card>
    </div>
    <div v-show="this.status.hasFound">
      <el-card class="box-card">
        <el-table :data="tableData" border style="width: 100%">
          <el-table-column prop="version" label="版本" width="100">
            <template slot-scope="scope">
              <el-popover placement="right" title="Jar包信息" trigger="hover">
                <slot v-for="info in scope.row.jarInfo">
                  <p>{{ info }}</p>
                </slot>
                <el-tag slot="reference" type="success">{{
                  scope.row.version
                }}</el-tag>
              </el-popover>
            </template>
          </el-table-column>
          <el-table-column prop="path" label="路径" width="300"
            ><template slot-scope="scope"
              ><svg class="icon" aria-hidden="true">
                <use xlink:href="#el-icon-url"></use>
              </svg>
              <span> {{ scope.row.path }}</span></template
            >
          </el-table-column>
          <el-table-column prop="path" label="状态" width="100">
            <template slot-scope="scope">
              <el-tag
                :type="scope.row.msg === '未启动' ? 'info' : ''"
                effect="plain"
                >{{ scope.row.msg }}</el-tag
              >
            </template>
          </el-table-column>
          <el-table-column prop="path" label="产品端口" width="100">
            <template slot-scope="scope">
              <el-tag type="success">{{ scope.row.viewPort }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button
                @click="shutdown(scope.row)"
                type="warning"
                size="small"
                icon="el-icon-close"
                @disabled="scope.row.shutdown"
                v-loading="scope.row.shutdown"
                element-loading-text="关闭中"
                element-loading-spinner="el-icon-loading"
                element-loading-background="rgba(0, 0, 0, 0.8)"
                plain
                >关闭</el-button
              >
              <el-button
                @click="startup(scope.row)"
                type="primary"
                size="small"
                @disabled="scope.row.start"
                v-loading="scope.row.start"
                element-loading-text="启动中"
                element-loading-spinner="el-icon-loading"
                element-loading-background="rgba(0, 0, 0, 0.8)"
                plain
                ><svg class="icon" aria-hidden="true">
                  <use xlink:href="#el-icon-run"></use>
                </svg>
                启动</el-button
              >
              <el-button
                @click="update(scope.row)"
                type="danger"
                size="small"
                icon="el-icon-upload"
                @disabled="scope.row.update"
                v-loading="scope.row.update"
                element-loading-text="换包中"
                element-loading-spinner="el-icon-loading"
                element-loading-background="rgba(0, 0, 0, 0.8)"
                plain
                >更换Jar包</el-button
              >
              <el-button
                @click="reload(scope.row)"
                type="primary"
                size="small"
                @disabled="scope.row.reload"
                v-loading="scope.row.reload"
                element-loading-text="重启中"
                element-loading-spinner="el-icon-loading"
                element-loading-background="rgba(0, 0, 0, 0.8)"
                plain
                ><svg class="icon" aria-hidden="true">
                  <use xlink:href="#el-icon-reload"></use>
                </svg>
                重启</el-button
              >
              <el-button
                @click="updateAndReload(scope.row)"
                type="success"
                size="small"
                icon="el-icon-loading"
                @disabled="scope.row.updateAndReload"
                v-loading="scope.row.updateAndReload"
                element-loading-text="jar包正在更换中"
                element-loading-spinner="el-icon-loading"
                element-loading-background="rgba(0, 0, 0, 0.8)"
                element-loading-custom-class="updateLoading"
                plain
                >更换Jar包并重启</el-button
              >
            </template>
          </el-table-column>
          <!-- <el-table-column label="可更换bihome">
            <template slot-scope="scope">
              <el-button
                v-for="tag in bihomes[scope.row.version]"
                :key="tag"
                type="info"
                style="margin: 2px"
                size="small"
                @click="exchangeBihome(scope.row, tag)"
                round
                plain
                ><svg class="icon" aria-hidden="true">
                  <use xlink:href="#el-icon-enviroment"></use>
                </svg>
                {{ tag }}</el-button
              >
            </template>
          </el-table-column> -->
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import bus from "../components/bus";

export default {
  name: "linux_mobile",

  data() {
    return {
      tableData: [],
      status: {
        hasFound: false,
      },
      bihomes: {},
    };
  },
  async created() {
    this.$set(this.status, "hasFound", false);
    await this.getAllProduct();
    // this.get141Jar();
    this.getAllBihome();
    this.checkStatus();
    // this.getDebugPort();
    this.getViewPort();
    this.getJarInfo();
  },
  methods: {
    refresh() {
      this.checkStatus();
      this.getJarInfo();
    },
    changeTableData(version, key, value) {
      for (let i = 0; i < this.tableData.length; i++) {
        if (this.tableData[i].version === version) {
          this.$set(this.tableData[i], key, value);
          break;
        }
      }
    },
    getJarInfo() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.6:5000/productJar/jarInfo")
        .then((res) => {
          for (let v in res.data.data) {
            if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
              for (let i = 0; i < _this.tableData.length; i++) {
                if (_this.tableData[i].version === v)
                  _this.$set(_this.tableData[i], "jarInfo", res.data.data[v]);
              }
            }
          }
        })
        .catch((err) => {
          console.log(err);
          this.$message({
            message: err,
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
        });
    },
    getAllProduct() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.6:5000/productJar/all")
        .then((res) => {
          for (let v in res.data.data) {
            if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
              _this.tableData.push({
                version: v,
                path: res.data.data[v],
                start: false,
                shutdown: false,
                reload: false,
                update: false,
                updateAndReload: false,
              });
            }
          }
          _this.$set(_this.status, "hasFound", true);
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
          console.log(err);
        });
    },
    get141Jar() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.6:5000/productJar/141jar")
        .then((res) => {
          for (let v in res.data.data) {
            if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
              for (let i = 0; i < _this.tableData.length; i++) {
                if (_this.tableData[i].version === v)
                  _this.$set(_this.tableData[i], "jarDate", res.data.data[v]);
              }
            }
            _this.$set(_this.date, v, res.data.data[v][0]);
          }
        })
        .catch((err) => {
          console.log(err);
          this.$message({
            message: err,
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
        });
    },
    getAllBihome() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.6:5000/productJar/allBihome")
        .then((res) => {
          for (let v in res.data.data) {
            if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
              for (let i = 0; i < _this.tableData.length; i++) {
                if (_this.tableData[i].version === v)
                  _this.$set(_this.bihomes, v, res.data.data[v]);
              }
            }
          }
        })
        .catch((err) => {
          console.log(err);
          this.$message({
            message: err,
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
        });
    },
    checkStatus() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.6:5000/productJar/check")
        .then((res) => {
          for (let v in res.data.data) {
            if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
              for (let i = 0; i < _this.tableData.length; i++) {
                if (_this.tableData[i].version === v) {
                  _this.$set(_this.tableData[i], "checkRes", res.data.data[v]);
                  if (_this.tableData[i].checkRes === "0")
                    _this.$set(_this.tableData[i], "msg", "未启动");
                  else {
                    _this.$set(_this.tableData[i], "msg", "运行中");
                  }
                  break;
                }
              }
            }
          }
        })
        .catch((err) => {
          console.log(err);
          this.$message({
            message: err,
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
        });
    },
    getDebugPort() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.6:5000/productJar/port")
        .then((res) => {
          for (let v in res.data.data) {
            if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
              for (let i = 0; i < _this.tableData.length; i++) {
                if (_this.tableData[i].version === v)
                  _this.$set(_this.tableData[i], "port", res.data.data[v]);
              }
            }
          }
        })
        .catch((err) => {
          console.log(err);
          this.$message({
            message: err,
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
        });
    },
    getViewPort() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.6:5000/productJar/bi")
        .then((res) => {
          for (let v in res.data.data) {
            if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
              for (let i = 0; i < _this.tableData.length; i++) {
                if (_this.tableData[i].version === v)
                  _this.$set(_this.tableData[i], "viewPort", res.data.data[v]);
              }
            }
          }
        })
        .catch((err) => {
          console.log(err);
          this.$message({
            message: err,
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
        });
    },
    shutdown(row) {
      this.changeTableData(row.version, "shutdown", true);
      this.$axios
        .post("http://192.168.0.6:5000/productJar/shutdown", {
          version: row.version,
        })
        .then((res) => {
          if (res.data.code === 200) {
            this.$message({
              message: res.data.data,
              duration: 6 * 1000,
              showClose: true,
              type: "success",
            });
            this.$common.changeListKeyValue(
              this.tableData,
              row.version,
              "msg",
              "未启动"
            );
          }
          this.$common.changeListKeyValue(
            this.tableData,
            row.version,
            "shutdown",
            false
          );
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
          console.log(err);
          this.$common.changeListKeyValue(
            this.tableData,
            row.version,
            "shutdown",
            false
          );
        });
    },
    startup(row) {
      this.changeTableData(row.version, "start", true);
      this.$axios
        .post("http://192.168.0.6:5000/productJar/startup", {
          version: row.version,
        })
        .then((res) => {
          if (res.data.code === 200) {
            this.$message({
              message: res.data.data,
              duration: 6 * 1000,
              showClose: true,
              type: "success",
            });
          }
          this.$common.changeListKeyValue(
            this.tableData,
            row.version,
            "msg",
            "运行中"
          );
          this.$common.changeListKeyValue(
            this.tableData,
            row.version,
            "start",
            false
          );
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
          console.log(err);
          this.$common.changeListKeyValue(
            this.tableData,
            row.version,
            "start",
            false
          );
        });
    },
    update(row) {
      this.changeTableData(row.version, "update", true);
      this.$axios
        .post("http://192.168.0.192:5000/productJar/updateLinuxJar", {
          version: row.version,
        })
        .then((res) => {
          if (res.data.code === 200) {
            this.$message({
              message: res.data.data,
              duration: 6 * 1000,
              showClose: true,
              type: "success",
            });
          }
          this.$common.changeListKeyValue(
            this.tableData,
            row.version,
            "update",
            false
          );
          this.getJarInfo();
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
          console.log(err);
          this.$common.changeListKeyValue(
            this.tableData,
            row.version,
            "update",
            false
          );
        });
    },
    reload(row) {
      this.changeTableData(row.version, "reload", true);
      this.$axios
        .post("http://192.168.0.6:5000/productJar/reload_product", {
          version: row.version,
        })
        .then((res) => {
          if (res.data.code === 200) {
            this.$message({
              message: res.data.data,
              duration: 6 * 1000,
              showClose: true,
              type: "success",
            });
          }
          this.$common.changeListKeyValue(
            this.tableData,
            row.version,
            "reload",
            false
          );
          this.$common.changeListKeyValue(
            this.tableData,
            row.version,
            "updateAndReload",
            false
          );
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
          console.log(err);
          this.$common.changeListKeyValue(
            this.tableData,
            row.version,
            "reload",
            false
          );
          this.$common.changeListKeyValue(
            this.tableData,
            row.version,
            "updateAndReload",
            false
          );
        });
    },
    updateAndReload(row) {
      this.changeTableData(row.version, "updateAndReload", true);
      this.changeTableData(row.version, "update", true);
      this.$axios
        .post("http://192.168.0.192:5000/productJar/updateLinuxJar", {
          version: row.version,
        })
        .then((res) => {
          if (res.data.code === 200) {
            this.$message({
              message: res.data.data,
              duration: 6 * 1000,
              showClose: true,
              type: "success",
            });
            this.reload(row);
            this.$common.changeListKeyValue(
              this.tableData,
              row.version,
              "update",
              false
            );
            this.getJarInfo();
          }
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
          console.log(err);
          this.$common.changeListKeyValue(
            this.tableData,
            row.version,
            "update",
            false
          );
          this.$common.changeListKeyValue(
            this.tableData,
            row.version,
            "updateAndReload",
            false
          );
        });
    },
    exchangeBihome(row, key) {
      this.$axios
        .post("http://192.168.0.6:5000/productJar/changeBihome", {
          version: row.version,
          bihome: key,
        })
        .then((res) => {
          if (res.data.code === 200) {
            this.$message({
              message: res.data.data,
              duration: 6 * 1000,
              showClose: true,
              type: "success",
            });
          }
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
          console.log(err);
        });
    },
  },
};
</script>