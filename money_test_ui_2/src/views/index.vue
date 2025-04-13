<script setup>
import Header from '@/views/SysUser/head/user_head_index.vue'
import Footer from '@/views/SysUser/footer/Footer_index.vue'
import {PictureFilled, Search} from "@element-plus/icons-vue";
import axios from "axios";
import {onMounted, ref} from "vue";
import router from "@/router";
import {ElMessage} from "element-plus";

// 用于存储项目信息
const project = ref([]);
// 设置图片基础路径
const base_squareUrl = "http://localhost:8000/media/project_images/";
// 从头文件中获取 token 信息
const token = sessionStorage.getItem("token");
//计算进度
const calculateProgress = (item) =>Math.min(Math.floor((item.raised_amount / item.goal_amount) * 100), 100);
//计算项目剩余天数
const lastday = (item)=>{
  const now = new Date();
  const end = new Date(item.end_time);
  const difference = end-now;
  const remainingDays = Math.ceil(difference / (1000 * 60 * 60 * 24)); // 转为天数
  return remainingDays > 0 ? remainingDays : 0; // 剩余天数不能小于 0
}

// 获取项目信息的函数
const fetchProject = async () => {
  try {
    const response = await axios.get('http://localhost:8000/project/getproject-pass', {
      headers: {
        Authorization: token,
      }
    });
    project.value = response.data.data['projects'];
  } catch (error) {
    console.log("获取项目信息失败");
  }
};
//自动检查项目剩余天数，更新项目状态
const check_project = async () => {
  for (const item of project.value) {
    const now = new Date();
    const end = new Date(item.end_time);
    const difference = end-now;
    if(item.status===2){
      break;
    }
    if (difference <= 0) {
      const response = await axios.post('http://localhost:8000/project/turn_project', {
        project_id: item.project_id,
      },{
        headers: {
          Authorization: token,
        }
      })
      if(response.data.code !== 200){
        ElMessage.error(response.data.info);
      }
    }
  }
}
// 用于存储类别数据
const categories = ref([]);
//选中的el-option的value属性值
const el_option_value = ref(null)
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
//事件监听
const select_project_by_category = (value) => {
  if(value){
    router.push({name:'project-category',params:{id:value}});
  }
}
// 自动化调用 API
onMounted(async () => {
  await fetchProject();
  check_project();
  fetchCategories();
});

//点击卡片跳转到详情页
const goto_projectDetail=(project_id)=>{
  router.push({name:'project',params:{id:project_id}});
};
//绑定时间选择器
const project_time = ref([]);
//额度数据绑定
const MinMoney = ref(0)
const MaxMoney = ref(0)
//点击时间选择器旁边的搜索按钮后，进行项目指定时间段的查询
const search_project_by_time = async () =>{
  const timeRange = Array.isArray(project_time.value)?project_time.value:[];
  // 如果没有选择时间和额度，弹出错误提示
  if (timeRange.length === 0 && (MinMoney.value === 0 && MaxMoney.value === 0)) {
    location.reload();
    return;
  }
  if (MinMoney.value > MaxMoney.value) {
    ElMessage.error('最低额度不能大于最高额度！');
    return;
  }
  //传递信息进行操作
  let response = await axios.post('http://localhost:8000/project_operate/search-ByTime', {
        start_time: timeRange.length ? timeRange[0] : null,
        end_time: timeRange.length ? timeRange[1] : null,
        category:'no',
        minMoney: MinMoney.value,
        maxMoney: MaxMoney.value,
      },{
        headers:{
          Authorization: token,
        }
      }
  );
  let data = response.data;
  if (data.code === 200 && data.data['projects'].length > 0) {
    project.value = data.data['projects'];
  }else {
    project.value = [];//清空项目数据
    ElMessage.error(data.info || '未查询到项目')
  }
}
</script>

