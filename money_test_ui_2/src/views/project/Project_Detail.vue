<script setup>
import { useRoute } from "vue-router";
import { onMounted, ref } from "vue";
import Header from "../SysUser/head/head_index.vue";
import user_Header from "../SysUser/head/user_head_index.vue";
import {ElMessage, ElMessageBox} from "element-plus";
import {ChatSquare, Edit, PictureFilled, UserFilled} from "@element-plus/icons-vue";
import dayjs from "dayjs";
import router from "@/router";
import axios from "@/utils/axios";
// 从头文件中获取用户信息,这只是一个副本，对其进行的修改不会映射到头文件中
const current = JSON.parse(sessionStorage.getItem("user")) || {
  username: '',
  user_email: '',
  phonenumber: '',
  user_birthday: '',
  remark: '',
  identify:''
};

// 日期格式化显示
const formateDate = (item) => {
  return dayjs(item).format("YYYY年MM月DD日 HH:mm:ss");
};

// 当前项目 ID
const route = useRoute();
const projectId = ref(route.params.id); // 动态路由参数

// 项目信息存储
const project = ref(null); // 初始化为 null，待数据加载后赋值

// API Token
const token = sessionStorage.getItem("token");

// 设置图片基础路径
const base_squareUrl = "http://localhost:8000/media/project_images/";
const base_avatar = "http://localhost:8000/media/userAvatar/";

// 获取项目信息
const fetch_project = async () => {
  try {
    const response = await axios.post(
        "/project/getproject-pass",
        {
          project_id: Number(projectId.value),
        },
        {
          headers: {
            Authorization: token,
          }
        }
    );
    const data = response.data;
    if (data.code === 200) {
      project.value = data.data.project; // 将后端返回的项目数据赋值给 `project`
    } else {
      ElMessage.error(data.info);
    }
  } catch (error) {
    console.error(error);
    ElMessage.error("获取项目信息失败：" + error.message);
  }
};

// 计算进度
const calculateProgress = (item) =>
    Math.min(Math.floor((item.raised_amount / item.goal_amount) * 100), 100);

// 计算项目剩余天数
const lastday = (item) => {
  const now = new Date();
  const end = new Date(item.end_time);
  const difference = end - now;
  const remainingDays = Math.ceil(difference / (1000 * 60 * 60 * 24)); // 转为天数
  return remainingDays > 0 ? remainingDays : 0; // 剩余天数不能小于 0
};

// 跳转到投资详情页
const go_to_investment = () => {
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
  router.push({ name: "project_investment", params: { id: Number(projectId.value) } });
};

// 看好按钮设置
const if_red = ref(false); // 喜爱状态

// 初始化看好按钮状态
const begin_if_red = async () => {
  if(!current.id){
    return;
  }
  try {
    const response = await axios.post(
        "/project_operate/love",
        {
          project_id: Number(projectId.value),
          user_id: JSON.parse(sessionStorage.getItem("user")).id,
          oprate: "get_love",
        },
        {
          headers: {
            Authorization: token,
          }
        }
    );
    const data = response.data;
    if (data.code === 200) {
      if_red.value = false; // 没有喜爱记录
    } else {
      if_red.value = true; // 已有喜爱记录
    }
  } catch (e) {
    console.error(e);
    ElMessage.error("获取看好状态失败：" + e.message);
  }
};

