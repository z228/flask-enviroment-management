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
          <i class="el-icon-windows"></i>Windows
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
        <el-skeleton :rows="6" animated/>
      </el-card>
    </div>
    <div v-show="this.status.hasFound">
      <el-card class="box-card">
        <el-table :data="tableData" border style="width: 100%">
          <el-table-column prop="version" label="版本" width="100">
            <template slot-scope="scope">
              <el-popover
                  placement="right"
                  title="Jar包信息"
                  trigger="hover"
              >
                <slot v-for="info in scope.row.jarInfo">
                  <p>{{ info }}</p>
                </slot>
                <el-tag slot="reference" type="success">{{
                    scope.row.version
                  }}
                </el-tag>
              </el-popover>
            </template>
          </el-table-column>
          <el-table-column prop="path" label="url路径" width="200"
          >
            <template slot-scope="scope">
              <a target="_blank" :href="scope.row.url">{{ scope.row.url }}</a>
              <!-- <router-link tag="a" :to="{}" target="_blank" :href="scope.row.url" >{{scope.row.url }}</router-link> -->
            </template>
          </el-table-column>
          <el-table-column prop="path" label="状态" width="100">
            <template slot-scope="scope">
              <el-tag
                  :type="scope.row.msg === '未启动' ? 'info' : ''"
                  effect="plain"
              >{{ scope.row.msg }}
              </el-tag
              >
            </template>
          </el-table-column>
          <!-- <el-table-column prop="path" label="产品端口" width="100">
            <template slot-scope="scope">
              <el-tag type="success">{{ scope.row.viewPort }}</el-tag>
            </template>
          </el-table-column> -->
          <el-table-column prop="path" label="调试端口" width="80">
            <template slot-scope="scope">
              <el-tag type="success">{{ scope.row.port }}</el-tag>
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
              >关闭
              </el-button
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
              >
                <svg class="icon" aria-hidden="true">
                  <use xlink:href="#el-icon-run"></use>
                </svg>
                启动
              </el-button
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
              >更换Jar包
              </el-button
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
              >
                <svg class="icon" aria-hidden="true">
                  <use xlink:href="#el-icon-reload"></use>
                </svg>
                重启
              </el-button
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
              >更换Jar包并重启
              </el-button
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
              >应用
              </el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script>

export default {
  name: "windows_local",

  data() {
    return {
      tableData: [],
      status: {
        hasFound: false,
      },
      bihome: {},
      jarDate: {},
      date: {},
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
    this.getJarInfo();
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
    getURL() {
      let _this = this;
      this.$axios
          .get("http://192.168.0.192:5000/productJar/url", {
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
          })
          .then((res) => {
            for (let v in res.data.data) {
              if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
                for (let i = 0; i < _this.tableData.length; i++) {
                  if (_this.tableData[i].version === v)
                    _this.$set(
                        _this.tableData[i],
                        "url",
                        "http://192.168.0.192:" + res.data.data[v]
                    );
                }
              }
            }
          })
    },
    clearData() {
      this.$common.resetObject(this.tableData);
      this.$common.resetObject(this.bihomes);
      this.$common.resetObject(this.jarDate);
      this.$common.resetObject(this.date);
    },
    refresh() {
      this.checkStatus();
      this.getJarInfo();
    },
    getAllProduct() {
      let _this = this;
      this.$axios
          .get("http://192.168.0.192:5000/productJar/all", {
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
          })
          .then((res) => {
            for (let v in res.data.data) {
              if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
                // console.log(res.data.data[v])
                if (_this.tableData)
                  _this.tableData.push({
                    version: v,
                    path: res.data.data[v].path,
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
    },
    get141Jar() {
      let _this = this;
      this.$axios
          .get("http://192.168.0.192:5000/productJar/141jar", {
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
          })
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
    },
    getAllBihome() {
      let _this = this;
      this.$axios
          .get("http://192.168.0.192:5000/productJar/allBihome", {
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
          })
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
    },
    getCurrentBihome() {
      let _this = this;
      this.$axios
          .get("http://192.168.0.192:5000/productJar/currentBihome", {
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
          })
          .then((res) => {
            for (let v in res.data.data) {
              _this.$set(_this.bihome, v, res.data.data[v]);
            }
          })
    },
    getJarInfo() {
      let _this = this;
      this.$axios
          .get("http://192.168.0.192:5000/productJar/jarInfo", {
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
          })
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
    },
    checkStatus() {
      let _this = this;
      this.$axios
          .get("http://192.168.0.192:5000/productJar/check", {
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
          })
          .then((res) => {
            for (let v in res.data.data) {
              if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
                for (let i = 0; i < _this.tableData.length; i++) {
                  if (_this.tableData[i].version === v) {
                    _this.$set(_this.tableData[i], "checkRes", res.data.data[v].status);
                    _this.$set(_this.tableData[i], "startup", res.data.data[v].startup);
                    _this.$set(_this.tableData[i], "shutdown", res.data.data[v].shutdown);
                    _this.$set(_this.tableData[i], "update", res.data.data[v].update);
                    _this.$set(_this.tableData[i], "reload", res.data.data[v].reload);
                    _this.$set(_this.tableData[i], "updateAndReload", res.data.data[v].updateAndReload);
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
    },
    getDebugPort() {
      let _this = this;
      this.$axios
          .get("http://192.168.0.192:5000/productJar/port", {
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
          })
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
    },
    getViewPort() {
      let _this = this;
      this.$axios
          .get("http://192.168.0.192:5000/productJar/bi", {
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
          })
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
    },
    shutdown(row) {
      this.changeTableData(row.version, "shutdown", true);
      this.$axios
          .post("http://192.168.0.192:5000/productJar/shutdown", {
            version: row.version,
          }, {
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
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
            this.$common.changeListKeyValue(
                this.tableData,
                row.version,
                "msg",
                "未启动"
            );
            this.$common.changeListKeyValue(
                this.tableData,
                row.version,
                "shutdown",
                false
            );
          })
    },
    startup(row) {
      this.changeTableData(row.version, "start", true);
      this.$axios
          .post("http://192.168.0.192:5000/productJar/startup", {
            version: row.version,
          }, {
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
          })
          .then((res) => {
            if (res.data.code === 200) {
              this.$message({
                message: res.data.data,
                duration: 600000,
                showClose: true,
                type: "success",
              });
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
            }
          })
    },

    update(row) {
      this.changeTableData(row.version, "update", true);
      let form = {};
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
          .post("http://192.168.0.192:5000/productJar/update", form, {
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
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
            this.$common.changeListKeyValue(
                this.tableData,
                row.version,
                "update",
                false
            );
          })
    },
    reload(row) {
      this.changeTableData(row.version, "reload", true);
      this.$axios
          .post("http://192.168.0.192:5000/productJar/reload_product", {
            version: row.version,
          },{
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
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
            this.$common.changeListKeyValue(
                this.tableData,
                row.version,
                "reload",
                false
            );
          })
    },
    updateAndReload(row) {
      this.changeTableData(row.version, "updateAndReload", true);
      let form = {};
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
          .post("http://192.168.0.192:5000/productJar/updateReload", form,{
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
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
            this.$common.changeListKeyValue(
                this.tableData,
                row.version,
                "updateAndReload",
                false
            );
          })
    },
    exchangeBihome(row, key) {
      this.$axios
          .post("http://192.168.0.192:5000/productJar/changeBihome", {
            version: row.version,
            bihome: key,
          }, {
             headers: {
              "Authorization": sessionStorage.getItem("userInfo")
            }
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
    },
    chooseDate() {
      console.log(this.date);
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
  },
};
</script>