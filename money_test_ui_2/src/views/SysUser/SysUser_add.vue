<script setup>
import Header from '../SysUser/head/head_index.vue'
import Footer from '../SysUser/footer/Footer_index.vue'

import axios from 'axios'
import { ref, onMounted } from "vue";
import {ElMessage, ElMessageBox} from "element-plus";
import {Delete} from "@element-plus/icons-vue";

//从头文件中获取token信息
const token = sessionStorage.getItem("token");
// 用于存储类别数据
const categories = ref([]);

// 获取类别数据的函数
const fetchCategories = async () => {
  try {
    //向后端发送get请求，获取数据
    const response = await axios.get('http://localhost:8000/project/category', {
      headers: {
        Authorization: token,
      }
    });
    //接收后端返回的值
    categories.value = response.data.all_category;
  } catch (error) {
    console.error('获取类别失败:', error);
  }
};

// 在组件加载时自动调用 API
onMounted(() => {
  fetchCategories();
});

//点击添加类别的按钮，出现弹窗，
const category_add=()=>{
  ElMessageBox.prompt('请输入要添加的类别名','添加类别',{
    confirmButtonText:'确认添加',
    cancelButtonText:"取消",
    inputErrorMessage:'请输入类别名！',
    inputValidator:(value)=>{
      if(!value){
        return '请输入类别';
      }
      return true;
    },
  }).then(async (value) => {
    try {
      //进行post请求
      const response = await axios.post('http://localhost:8000/project/category',{
        'operate':'添加类名',
        'category_name':value.value,
      },{
        headers: {
          Authorization: token,
        }
      });
      let data = response.data;
      if (data.code===200){
        //显示类别添加成功信息
        ElMessage.success(data.info)
        //延迟刷新界面
        setTimeout(()=>{
          location.reload();
        }, 1000);
      }else {
        ElMessage.error(data.info);
      }
    }catch (error){
      ElMessage.error(error)
    }
  }).catch(() => {
    ElMessage({
      type: 'info',
      message: '输入取消',
    })
  })
}
//默认删除按钮不显示
const if_show = ref(false)
const category_delete=()=>{
  if_show.value = !if_show.value
}

//进行删除操作
const delete_op=(category)=>{
  ElMessageBox.confirm(
      `您确定要删除类别 "${category.category_name}" 吗？`,
      '确认删除',
      {
        confirmButtonText:'确认',
        cancelButtonText:'取消',
        type:'warning',
      }
  ).then(async ()=>{
    try{
      //进行post请求
      const response = await axios.post('http://localhost:8000/project/category',{
        'operate':'删除类名',
        'category_name':category.category_name,
      },{
        headers: {
          Authorization: token,
        }
      });
      let data = response.data
      if (data.code===200){
        //显示类别删除成功信息
        ElMessage.success(data.info)
        //延迟刷新界面
        setTimeout(()=>{
          location.reload();
        }, 2000);
      }else {
        ElMessage.error(data.info);
      }
    }catch(error){
      ElMessage.error(error)
    }
  }).catch(()=>{
    ElMessage({
      type: 'info',
      message: '取消删除',
    })
  })
}
</script>

<template>
  <div class="common-layout">
    <el-container>
      <!-- 头部 -->
      <el-header><Header /></el-header>

      <!-- 主体内容 -->
      <el-main>
        <h2 class="title">项目类别</h2>
        <div class="btn">
          <el-button type="primary" round @click="category_add">添加类别</el-button>
          <el-button v-if="!if_show" type="danger" round @click="category_delete">删除类别</el-button>
          <el-button v-if="if_show" type="info" round @click="category_delete">返回</el-button>
        </div>
        <!-- 卡片容器 -->
        <div class="card-container">
          <el-card
            v-if="categories"
            v-for="category in categories"
            :key="category.id"
            class="category-card"
            shadow="hover"
          >
            <h3 class="category-name">
              {{ category.category_name }}
              <el-button @click="delete_op(category)" v-if="if_show" type="danger" :icon="Delete" circle size="small" />
            </h3>

          </el-card>
          <!-- 如果没有数据 -->
          <div v-else class="empty-message">
            当前没有类别
          </div>
        </div>
      </el-main>

      <!-- 页脚 -->
      <el-footer><Footer /></el-footer>
    </el-container>
  </div>
</template>

<style scoped>
/* 全局布局 */
.common-layout {
  background-color: #f5f5f5;
  min-height: 100vh;
}

/* 标题样式 */
.title {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  margin: 20px 0;
  color: #333;
}

/* 卡片容器布局 */
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  padding: 20px;
}

/* 卡片样式 */
.category-card {
  width: 320px;
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.category-card:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

/* 卡片内部文字样式 */
.category-name {
  font-size: 18px;
  font-weight: 500;
  text-align: center;
  margin: 10px 0;
  color: #666;
}

/* 空数据提示 */
.empty-message {
  font-size: 16px;
  color: #999;
  text-align: center;
  margin: 20px 0;
}
</style>