// 切换看好状态
const turn_red = async () => {
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
  // 更新本地状态
  if_red.value = !if_red.value;
  try {
    const response = await axios.post(
        "/project_operate/love",
        {
          project_id: Number(projectId.value),
          user_id: JSON.parse(sessionStorage.getItem("user")).id,
          oprate: "turn_love",
        },
        {
          headers: {
            Authorization: token,
          }
        }
    );
    const data = response.data;
    if (data.code === 200) {
      ElMessage.success(data.info);
    } else {
      ElMessage.error(data.info);
    }
  } catch (e) {
    console.error(e);
    ElMessage.error("切换看好状态失败：" + e.message);
  }
};
//存储项目评论
let comments = ref([])
//获取项目评论
const get_comment = async () => {
  try {
    let response = await axios.get('/project_operate/get_comment?project_id=' + Number(projectId.value),
        {
          headers: {
            Authorization: token,
          }
        }
    );
    let data = response.data;
    if(data.code===200){
      comments.value = data.data
    }
  }catch (e) {
    ElMessage.error(e.message);
  }
}
// 页面加载时获取数据
onMounted(() => {
  fetch_project(); // 获取项目信息
  begin_if_red(); // 初始化看好状态
  get_comment();//初始化项目评论
});
//存储评论内容
const comment = ref('')
//评论发布功能实现
const pub_comment =async () => {
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
  //判断评论是否为空，或者只包含空格
  if(!comment.value){
    ElMessage.error('评论内容不能为空!')
    return;
  }
  //如果评论内容不为空，则进行评论的添加
  try {
    let response = await axios.post('/project_operate/pub_comment',{
      project_id: Number(projectId.value),
      user_id:JSON.parse(sessionStorage.getItem("user")).id,
      connect:comment.value,
    },{
      headers: {
        Authorization: token,
      }
    });
    let data = response.data;
    if (data.code === 200) {
      ElMessage.success(data.info);
      setTimeout(()=>{
        location.reload()
      },1000)
    }else {
      ElMessage.error('出现错误，稍后重试！！')
    }
  }catch (e){
    console.error(e);
    ElMessage.error(e.message);
  }
}

