<script setup>
import { useRoute } from "vue-router";
import { onMounted, ref } from "vue";
import axios from "axios";
import { ElMessage } from "element-plus";
import Header from "../SysUser/head/head_index.vue";
import {PictureFilled} from "@element-plus/icons-vue";

// 设置图片基础路径
const base_squareUrl = "http://localhost:8000/media/project_images/";
const base_avatar = "http://localhost:8000/media/userAvatar/";

// 从 sessionStorage 中获取 token 信息
const token = sessionStorage.getItem("token");

// 存储获取的项目信息
const project_infomation = ref([]);
const route = useRoute();
const projectId = ref(route.params.id); // 当前项目 ID

// 获取项目信息的方法
const fetchinfomation = async () => {
  try {
    const response = await axios.post("http://localhost:8080/project/getproject-pass", {
      'project_id': projectId.value,
    }, {
      headers: {
        Authorization: token, // 如果后端需要验证
      },
    });
    const data = response.data;
    console.log(data);
    if (data.code === 200) {
      // 如果获取后端返回成功信息，直接存入数据
      project_infomation.value = data.data;
      console.log(project_infomation.value);
    } else {
      ElMessage.error(data.info);
    }
  } catch (err) {
    console.error(err);
    ElMessage.error("网络连接错误，请稍后再试");
  }
};

// 在组件挂载时调用
onMounted(() => {
  fetchinfomation();
});
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <Header/>
      </el-header>
      <el-main>
        {{ projectId }}
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>

</style>