<template>
  <!--  普通用户首页-->
  <div class="common-layout">
    <el-container>
      <el-header><Header></Header></el-header>
      <el-main>
        <div class="main-title">
          <h2 class="title-font">众筹项目</h2>共 {{project.length}} 个众筹项目
        </div>
        <div class="project-list-container">
          <div class="search_all">
            <div class="search-wrapper">
              <!-- 选择类别 -->
              <div class="select">
                <el-select
                    v-model="el_option_value"
                    placeholder="请选择类别"
                    style="width: 240px;"
                    @change="select_project_by_category"
                >
                  <el-option
                      v-for="item in categories"
                      :key="item.category_id"
                      :value="item.category_id"
                      :label="item.category_name"
                  ></el-option>
                </el-select>
              </div>

              <!-- 选择时间段 -->
              <div class="date-picker">
                <el-date-picker
                    v-model="project_time"
                    type="datetimerange"
                    start-placeholder="项目开始时间"
                    end-placeholder="项目结束时间"
                    value-format="YYYY-MM-DD HH:mm:ss"
                    format="YYYY-MM-DD HH:mm:ss"
                    style="width: 250px;"
                />
              </div>

              <!-- 众筹额度选择框 -->
              <div class="money-range">
                <el-input-number v-model="MinMoney" :min="0" :step="1000" label="最低额度" style="width: 150px;">
                  <template #prefix>
                    <span>￥</span>
                  </template>
                </el-input-number>
                <span style="padding: 10px;">-</span>
                <el-input-number v-model="MaxMoney" :min="0" :step="1000" label="最高额度" style="width: 150px;">
                  <template #prefix>
                    <span>￥</span>
                  </template>
                </el-input-number>
              </div>

              <!-- 查询按钮 -->
              <el-button
                  type="primary"
                  :icon="Search"
                  @click="search_project_by_time"
                  style="width: 150px; padding: 10px 20px; margin-left: 20px; height: 40px;"
              >
                查询
              </el-button>
            </div>
          </div>
          <!--          使用css Grid布局-->
          <div class="grid-container">
            <!--            项目卡片-->
            <div v-for="item in project" :key="item.project_id" class="grid-item">
              <el-card shadow="hover" class="project-card" @click="goto_projectDetail(item.project_id)">
                <template #header>
                  <el-image
                      v-if="item.image"
                      :src="base_squareUrl + item.image"
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
                </template>
                <div class="d-flex-1 align-items-center">
                  <span class="category-badge">{{item.category}}</span>
                  <h4 class="project-title">{{item.title}}</h4>
                </div>
                <el-progress :percentage="calculateProgress(item)" :show-text="false"></el-progress>
                <div v-if="item.description" class="project-description">
                  {{item.description}}
                </div>
                <div v-else class="project-description">
                  该项目暂无描述
                </div>
                <div class="d-flex justify-content-between align-items-center">
                  <span class="text-success">￥{{ item.goal_amount }}</span>
                  <span class="text-info">剩余&nbsp;{{lastday(item)}}&nbsp;天</span>
                </div>
                <div class="chouji-font">已筹集: ￥{{ item.raised_amount }}</div>
                <hr />
                <div class="card-bottom">
                  <span class="project-owner">
                    发起人: {{ item.owner.username }}
                  </span>
                  <span class="zhichi">{{item.kanhao}}人看好</span>
                </div>
              </el-card>
            </div>
          </div>
        </div>
        <!--          没有数据时的提示-->
        <div v-if="!project.length">
          当前没有项目
        </div>
      </el-main>
      <el-footer><Footer></Footer></el-footer>
    </el-container>
  </div>
</template>

<style scoped>
.project-list-container{
  padding: 10px;
  background-color: #f2f6fc;
}
.grid-container{
  display: grid;
  gap: 20px;/* 卡片间距 */
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* 动态调整列数 */
}
.grid-item {
  display: flex;
  justify-content: center;

}

.project-card {
  width: 100%;
  max-width: 300px;
  cursor: pointer;
}

.project-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
}
.d-flex-1{
  display: flex;
  justify-content:flex-start;
  padding: 5px;
}
.category-badge {
  background-color: #28a745; /* 绿色背景 */
  color: #fff; /* 白色字体 */
  padding: 0.2em 0.6em;
  border-radius: 0.25em;
  font-size: 1.0em;
  font-weight: bold;
  display: inline-block;
}
/* 标题样式 */
.project-title {
  font-size: 1.2em;
  font-weight: bold;
  margin-left: 5px;
}
/* 间距调整 */
.me-2 {
  margin-right: 0.5rem; /* 添加右侧间距 */
}
.project-description{
  display: flex;
  justify-content: flex-start;
  color: #666a7e;
  padding: 5px;
}
.d-flex{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px;
}
.text-success{
  color: #1b8855;
  justify-content: flex-start;
  font-weight: bold;
}
.text-info{
  color: #666a7e;
}
.chouji-font{
  display: flex;
  justify-content: flex-start;
  color: #666a7e;
  padding: 5px;
}
.card-bottom{
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.project-owner{
  justify-content: flex-start;
  padding: 5px;
  color: #666a7e;
}
.zhichi{
  color: #666a7e;
}
.search_all {
  padding: 20px;
  margin-top: 20px;
  margin-bottom: 20px;
}

.search-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.search-wrapper > div {
  margin-right: 20px;
  margin-bottom: 10px;
}

.select, .date-picker, .money-range {
  display: inline-block;
}

.el-select, .el-date-picker, .el-input-number {
  width: 100%;
}

.el-button {
  font-size: 16px;
  font-weight: bold;
  letter-spacing: 1px;
}

.el-button:hover {
  background-color: #66b1ff;
  border-color: #66b1ff;
}
.title-font{
  font-size: 1.2em;
  padding-right: 20px;
}
.main-title{
  display: flex;
  padding-bottom: 20px;
}
.search_all {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin-top: 20px;
}
</style>