const activeCommentId=ref(null);//用于记录当前打开评论的id
const response_comment = (commentId)=>{
  if(activeCommentId.value === commentId){
    //如果当前点击的已经是打开的评论，则关闭
    activeCommentId.value = null;
  }else {
    activeCommentId.value = commentId;
  }
}
//存储回复评论
const reply_comment = ref('')
//回复评论功能实现,传入的参数是回复评论的id
const response_comment_yes = async (commentId) => {
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
  if(!reply_comment.value){
    ElMessage.error('评论内容不能为空！')
    return;
  }
  try{
    let response = await axios.post('/project_operate/reply_comment',
        {
          user_id:JSON.parse(sessionStorage.getItem("user")).id,
          comment_id:commentId,
          content:reply_comment.value,
        },{
          headers: {
            Authorization: token,
          }
        });
    let data = response.data;
    if (data.code === 200){
      ElMessage.success(data.info);
      setTimeout(()=>{
        location.reload();
      },1000);
    }else {
      ElMessage.error(data.info);
    }
  }catch (e) {
    ElMessage.error(e.message)
  }
}
//进行回复评论的功能实现
const response_reply_comment = ref(null);
const queren_response = async (comment_reply_ID) =>{
  if(response_reply_comment.value === comment_reply_ID){
    //如果当前点击的已经是打开的评论，则关闭
    response_reply_comment.value = null;
  }else {
    response_reply_comment.value = comment_reply_ID;
  }
}
//存储评论
const huifu = ref('')
//回复评论功能实现
const huifupingl = async (commentId,comment_reply_id) => {
  if(!huifu.value){
    ElMessage.error('评论内容不能为空！')
    return;
  }
  try {
    let response = await axios.post('/project_operate/reply_comment',{
      user_id:JSON.parse(sessionStorage.getItem("user")).id,
      comment_id:commentId,
      comment_reply_id:comment_reply_id,
      content:huifu.value
    },{
      headers: {
        Authorization: token,
      }
    });
    let data = response.data;
    if (data.code === 200){
      ElMessage.success(data.info)
      setTimeout(()=>{
        location.reload();
      },1000);
    }else {
      ElMessage.error(data.info)
    }
  }catch (e){
    ElMessage.error(e.message)
  }
}
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
      const matches = contentDisposition.match(/filename="(.+)"/);
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
      <el-header v-if="current.identify==='manager'">
        <Header />
      </el-header>
      <el-header v-else>
        <user_Header></user_Header>
      </el-header>
      <el-main>
        <div v-if="project" class="project-detail-container">
          <div class="container">
            <div class="row">
              <!-- 项目信息左侧 -->
              <div class="col-lg-7">
                <el-image
                    v-if="project.image"
                    :src="base_squareUrl + project.image"
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
              </div>

              <!-- 项目信息右侧 -->
              <div class="col-lg-5">
                <div class="main-infomation">
                  <!-- 标题和分类标签 -->
                  <div class="project-header">
                    <span class="category-badge">{{ project.category }}</span>
                    <span class="project-title">{{ project.title }}</span>
                  </div>

                  <!-- 发起人信息 -->
                  <div class="author">
                    <el-avatar
                        v-if="project.owner.avatar"
                        :src="base_avatar + project.owner.avatar"
                        size="60"
                        shape="circle"
                        class="user-avatar"
                    ></el-avatar>
                    <el-avatar
                        v-else
                        size="60"
                        class="user-avatar"
                        :icon="UserFilled"
                    />
                    &nbsp;&nbsp;{{ project.owner.username }}
                  </div>
                  <div class="description_my">
                    <span v-if="!project.description">当前项目无详细描述</span>
                    <span>项目描述:{{project.description}}</span>
                  </div>
                  <div class="project_resouces">
                    <span v-if="project.resources">
                      项目资源:<el-button @click="downloadResource(project.resources)">点击下载</el-button>
                    </span>
                    <span v-else>
                      当前项目无项目资源
                    </span>
                  </div>
                  <!-- 筹集金额与进度条 -->
                  <div class="money">
                    <span>已筹: ￥{{ project.raised_amount }}</span>
                    <el-progress :percentage="calculateProgress(project)" />
                    <span>目标金额: ￥{{ project.goal_amount }}</span>
                  </div>

                  <!-- 剩余天数与支持按钮 -->
                  <div class="project-info">
                    <div class="remaining-days">
                      剩余天数: {{ lastday(project) }} 天
                      {{project.kanhao}}人看好
                    </div>
                    <div class="kanhao_xiai">
                      <el-button size="large" type="success" @click="go_to_investment">立即支持</el-button>
                      <div class="project-help">
                        <el-button v-if="!if_red" @click="turn_red">
                          <svg t="1733368201613" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4279" width="25" height="25"><path d="M667.786667 117.333333C832.864 117.333333 938.666667 249.706667 938.666667 427.861333c0 138.250667-125.098667 290.506667-371.573334 461.589334a96.768 96.768 0 0 1-110.186666 0C210.432 718.368 85.333333 566.112 85.333333 427.861333 85.333333 249.706667 191.136 117.333333 356.213333 117.333333c59.616 0 100.053333 20.832 155.786667 68.096C567.744 138.176 608.170667 117.333333 667.786667 117.333333z m0 63.146667c-41.44 0-70.261333 15.189333-116.96 55.04-2.165333 1.845333-14.4 12.373333-17.941334 15.381333a32.32 32.32 0 0 1-41.770666 0c-3.541333-3.018667-15.776-13.536-17.941334-15.381333-46.698667-39.850667-75.52-55.04-116.96-55.04C230.186667 180.48 149.333333 281.258667 149.333333 426.698667 149.333333 537.6 262.858667 675.242667 493.632 834.826667a32.352 32.352 0 0 0 36.736 0C761.141333 675.253333 874.666667 537.6 874.666667 426.698667c0-145.44-80.853333-246.218667-206.88-246.218667z" fill="#000000" p-id="4280"></path></svg>
                        </el-button>
                        <el-button v-else @click="turn_red">
                          <svg t="1733381045058" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4426" width="25" height="25"><path d="M512 901.746939c-13.583673 0-26.122449-4.179592-37.093878-13.061225-8.881633-7.314286-225.697959-175.020408-312.424489-311.379592C133.746939 532.37551 94.040816 471.24898 94.040816 384.522449c0-144.718367 108.146939-262.269388 240.326531-262.269388 67.395918 0 131.657143 30.82449 177.632653 84.636735 45.453061-54.334694 109.191837-84.636735 177.110204-84.636735 132.702041 0 240.326531 117.55102 240.326531 262.269388 0 85.159184-37.093878 143.673469-67.395919 191.216327l-1.044898 1.567346c-86.726531 136.359184-303.542857 304.587755-312.424489 311.379592-10.44898 8.359184-22.987755 13.061224-36.571429 13.061225z" fill="#E5404F" p-id="4427"></path></svg>
                        </el-button>
                        看好
                      </div>
                    </div>
                    <hr />
                  </div>

                  <!-- 项目详细描述 -->
                  <div class="project-summary">
                    此项目于 {{ formateDate(project.start_time) }} 开始，需在 {{ formateDate(project.end_time) }} 前达到目标金额才能成功。
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- 评论区域 -->
          <div class="comment-section">
            <div class="comments-count">评论共 {{comments.length}} 条</div>
            <hr />
            <h4>发表评论</h4>
            <el-input
                style="width: 100%"
                :autosize="{ minRows: 2, maxRows: 4 }"
                type="textarea"
                placeholder="请输入评论..."
                v-model="comment"
            />
            <el-button size="large" type="success" @click="pub_comment">发布评论</el-button>
            <hr/>
            <!--           下面显示当前项目评论-->
            <div class="comments-list">
              <div v-for="item in comments" :key="item.id" class="comment-item">
                <div class="comment-header">
                  <el-avatar
                      v-if="item.user.avatar"
                      :src="base_avatar+item.user.avatar"
                      size="40"
                      shape='circle'
                      class="user-avatar-2"
                  />
                  <el-avatar
                      v-else
                      size="40"
                      shape="circle"
                      :icon="UserFilled"
                      class="user-avatar-2"
                  ></el-avatar>
                  <span class="username">{{ item.user.username }}</span>
                  <!--                  判断是否为作者-->
                  <span v-if="item.user.id === project.owner.id" class="biaoqian">项目发起者</span>
                  <span class="comment-time">{{ formateDate(item.comment_date) }}</span>
                </div>
                <div class="comment-content">
                  {{ item.content }}
                  <div class="huifu">
                    <el-button type="primary" :icon="ChatSquare" @click="response_comment(item.comment_id)">
                      {{activeCommentId === item.comment_id ? '收起':'回复'}}
                    </el-button>
                  </div>
                </div>
                <!--                回复表单-->
                <div class="reply-form" v-if="activeCommentId === item.comment_id">
                  <el-input
                      style="width: 100%"
                      :autosize="{ minRows: 2, maxRows: 4 }"
                      type="textarea"
                      :placeholder="'回复: '+ item.user.username"
                      class="reply_form"
                      v-model="reply_comment"
                  />
                  <el-button size="default" type="primary" round @click="response_comment_yes(item.comment_id)">评论</el-button>
                </div>
                <!--                回复列表-->
                <hr/>
                <div class="replies" v-if="item.replies && item.replies.length">
                  <div class="reply" v-for="reply in item.replies" :key="reply.comment_reply_id">
                    <div class="comment-header-2">
                      <el-avatar
                          v-if="reply.user.avatar"
                          :src="base_avatar+reply.user.avatar"
                          size="40"
                          shape='circle'
                          class="user-avatar-2"
                      />
                      <el-avatar
                          v-else
                          size="40"
                          shape="circle"
                          :icon="UserFilled"
                          class="user-avatar-2"
                      ></el-avatar>
                      <span class="username" v-if="reply.parent == null">{{ reply.user.username }}&nbsp;回复&nbsp;{{item.user.username}}</span>
                      <span class="username" v-else>{{ reply.user.username }}&nbsp;回复&nbsp;{{reply.parent_user_name}}</span>
                      <!--                  判断是否为作者-->
                      <span v-if="reply.user.id === project.owner.id" class="biaoqian">项目发起者</span>
                      <span class="comment-time">{{ formateDate(reply.created_at) }}</span>
                    </div>
                    <div class="comment-content">
                      {{ reply.content }}
                      <div class="huifu">
                        <el-button type="primary" :icon="ChatSquare" @click="queren_response(reply.comment_reply_id)">
                          {{response_reply_comment === reply.comment_reply_id ? '收起':'回复'}}
                        </el-button>
                      </div>
                    </div>
                    <div class="reply-form" v-if="response_reply_comment === reply.comment_reply_id">
                      <el-input
                          style="width: 100%"
                          :autosize="{ minRows: 2, maxRows: 4 }"
                          type="textarea"
                          :placeholder="'回复: '+ reply.user.username"
                          class="reply_form"
                          v-model="huifu"
                      />
                      <el-button size="default" type="primary" round @click="huifupingl(item.comment_id,reply.comment_reply_id)">评论</el-button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="loading">
          <el-spin tip="加载中..." />
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>
.project-detail-container {
  margin-top: 30px;
}

