<template>
  <div class="m-contain">
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-centos"></i>cent187(服务器ip：192.168.0.187)
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
          <el-table-column prop="version" label="版本" width="200">
            <template slot-scope="scope">
              <el-tag type="success">{{ scope.row.version }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="path" label="url路径" width="320"
            ><template slot-scope="scope"
              >
              <router-link tag="a" :to="{}" target="_blank" :href="scope.row.url" >{{scope.row.url }}</router-link>
            </template>
          </el-table-column>
          <el-table-column prop="path" label="状态" width="100">
            <template slot-scope="scope">
              <el-tag
                :type="scope.row.msg === '空闲中' ? 'info' : ''"
                effect="plain"
                >{{ scope.row.msg }}</el-tag
              >
            </template>
          </el-table-column>
          <!-- <el-table-column prop="path" label="产品端口" width="80">
            <template slot-scope="scope">
              <el-tag type="success">{{ scope.row.viewPort }}</el-tag>
            </template>
          </el-table-column> -->
          <el-table-column prop="path" label="调试端口" width="80">
            <template slot-scope="scope">
              <el-tag type="success">{{ scope.row.port }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" >
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
              <!-- <el-button
                @click="update(scope.row)"
                type="danger"
                size="small"
                icon="el-icon-upload"
                plain
                >更换Jar包</el-button
              > -->
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
              <el-select
                v-model="date[scope.row.version]"
                placeholder="请选择jar包日期"
                style="width: 150px; margin-left: 10px"
                size="small"
                clearable
                @change="chooseDate()"
                filterable
              >
                <el-option
                  v-for="item in scope.row.jarDate"
                  :key="item"
                  :label="formatDateStr(item)"
                  :value="item"
                  ><span style="float: left"
                    ><svg class="icon" aria-hidden="true">
                      <use xlink:href="#el-icon-jar"></use></svg
                  ></span>
                  <span>{{ formatDateStr(item) }}</span>
                </el-option>
              </el-select>
              <el-upload
                class="upload-demo"
                action="http://192.168.0.187:5500/productJar/uploadJar"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :data="{ version: scope.row.version }"
                style="width: 150px; margin-left: 10px"
              >
                <el-button size="small" type="info" icon="el-icon-upload2"
                  >上传自定义jar包</el-button
                >
              </el-upload>
              <!-- <el-date-picker
              v-model="date[scope.row.version]"
              type="date"
              placeholder="选择日期"
              format="yyyy 年 MM 月 dd 日"
              value-format="yyyyMMdd"
            >
            </el-date-picker> -->
            </template>
          </el-table-column>
          <el-table-column label="可更换bihome" width="170">
            <template slot-scope="scope">
              <el-select
                v-model="bihome[scope.row.version]"
                placeholder="请选择bihome"
                style="width: 100px; margin-left: 10px"
                size="small"
                clearable
                @change="chooseDate()"
                filterable
              >
                <el-option
                  v-for="item in scope.row.bihomes"
                  :key="item"
                  :label="item"
                  :value="item"
                  ><span style="float: left"></span>
                  <span>{{ item }}</span>
                </el-option>
              </el-select>
              <el-button
                @click="exchangeBihome(scope.row, bihome[scope.row.version])"
                type="text"
                size="small"
                style="margin-left: 10px"
                >应用</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <p>tips：</p>
          <br/> 
          <p>1.上传jar包只要文件名中包含：api、product、third、product-swf 即可自动完成替换
            </p>  
            <br/>        
            <p>2.切换bihome，打开下拉选择，选中后，点击应用即可切换(没有启动环境不会自动启动环境，已启动的会自动重启)</p>          
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import bus from "../components/bus";

export default {
  name: "cent187",

  data() {
    return {
      tableData: [],
      status: {
        hasFound: false,
        msg: "",
      },
      bihome: {},
      jarDate: {},
      isUsed: {},
      date: {},
      checkRes: {},
    };
  },
  created() {
    this.$set(this.status, "hasFound", false);
    this.getAllProduct();
    this.get141Jar();
    this.getAllBihome();
    this.checkStatus();
    this.getDebugPort();
    this.getViewPort();
    this.getCurrentBihome();
    this.getURL();
  },
  methods: {
    changeTableData(version, key, value) {
      for (let i = 0; i < this.tableData.length; i++) {
        if (this.tableData[i].version === version) {
          this.$set(this.tableData[i], key, value);
          break;
        }
      }
    },
    getAllProduct() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.187:5500/productJar/all")
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
            duration: 600000,
            showClose: true,
            type: "error",
          });
          console.log(err);
        });
    },
    get141Jar() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.187:5500/productJar/141jar")
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
            duration: 600000,
            showClose: true,
            type: "error",
          });
        });
    },
    getAllBihome() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.187:5500/productJar/allBihome")
        .then((res) => {
          for (let v in res.data.data) {
            if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
              for (let i = 0; i < _this.tableData.length; i++) {
                if (_this.tableData[i].version === v)
                  _this.$set(_this.tableData[i], "bihomes", res.data.data[v]);
              }
            }
          }
        })
        .catch((err) => {
          console.log(err);
          this.$message({
            message: err,
            duration: 600000,
            showClose: true,
            type: "error",
          });
        });
    },
    getCurrentBihome() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.187:5500/productJar/currentBihome")
        .then((res) => {
          for (let v in res.data.data) {
            _this.$set(_this.bihome, v, res.data.data[v]);
          }
        })
        .catch((err) => {
          console.log(err);
          this.$message({
            message: err,
            duration: 600000,
            showClose: true,
            type: "error",
          });
        });
    },
    getURL() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.187:5500/productJar/url")
        .then((res) => {
          for (let v in res.data.data) {
            if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
              for (let i = 0; i < _this.tableData.length; i++) {
                if (_this.tableData[i].version === v)
                  _this.$set(_this.tableData[i], "url", "http://192.168.0.187:"+res.data.data[v]);
              }
            }
          }
        })
        .catch((err) => {
          console.log(err);
          this.$message({
            message: err,
            duration: 600000,
            showClose: true,
            type: "error",
          });
        });
    },
    checkStatus() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.187:5500/productJar/check")
        .then((res) => {
          for (let v in res.data.data) {
            if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
              for (let i = 0; i < _this.tableData.length; i++) {
                if (_this.tableData[i].version === v) {
                  _this.$set(_this.tableData[i], "checkRes", res.data.data[v]['status']);
                  _this.$set(_this.tableData[i], "start", res.data.data[v]['start']);
                  _this.$set(_this.tableData[i], "shutdown", res.data.data[v]['shutdown']);
                  _this.$set(_this.tableData[i], "reload", res.data.data[v]['reload']);
                  _this.$set(_this.tableData[i], "update", res.data.data[v]['update']);
                  _this.$set(_this.tableData[i], "updateAndReload", res.data.data[v]['updateAndReload']);
                  _this.$set(_this.tableData[i], "changeBihome", res.data.data[v]['changeBihome']);
                  if (_this.tableData[i].checkRes === "0")
                    _this.$set(_this.tableData[i], "msg", "空闲中");
                  else {
                    _this.$set(
                      _this.tableData[i],
                      "msg",
                      res.data.data[v] + "已启动"
                    );
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
            duration: 600000,
            showClose: true,
            type: "error",
          });
        });
    },
    getDebugPort() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.187:5500/productJar/port")
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
            duration: 600000,
            showClose: true,
            type: "error",
          });
        });
    },
    getViewPort() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.187:5500/productJar/bi")
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
            duration: 600000,
            showClose: true,
            type: "error",
          });
        });
    },
    shutdown(row) {
      let _this = this;
      this.changeTableData(row.version, "shutdown", true);
      this.$axios
        .post("http://192.168.0.187:5500/productJar/shutdown", {
          version: row.version,
        })
        .then((res) => {
          for (let i = 0; i < _this.tableData.length; i++) {
            if (_this.tableData[i].version === row.version)
              _this.$set(_this.tableData[i], "msg", "空闲中");
          }
          if (res.data.code === 200) {
            this.$message({
              message: res.data.data,
              duration: 600000,
              showClose: true,
              type: "success",
            });
          }
          this.changeTableData(row.version, "shutdown", false);
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 600000,
            showClose: true,
            type: "error",
          });
          console.log(err);
          this.changeTableData(row.version, "shutdown", false);
        });
    },
    startup(row) {
      let _this = this;
      this.changeTableData(row.version, "start", true);
      this.$axios
        .post("http://192.168.0.187:5500/productJar/startup", {
          version: row.version,
          user: this.$store.state.userInfo,
        })
        .then((res) => {
          if (res.data.code === 200) {
            for (let i = 0; i < _this.tableData.length; i++) {
              if (_this.tableData[i].version === row.version)
                _this.$set(
                  _this.tableData[i],
                  "msg",
                  this.$store.state.userInfo + "已启动"
                );
            }
            this.$message({
              message: res.data.data,
              duration: 600000,
              showClose: true,
              type: "success",
            });
            this.changeTableData(row.version, "start", false);
          }
          if (res.data.code === 205) {
            console.log(res.data);
            this.$message({
              message: res.data.data,
              duration: 600000,
              showClose: true,
              type: "warning",
            });
          }
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 600000,
            showClose: true,
            type: "error",
          });
          console.log(err);
          this.changeTableData(row.version, "start", false);
        });
    },

    update(row) {
      let form = {};
      this.changeTableData(row.version, "update", true);
      if (this.date[row.version] != null)
        form = {
          version: row.version,
          date: this.date[row.version],
        };
      else
        form = {
          version: row.version,
          date: "",
        };
      this.$axios
        .post("http://192.168.0.187:5500/productJar/update", form)
        .then((res) => {
          if (res.data.code === 200) {
            this.$message({
              message: res.data.data,
              duration: 600000,
              showClose: true,
              type: "success",
            });
          }
          this.changeTableData(row.version, "update", false);
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 600000,
            showClose: true,
            type: "error",
          });
          console.log(err);
          this.changeTableData(row.version, "update", false);
        });
    },
    reload(row) {
      let _this = this;
      this.changeTableData(row.version, "reload", true);
      this.$axios
        .post("http://192.168.0.187:5500/productJar/reload_product", {
          version: row.version,
          user: this.$store.state.userInfo,
        })
        .then((res) => {
          if (res.data.code === 200) {
            for (let i = 0; i < _this.tableData.length; i++) {
              if (_this.tableData[i].version === row.version)
                _this.$set(
                  _this.tableData[i],
                  "msg",
                  this.$store.state.userInfo + "已启动"
                );
            }
            this.$message({
              message: res.data.data,
              duration: 600000,
              showClose: true,
              type: "success",
            });
          }
          this.changeTableData(row.version, "reload", false);
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 600000,
            showClose: true,
            type: "error",
          });
          console.log(err);
          this.changeTableData(row.version, "reload", false);
        });
    },
    updateAndReload(row) {
      let _this = this;
      let form = {};
      if (this.date[row.version] != null)
        form = {
          version: row.version,
          date: this.date[row.version],
          user: this.$store.state.userInfo,
        };
      else
        form = {
          version: row.version,
          date: "",
          user: this.$store.state.userInfo,
        };
      this.changeTableData(row.version, "updateAndReload", true);
      this.$axios
        .post("http://192.168.0.187:5500/productJar/updateReload", form)
        .then((res) => {
          if (res.data.code === 200) {
            for (let i = 0; i < _this.tableData.length; i++) {
              if (_this.tableData[i].version === row.version)
                _this.$set(
                  _this.tableData[i],
                  "msg",
                  this.$store.state.userInfo + "已启动"
                );
            }
            this.$message({
              message: res.data.data,
              duration: 600000,
              showClose: true,
              type: "success",
            });
          }
          _this.changeTableData(row.version, "updateAndReload", false);
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 600000,
            showClose: true,
            type: "error",
          });
          _this.changeTableData(row.version, "updateAndReload", false);
          console.log(err);
        });
    },
    exchangeBihome(row, key) {
      this.$axios
        .post("http://192.168.0.187:5500/productJar/changeBihome", {
          version: row.version,
          bihome: key,
        })
        .then((res) => {
          if (res.data.code === 200) {
            this.$message({
              message: res.data.data,
              duration: 600000,
              showClose: true,
              type: "success",
            });
          }
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 600000,
            showClose: true,
            type: "error",
          });
          console.log(err);
        });
    },
    chooseDate() {
      console.log(this.date);
      console.log(this.bihome);
    },

    formatDateStr(str) {
      return (
        str.substring(0, 4) +
        "-" +
        str.substring(4, 6) +
        "-" +
        str.substring(6, 8)
      );
    },
    handleAvatarSuccess(res, file) {
      if (res.code === 200) {
        this.$message({
          message: res.data,
          duration: 600000,
          showClose: true,
          type: "success",
        });
      } else {
        this.$message({
          message: res.data,
          duration: 600000,
          showClose: true,
          type: "error",
        });
      }
    },
  },
};
</script>
<style scoped>
.el-upload {
  display: inline;
  text-align: center;
  cursor: pointer;
  outline: 0;
}

.upload-demo {
  display: inline;
}
</style>