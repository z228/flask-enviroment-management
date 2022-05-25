<template>
  <div class="m-contain" v-if="this.$store.state.userInfo==='admin' ||this.$store.state.userInfo==='曾成龙'||this.$store.state.userInfo==='zcl'">
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-script"></i>定时任务
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div>
      <el-card>
        <div class="script_select all codeEdit">
          <el-select
            v-model="cmEditorMode"
            placeholder="请选择代码格式"
            @change="onEditorModeChange"
          >
            <el-option
              v-for="item in cmEditorModeOptions"
              :key="item"
              :label="item"
              :value="item"
            ></el-option>
          </el-select>
        </div>
        <div class="name_input all codeEdit">
          <el-input
            placeholder="请输入脚本名"
            v-model="script_name"
            maxlength="10"
            show-word-limit
            clearable
          >
          </el-input>
        </div>
        <div class="script_input all codeEdit">
          <el-select v-model="cmTheme" placeholder="请选择主题">
            <el-option
              v-for="item in cmThemeOptions"
              :key="item"
              :label="item"
              :value="item"
            ></el-option>
          </el-select>
        </div>

        <div
          class="code-mirror-div all"
          style="border: 1px solid #dcdfe6; margin-top: 60px"
        >
          <code-mirror-editor
            ref="cmEditor"
            :cmTheme="cmTheme"
            :cmMode="cmMode"
            :autoFormatJson="autoFormatJson"
            :jsonIndentation="jsonIndentation"
          ></code-mirror-editor>
        </div>
        <div class="all btn_ent">
          <el-button type="primary" @click="saveTask()">保存</el-button>
        </div>
      </el-card>
      <el-card class="all">
        <el-empty
          description="暂时没有脚本"
          v-show="!this.status.hasFountScript"
          class="all"
        ></el-empty>

        <el-table
          class="all"
          :data="tableData"
          border
          v-show="this.status.hasFountScript"
          style="width: 100%"
        >
          <el-table-column fixed prop="name" label="脚本名"> </el-table-column>
          <el-table-column prop="cycle" label="执行周期"> </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button @click="execute(scope.row)" type="text" size="small"
                >执行</el-button
              >
              <el-button @click="editScript(scope.row)" type="text" size="small"
                >编辑</el-button
              >
              <el-button
                @click="deleteScript(scope.row, scope.$index)"
                type="text"
                size="small"
                >删除</el-button
              >
            </template>
          </el-table-column>
        </el-table>
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
      cmTheme: "idea", // codeMirror主题
      // codeMirror主题选项
      cmThemeOptions: [
        "default",
        "3024-day",
        "3024-night",
        "abcdef",
        "ambiance",
        "ayu-dark",
        "ayu-mirage",
        "base16-dark",
        "base16-light",
        "bespin",
        "blackboard",
        "cobalt",
        "colorforth",
        "darcula",
        "dracula",
        "duotone-dark",
        "duotone-light",
        "eclipse",
        "elegant",
        "erlang-dark",
        "gruvbox-dark",
        "hopscotch",
        "icecoder",
        "idea",
        "isotope",
        "lesser-dark",
        "liquibyte",
        "lucario",
        "material",
        "material-darker",
        "material-palenight",
        "material-ocean",
        "mbo",
        "mdn-like",
        "midnight",
        "monokai",
        "moxer",
        "neat",
        "neo",
        "night",
        "nord",
        "oceanic-next",
        "panda-syntax",
        "paraiso-dark",
        "paraiso-light",
        "pastel-on-dark",
        "railscasts",
        "rubyblue",
        "seti",
        "shadowfox",
        "solarized dark",
        "solarized light",
        "the-matrix",
        "tomorrow-night-bright",
        "tomorrow-night-eighties",
        "ttcn",
        "twilight",
        "vibrant-ink",
        "xq-dark",
        "xq-light",
        "yeti",
        "yonce",
        "zenburn",
      ],
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
      tableData: [],
      options: [
        {
          value: "Python",
          label: "Python脚本",
        },
      ],
      value: "Python",
      textarea: "",
      script_name: "",
      status: {
        hasFountScript: false,
      },
    };
  },
  created() {
    this.getAllTask();
  },
  methods: {
    getAllTask() {
      this.tableData.splice(0, this.tableData.length);
      console.log(this.tableData);
      this.$set(this.status, "hasFountScript", false);
      let _this = this;
      this.$axios
        .get("http://localhost:5000/productJar/allScript")
        .then((res) => {
          let data = res.data.data;
          for (let script in data) {
            if (Object.prototype.hasOwnProperty.call(data, script)) {
              _this.tableData.push({
                name: res.data.data[script].name,
                cycle: "",
              });
            }
          }
          if (_this.tableData !== [])
            this.$set(this.status, "hasFountScript", true);
        });
    },
    execute(row) {
      this.$axios
        .post("http://localhost:5000/productJar/execute", {
          name: row.name,
        })
        .then((res) => {
          if (res.data.code === 200) {
            this.$message.success(res.data.data);
          }
          else{
            this.$message.info(res.data.data);
          }
        });
    },
    editScript(row) {},
    saveTask() {
      let _this = this;
      let end = ".json";
      switch (this.cmMode) {
        case "application/json":
          end = ".json";
          break;
        case "sql":
          end = ".sql";
          break;
        case "javascript":
          end = ".js";
          break;
        case "xml":
          end = ".xml";
          break;
        case "css":
          end = ".css";
          break;
        case "html":
          end = ".html";
          break;
        case "yaml":
          end = ".yaml";
          break;
        case "markdown":
          end = ".md";
          break;
        case "python":
          end = ".py";
          break;
        default:
          end = ".json";
      }
      let EditorValue = this.$refs.cmEditor.getValue();
      this.$axios
        .post("http://localhost:5000/productJar/saveScript", {
          content: EditorValue,
          type: this.cmMode,
          name: _this.script_name,
        })
        .then((res) => {
          if (res.data.code === 200) {
            this.$message.success(res.data.data);
            this.tableData.push({
              name: _this.script_name + end,
              cycle: "",
            });
            _this.script_name = "";
            this.$refs.cmEditor.setValue("");
          }
        });
    },
    deleteScript(row, index) {
      console.log(index);
      this.$axios
        .post("http://localhost:5000/productJar/delete", {
          name: row.name,
        })
        .then((res) => {
          if (res.data.code === 200) {
            this.$message.success(res.data.data);
            console.log(index);
            this.tableData.splice(index, 1);
          }
        });
    },
    onEditorModeChange(value) {
      switch (value) {
        case "json":
          this.cmMode = "application/json";

          break;

        case "sql":
          this.cmMode = "sql";

          break;

        case "javascript":
          this.cmMode = "javascript";

          break;

        case "xml":
          this.cmMode = "xml";

          break;

        case "css":
          this.cmMode = "css";

          break;

        case "html":
          this.cmMode = "htmlmixed";

          break;

        case "yaml":
          this.cmMode = "yaml";

          break;

        case "markdown":
          this.cmMode = "markdown";

          break;

        case "python":
          this.cmMode = "python";

          break;

        default:
          this.cmMode = "application/json";
      }
    },

    // 修改样式（不推荐，建议参考<style>中的样式，提前配置好样式）

    setStyle() {
      let styleStr =
        "position: absolute; top: 80px; left: 50px; right: 200px; bottom: 20px; padding: 2px; height: auto;";

      this.$refs.cmEditor.setStyle(styleStr);
    },

    //获取内容

    getValue() {
      let content = this.$refs.cmEditor.getValue();

      console.log(content);
    },

    //修改内容

    setValue() {
      let jsonValue = {
        name: "laiyu",

        addr: "广东省深圳市",

        other: "nothing",

        tel: "168888888",

        intro: [{ item1: "item1" }],
      };

      this.$refs.cmEditor.setValue(JSON.stringify(jsonValue));
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