.container {
  width: 100%;
  margin-right: auto;
  margin-left: auto;
}
.row{
  display: flex;
  justify-content: center;
  align-content: center;
}
.project-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
.category-badge {
  background-color: #28a745; /* 绿色背景 */
  color: #fff; /* 白色字体 */
  padding: 0.3em 0.6em;
  border-radius: 0.25em;
  font-size: 1.0em;
  font-weight: bold;
  margin-right: 10px;
}

.project-title {
  font-size: 1.8em;
  font-weight: bold;
  color: #333;
}

.money {
  font-size: 1.1em;
  margin-top: 10px;
}

.project-info {
  margin-top: 20px;
}

.remaining-days {
  font-size: 1.1em;
  font-weight: bold;
}

.project-summary {
  margin-top: 20px;
  font-size: 1.1em;
  color: #555;
}

.comment-section {
  margin-top: 30px;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  max-width: 70%;  /* 设置评论区的最大宽度 */
  margin-left: auto;
  margin-right: auto;  /* 居中评论区 */
}

.comments-count {
  font-size: 1.1em;
  color: #555;
}

.project-help {
  margin-top: 5px;
  font-size: 1.0em;
  color: #007bff;
}

.user-avatar {
  margin-right: 10px;
}
.col-lg-7{
  margin: 5px;
  max-height: 350px;
}
.project-image {
  width: auto;
  height: 100%;
  object-fit: cover;
}

