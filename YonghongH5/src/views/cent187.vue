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
          <el-table-column prop="version" label="版本" width="150">
            <template slot-scope="scope">
              <el-popover placement="right" title="Jar包信息" trigger="hover">
                <slot v-for="info in scope.row.jarInfo">
                  <p>{{ info }}</p>
                </slot>
                <el-tag slot="reference" type="success"
                  >{{ scope.row.version }}
                </el-tag>
              </el-popover>
            </template>
          </el-table-column>
          <el-table-column prop="path" label="url路径" width="300">
            <template slot-scope="scope">
              <a target="_blank" :href="scope.row.url">{{ scope.row.url }} </a>
            </template>
          </el-table-column>
          <el-table-column prop="path" label="状态" width="150">
            <template slot-scope="scope">
              <el-tag
                :type="scope.row.msg === '空闲中' ? 'info' : ''"
                effect="plain"
                class="status-tag"
                >{{ scope.row.msg }}
              </el-tag>
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
              </el-button>
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
              </el-button>
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
              >
                <svg class="icon" aria-hidden="true">
                  <use xlink:href="#el-icon-reload"></use>
                </svg>
                重启
              </el-button>
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
              </el-button>
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
                action="http://192.168.0.187:5000/productJar/uploadJar"
                :show-file-list="false"
                :on-success="
                  (response, file, filelist) =>
                    handleAvatarSuccess(scope.row, response, file, filelist)
                "
                :data="{ version: scope.row.version }"
                style="width: 150px; margin-left: 10px"
              >
                <el-button
                  size="small"
                  type="info"
                  icon="el-icon-upload2"
                  @disabled="scope.row.updateAndReload"
                  v-loading="scope.row.updateAndReload"
                  element-loading-text="jar包正在更换中"
                  element-loading-spinner="el-icon-loading"
                  element-loading-background="rgba(0, 0, 0, 0.8)"
                  element-loading-custom-class="updateLoading"
                  plain
                  >上传自定义jar包
                </el-button>
              </el-upload>
              <!-- <el-date-picker
              v-model="date[scope.row.version]"
              type="date"
              placeholder="选择日期"
              format="yyyy 年 MM 月 dd 日"
              value-format="yyyyMMdd"
            >
            </el-date-picker> -->
              <!--              <el-button-->
              <!--                  style="margin-left: 10px"-->
              <!--                  type="text"-->
              <!--                  @click="editBiPro(scope.row)"-->
              <!--                  fullscreen=true-->
              <!--              >编辑bi.pro-->
              <!--              </el-button-->
              <!--              >-->
              <!--              <el-dialog-->
              <!--                  title="bi.properties"-->
              <!--                  :visible.sync="dialogVisible"-->
              <!--                  width="30%"-->
              <!--                  :before-close="handleClose"-->
              <!--              >-->
              <!--                <code-mirror-editor-->
              <!--                    ref="cmEditor"-->
              <!--                    cmTheme="idea"-->
              <!--                    cmMode="text/x-properties"-->
              <!--                    :autoFormatJson="autoFormatJson" style="border:1px solid #efefef"-->
              <!--                ></code-mirror-editor>-->
              <!--                <span slot="footer" class="dialog-footer">-->
              <!--                  <el-button @click="cancleEdit()">取 消</el-button>-->
              <!--                  <el-button type="primary" @click="commitChange()"-->
              <!--                  >确 定</el-button-->
              <!--                  >-->
              <!--                </span>-->
              <!--              </el-dialog>-->
            </template>
          </el-table-column>
          <!-- <el-table-column label="可更换bihome" width="170">
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
              </el-button>
            </template>
          </el-table-column> -->
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
import CodeMirrorEditor from "../components/CodeMirrorEditor";

