<script setup>
import Header from '../SysUser/head/head_index.vue'
import Footer from '../SysUser/footer/Footer_index.vue'
import {computed, onMounted, ref, watch} from "vue";
import axios from '@/utils/axios'
import {Check, Delete, PictureFilled} from "@element-plus/icons-vue";
import {ElMessage, ElMessageBox} from "element-plus";
import router from "@/router";
import user_Header from "../SysUser/head/user_head_index.vue";
// 从头文件中获取用户信息
const current = JSON.parse(sessionStorage.getItem("user")) || {};
const user_id = current.id

// 从头文件中获取 token 信息
const token = sessionStorage.getItem("token");
// 用于存储项目信息
const project = ref([]);

// 获取项目信息的函数
const fetchProject = async () => {
  try {
    const response = await axios.get('/project/getproject-nopass', {
      headers: {
        Authorization: token,
      }
    });
    project.value = response.data.data['projects'];
    console.log(project.value);
  } catch (error) {
    console.log("获取项目信息失败");
  }
};

// 自动化调用 API
onMounted(() => {
  fetchProject();
});
// 设置图片基础路径
const base_squareUrl = "http://localhost:8000/media/project_images/";

//点击通过按钮时，修改项目的审查状态
//通过项目
const project_pass = async (project_id)=>{
  const response = await axios.post('/project/getproject-nopass', {
    'operate':"project_pass",
    'project_id':project_id,
    'reviewer_id':user_id,
  },{
    headers: {
      Authorization: token,
    }
  });
  let data = response.data;
  if(data.code===200){
    ElMessage.success(data.info)
    setTimeout(()=>{
      location.reload();
    },1000)
  }else {
    ElMessage.error(data.info);
  }
}
//不通过项目
const project_nopass = async (project_id)=>{
  const response = await axios.post('/project/getproject-nopass', {
    'operate':"project_no_pass",
    'project_id':project_id,
    'reviewer_id':user_id,
  },{
    headers: {
      Authorization: token,
    }
  });
  let data = response.data;
  if(data.code===200){
    ElMessage.success(data.info)
    setTimeout(()=>{
      location.reload();
    },1000)
  }else {
    ElMessage.error(data.info);
  }
}
//下载资源
const downloadResource = async (resource)=>{
  if(!current.id){
    ElMessageBox.confirm(
        '请先登录',
        {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
          type: 'warning',
        }
    )
        .then(() => {
          router.push('/login')
        })
        .catch(() => {

        })
    return;
  }
  try{
    let response = await axios.get('/project_operate/download_resource',{
      params:{file_path:resource},
      responseType:'blob',
      headers: {
        Authorization:token
      }
    });
    //提取文件名,从响应头获取
    const contentDisposition = response.headers['content-disposition'];
    let filename = 'resource_file'; // 默认文件名
    if(contentDisposition){
      const matches = contentDisposition.match(/filename\*=UTF-8''(.+)/) || contentDisposition.match(/filename="(.+)"/);
      if(matches && matches[1]){
        filename = decodeURIComponent(matches[1]);
      }
    }
    //创建下载连接
    const blob = new Blob([response.data]);
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();

    URL.revokeObjectURL(link.href);
    ElMessage.success("文件下载成功！");
  }catch (error) {
    console.error("下载失败：", error);
    ElMessage.error("文件下载失败，请稍后再试！");
  }
};
</script>

<template>
  <div class="common-layout">
    <el-container>
      <!-- 头部 -->
      <el-header class="header">
        <Header />
      </el-header>
      <!-- 主体 -->
      <el-main>
        <h2 class="title">待审核的项目</h2>

        <!-- 项目列表 -->
        <div class="project-container">
          <el-card
              v-for="item in project"
              :key="item.project_id"
              shadow="hover"
              class="project-card"
          >
            <!-- 弹出框 -->
            <el-popover
                placement="bottom"
                trigger="hover"
                width="300"
            >
              <template #reference>
                <!-- 项目卡片 -->
                <div class="project-content">
                  <!-- 项目图片 -->
                  <el-image
                      v-if="item.image"
                      :src=base_squareUrl+item.image
                      fit="cover"
                      class="project-image"
                  >
                    <template #error>
                      <div class="image-slot">
                        <el-icon><PictureFilled /></el-icon>
                      </div>
                    </template>
                  </el-image>
                  <el-image
                      v-else
                      :src="require('@/assets/默认图片.jpg')"
                      fit="cover"
                      class="project-image"
                  />
                  <!-- 简要信息 -->
                  <h3 class="project-title">{{ item.title }}</h3>
                  <p class="project-owner">发起者: {{ item.owner.username }}</p>
                  <div class="btn">
                    <el-button type="primary" :icon="Check" @click="project_pass(item.project_id)" circle />
                    <el-button type="danger" :icon="Delete" @click="project_nopass(item.project_id)" circle />
                  </div>
                </div>
              </template>

              <!-- 弹出框的详细内容 -->
              <div class="popover-detail">
                <p><strong>分类:</strong> {{ item.category }}</p>
                <p><strong>目标金额:</strong> {{ item.goal_amount }} 元</p>
                <p><strong>描述:</strong> {{ item.description }}</p>
                <span v-if="item.resources">
                      项目资源:<el-button @click="downloadResource(item.resources)">点击下载</el-button>
                    </span>
                <span v-else>
                      项目资源:当前项目无项目资源
                    </span>
              </div>
            </el-popover>
          </el-card>
        </div>

        <!-- 没有数据时的提示 -->
        <div v-if="!project.length" class="empty-message">
          当前没有需要审核的项目
        </div>

      </el-main>

      <!-- 页脚 -->
      <el-footer><Footer /></el-footer>
    </el-container>
  </div>
</template>

<style scoped>
/* 布局样式 */
.common-layout {
  background-color: #f8f9fa;
  min-height: 100vh;
  padding: 20px;
}

/* 标题样式 */
.title {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

/* 项目列表容器 */
.project-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

/* 项目卡片样式 */
.project-card {
  width: 300px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  cursor: pointer;
}

/* 项目内容样式 */
.project-content {
  text-align: center;
  padding: 15px;
}

.project-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 10px;
}

.project-title {
  font-size: 18px;
  font-weight: 600;
  margin-top: 10px;
  color: #444;
}

.project-owner {
  font-size: 14px;
  color: #666;
}

/* 弹出框详细信息 */
.popover-detail {
  text-align: left;
  font-size: 14px;
}

.popover-detail p {
  margin: 5px 0;
  color: #555;
}

/* 没有数据提示 */
.empty-message {
  font-size: 16px;
  color: #999;
  text-align: center;
  margin-top: 50px;
}

/* 分页样式 */
.pagination {
  margin-top: 20px;
  text-align: center;
}

.btn{
  display: flex;
  justify-content: center;
  padding: 10px;
}
</style>