hr {
  margin: 20px 0;
}

.el-button {
  margin-top: 10px;
}

.el-input {
  margin-top: 10px;
}
.comment-section {
  margin-top: 30px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.comments-count {
  font-size: 1.2em;
  font-weight: bold;
  color: #333;
}

.comments-list {
  margin-top: 20px;
}
.comment-item {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f9f9f9; /* 评论区背景色 */
  border-radius: 8px; /* 评论框的圆角 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 轻微的阴影效果 */
  transition: all 0.3s ease-in-out; /* 评论项的过渡效果 */
}

.comment-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.user-avatar-2 {
  margin-right: 10px;
}

.username {
  font-weight: bold;
  margin-right: 10px;
}

.comment-time {
  font-size: 0.9em;
  color: #999;
}

.comment-content {
  margin-top: 10px;
  height: 25px;
  font-size: 1.1em;
  color: #555;
  display: flex; /* 使用弹性布局 */
  justify-content: space-between; /* 内容两端对齐 */
  align-items: center; /* 垂直方向居中对齐 */
}
.huifu {
  display: none;
  width: auto;
  border-radius: 8px;
  transition: opacity 0.3s ease, transform 0.3s ease; /* 平滑的显示和滑动效果 */
  opacity: 0;
  transform: translateY(0); /* 初始状态稍微下移 */
  margin-left:auto ;
}
.comment-content:hover .huifu{
  display: block;
  opacity: 1; /* 显示回复时的透明度 */
  transform: translateY(0); /* 回复滑动到原位 */
}
.biaoqian {
  display: inline-block;
  background-color: #28a745; /* 绿色背景 */
  color: #fff; /* 白色文字 */
  padding: 5px 10px;
  border-radius: 20px; /* 圆角效果 */
  font-size: 0.9em;
  font-weight: bold; /* 加粗字体 */
  text-align: center;
  margin-right: 8px;
  letter-spacing: 1px; /* 字间距 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 轻微阴影 */
  transition: all 0.3s ease; /* 平滑过渡效果 */
}

.biaoqian:hover {
  background-color: #218838; /* 鼠标悬停时变为深绿色 */
  transform: scale(1.1); /* 放大效果 */
}
.reply_form{
  padding-top: 10px;
}
.replies{
  width: 90%;
  margin-left: auto;
  margin-right: auto;
}
.comment-header-2{
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.description_my{
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
}
.author{
  display: flex;
  justify-content: left;
  align-items: center;
  padding-bottom: 10px;
}
.kanhao_xiai{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  margin-left: 225px;
  margin-right: 225px;
}
.project_resouces{
  display: flex;
  justify-content: space-between;
  align-items: center;
}

</style>