export default {
  name: "cent187",
  components: {
    CodeMirrorEditor,
  },
  data() {
    return {
      editorValue: "",
      autoFormatJson: false, // json编辑模式下，输入框失去焦点时是否自动格式化，true 开启， false 关闭
      dialogVisible: false,
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
  async created() {
    this.$set(this.status, "hasFound", false);
    await this.getAllProduct();
    this.get141Jar();
    this.getReleaseJar();
    this.getAllBihome();
    this.checkStatus();
    this.getDebugPort();
    // this.getViewPort();
    this.getCurrentBihome();
    this.getURL();
    this.getJarInfo();
    // this.getbiPro();
  },
  mounted() {
    const timer = setInterval(() => {
      this.refresh();
      this.get141Jar();
    }, 1000 * 60 * 60);
    this.$once("hook:beforeDestroy", () => {
      clearInterval(timer);
    });
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
        .get("http://192.168.0.187:5000/productJar/jarInfo", {
          headers: {
            Authorization: sessionStorage.getItem("userInfo"),
          },
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
        .get("http://192.168.0.187:5000/productJar/all", {
          headers: {
            Authorization: sessionStorage.getItem("userInfo"),
          },
        })
        .then((res) => {
          for (let v of res.data.data) {
            _this.tableData.push({
              version: v,
              //path: res.data.data[v].path,
            });
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
        .get("http://192.168.0.187:5000/productJar/141jar", {
          headers: {
            Authorization: sessionStorage.getItem("userInfo"),
          },
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
    getReleaseJar() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.187:5000/productJar/releasejar", {
          headers: {
            Authorization: sessionStorage.getItem("userInfo"),
          },
        })
        .then((res) => {
          console.log(res)
          for (let v in res.data.data) {
            if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
              for (let i = 0; i < _this.tableData.length; i++) {
                if (_this.tableData[i].version === v)
                  _this.$set(_this.tableData[i], "release", res.data.data[v]);
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
        .get("http://192.168.0.187:5000/productJar/allBihome", {
          headers: {
            Authorization: sessionStorage.getItem("userInfo"),
          },
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
    getCurrentBihome() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.187:5000/productJar/currentBihome", {
          headers: {
            Authorization: sessionStorage.getItem("userInfo"),
          },
        })
        .then((res) => {
          for (let v in res.data.data) {
            _this.$set(_this.bihome, v, res.data.data[v]);
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
    getURL() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.187:5000/productJar/url", {
          headers: {
            Authorization: sessionStorage.getItem("userInfo"),
          },
        })
        .then((res) => {
          for (let v in res.data.data) {
            if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
              for (let i = 0; i < _this.tableData.length; i++) {
                if (_this.tableData[i].version === v)
                  _this.$set(
                    _this.tableData[i],
                    "url",
                    "http://192.168.0.187:" + res.data.data[v]
                  );
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
        .get("http://192.168.0.187:5000/productJar/check", {
          headers: {
            Authorization: sessionStorage.getItem("userInfo"),
          },
        })
        .then((res) => {
          for (let v in res.data.data) {
            if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
              for (let i = 0; i < _this.tableData.length; i++) {
                if (_this.tableData[i].version === v) {
                  _this.$set(
                    _this.tableData[i],
                    "checkRes",
                    res.data.data[v].startUser
                  );
                  _this.$set(
                    _this.tableData[i],
                    "startup",
                    res.data.data[v].startup
                  );
                  _this.$set(
                    _this.tableData[i],
                    "shutdown",
                    res.data.data[v].shutdown
                  );
                  _this.$set(
                    _this.tableData[i],
                    "update",
                    res.data.data[v].update
                  );
                  _this.$set(
                    _this.tableData[i],
                    "reload",
                    res.data.data[v].reload
                  );
                  _this.$set(
                    _this.tableData[i],
                    "updateAndReload",
                    res.data.data[v].updateAndReload
                  );
                  if (_this.tableData[i].checkRes === "0")
                    _this.$set(_this.tableData[i], "msg", "空闲中");
                  else {
                    _this.$set(
                      _this.tableData[i],
                      "msg",
                      res.data.data[v].startUser + "已启动"
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
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
        });
    },
    getDebugPort() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.187:5000/productJar/port", {
          headers: {
            Authorization: sessionStorage.getItem("userInfo"),
          },
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
        .get("http://192.168.0.187:5000/productJar/bi", {
          headers: {
            Authorization: sessionStorage.getItem("userInfo"),
          },
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
      let _this = this;
      this.changeTableData(row.version, "shutdown", true);
      this.$axios
        .post(
          "http://192.168.0.187:5000/productJar/shutdown",
          {
            version: row.version,
            user: this.$store.state.userInfo,
          },
          {
            headers: {
              Authorization: sessionStorage.getItem("userInfo"),
            },
          }
        )
        .then((res) => {
          for (let i = 0; i < _this.tableData.length; i++) {
            if (_this.tableData[i].version === row.version)
              _this.$set(_this.tableData[i], "msg", "空闲中");
          }
          if (res.data.code === 200) {
            this.$message({
              message: res.data.data,
              duration: 6 * 1000,
              showClose: true,
              type: "success",
            });
          }
          if (res.data.code === 205) {
            console.log(res.data);
            this.$message({
              message: res.data.data,
              duration: 6 * 1000,
              showClose: true,
              type: "warning",
            });
          }
          this.changeTableData(row.version, "shutdown", false);
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 6 * 1000,
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
        .post(
          "http://192.168.0.187:5000/productJar/startup",
          {
            version: row.version,
            user: this.$store.state.userInfo,
          },
          {
            headers: {
              Authorization: sessionStorage.getItem("userInfo"),
            },
          }
        )
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
              duration: 6 * 1000,
              showClose: true,
              type: "success",
            });
          }
          if (res.data.code === 205) {
            console.log(res.data);
            this.$message({
              message: res.data.data,
              duration: 6 * 1000,
              showClose: true,
              type: "warning",
            });
          }
          this.changeTableData(row.version, "start", false);
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 6 * 1000,
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
          user: this.$store.state.userInfo,
        };
      else
        form = {
          version: row.version,
          date: "",
          user: this.$store.state.userInfo,
        };
      this.$axios
        .post("http://192.168.0.187:5000/productJar/update", form, {
          headers: {
            Authorization: sessionStorage.getItem("userInfo"),
          },
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
          if (res.data.code === 205) {
            console.log(res.data);
            this.$message({
              message: res.data.data,
              duration: 6 * 1000,
              showClose: true,
              type: "warning",
            });
          }
          this.changeTableData(row.version, "update", false);
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
          this.changeTableData(row.version, "update", false);
        });
    },
    reload(row) {
      let _this = this;
      this.changeTableData(row.version, "reload", true);
      this.$axios
        .post(
          "http://192.168.0.187:5000/productJar/reload_product",
          {
            version: row.version,
            user: this.$store.state.userInfo,
          },
          {
            headers: {
              Authorization: sessionStorage.getItem("userInfo"),
            },
          }
        )
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
              duration: 6 * 1000,
              showClose: true,
              type: "success",
            });
          }
          if (res.data.code === 205) {
            console.log(res.data);
            this.$message({
              message: res.data.data,
              duration: 6 * 1000,
              showClose: true,
              type: "warning",
            });
          }
          this.changeTableData(row.version, "reload", false);
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 6 * 1000,
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
        .post("http://192.168.0.187:5000/productJar/updateReload", form, {
          headers: {
            Authorization: sessionStorage.getItem("userInfo"),
          },
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
              duration: 6 * 1000,
              showClose: true,
              type: "success",
            });
          }
          if (res.data.code === 205) {
            console.log(res.data);
            this.$message({
              message: res.data.data,
              duration: 6 * 1000,
              showClose: true,
              type: "warning",
            });
          }
          _this.changeTableData(row.version, "updateAndReload", false);
          this.getJarInfo();
        })
        .catch((err) => {
          this.$message({
            message: err,
            duration: 6 * 1000,
            showClose: true,
            type: "error",
          });
          _this.changeTableData(row.version, "updateAndReload", false);
          console.log(err);
        });
    },
    exchangeBihome(row, key) {
      this.$axios
        .post(
          "http://192.168.0.187:5000/productJar/changeBihome",
          {
            version: row.version,
            bihome: key,
            user: this.$store.state.userInfo,
          },
          {
            headers: {
              Authorization: sessionStorage.getItem("userInfo"),
            },
          }
        )
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
    handleAvatarSuccess(row, res, file, fileList) {
      this.changeTableData(row.version, "updateAndReload", false);
      if (res.code === 200) {
        this.$message({
          message: res.data,
          duration: 6 * 1000,
          showClose: true,
          type: "success",
        });
        this.getJarInfo();
      } else {
        this.$message({
          message: res.data,
          duration: 6 * 1000,
          showClose: true,
          type: "error",
        });
      }
    },
    handleClose(done) {
      this.$confirm("确认关闭？")
        .then((_) => {
          done();
        })
        .catch((_) => {});
    },
    cancleEdit() {
      this.$confirm("确认关闭？")
        .then((_) => {
          this.dialogVisible = false;
          done();
        })
        .catch((_) => {});
    },
    commitChange() {},
    getValue() {
      let content = this.$refs.cmEditor.getValue();
      console.log(content);
    },
    //修改内容
    setValue(data) {
      this.editorValue = data;
    },
    editBiPro(row) {
      let _this = this;
      this.dialogVisible = true;
      for (let i = 0; i < _this.tableData.length; i++) {
        if (_this.tableData[i].version === row.version)
          _this.$refs.cmEditor.setValue(this.tableData[i].biPro);
        break;
      }
    },
    getbiPro() {
      let _this = this;
      this.$axios
        .get("http://192.168.0.187:5000/productJar/biPro", {
          headers: {
            Authorization: sessionStorage.getItem("userInfo"),
          },
        })
        .then((res) => {
          for (let v in res.data.data) {
            if (Object.prototype.hasOwnProperty.call(res.data.data, v)) {
              for (let i = 0; i < _this.tableData.length; i++) {
                if (_this.tableData[i].version === v)
                  _this.$set(_this.tableData[i], "biPro", res.data.data[v]);
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
.status-tag {
  display: flex;
  justify-content: center;
}
</style>