<template>
  <div
    class="log-contain"
    v-if="
      this.$store.state.username === 'admin' ||
      this.$store.state.username === 'zhengsong' ||
      this.$store.state.username === 'zcl'
    "
  >
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-tickets"></i>日志
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div>
      <el-card>
        <!-- <div class="script_select all codeEdit">请输入要check的服务器ip</div> -->
        <div class="name_input all codeEdit">
          <!-- <el-form-item label="请输入要check的服务器ip:"> -->
          <el-select v-model="ip" placeholder="请选择ip">
            <el-option
              v-for="item in ip_list"
              :key="item"
              :label="item"
              :value="item"
            ></el-option>
          </el-select>
        </div>
        <div class="script_input all codeEdit">
          <el-select
            v-if="hasGetLogList === true"
            v-model="log"
            placeholder="请选择日志"
          >
            <el-option
              v-for="item in logs[ip]"
              :key="item"
              :label="item"
              :value="item"
            ></el-option>
          </el-select>
        </div>
        <div class="name_input all codeEdit">
          <el-input
            placeholder="请输入行数"
            v-model="lines"
            show-word-limit
            clearable
          >
          </el-input>
        </div>
        <div class="all codeEdit">
          <el-button type="primary" @click="getLog()">查询</el-button>
        </div>
        <div
          class="code-mirror-div all"
          style="border: 1px solid #dcdfe6; margin-top: 60px; font-size: 14px"
        >
          <code-mirror-editor
            ref="cmEditor"
            :cmTheme="cmTheme"
            :cmMode="cmMode"
            :autoFormatJson="autoFormatJson"
            :jsonIndentation="jsonIndentation"
          ></code-mirror-editor>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import Header from "../components/Header";
import bus from "../components/bus";
import CodeMirrorEditor from "../components/CodeMirrorEditor";
export default {
  name: "task",
  components: {
    CodeMirrorEditor,
  },
  // components: {Header},
  data() {
    return {
      hasGetLogList: false,
      lines: "50",
      log: "flask.log", // codeMirror主题
      // codeMirror主题选项
      logs: {},
      cmTheme: "idea",
      cmEditorMode: "python", // 编辑模式
      // 编辑模式选项
      cmEditorModeOptions: [
        "default",
        "json",
        "sql",
        "javascript",
        "css",
        "xml",
        "html",
        "yaml",
        "markdown",
        "python",
      ],
      cmMode: "python", //codeMirror模式
      jsonIndentation: 2, // json编辑模式下，json格式化缩进 支持字符或数字，最大不超过10，默认缩进2个空格
      autoFormatJson: true, // json编辑模式下，输入框失去焦点时是否自动格式化，true 开启， false 关闭
      options: [
        {
          value: "Python",
          label: "Python脚本",
        },
      ],
      value: "Python",
      textarea: "",
      ip: "192.168.0.187",
      ip_list: ["192.168.0.187","192.168.0.185","192.168.0.188"],
      status: {
        hasFountScript: false,
      },
    };
  },
  created() {
    this.getLogList();
  },
  methods: {
    getLog() {
      let _this = this;
      this.$axios
        .post("http://" + _this.ip + ":5000/log", {
          lines: _this.lines,
          log: _this.log,
        })
        .then((res) => {
          let data = res.data.log;
          this.$refs.cmEditor.setValue(data);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getLogList() {
      let _this = this;
      this.ip_list.forEach((ip) => {
        console.log(ip);
        this.$axios
          .get("http://" + ip + ":5000/loglist")
          .then((res) => {
            _this.logs[ip] = [];
            let data = res.data.logList;
            for (let i = 0; i < data.length; i++) {
              if (data[i].indexOf('.log') !==-1)
                _this.logs[ip].push(data[i]);
            }
            this.hasGetLogList = true;
            _this.logs[ip].sort()
          })
          .catch((err) => {
            console.log(err);
          });
      });
    },
  },
};
</script>

<style scoped>
.all {
  margin: 10px;
  /* float:left; */
}
.codeEdit {
  float: left;
}
.name_input {
  width: 200px;
}
/* .code-mirror-div{
  margin: 10px;
} */

.btn_ent {
}
</style>