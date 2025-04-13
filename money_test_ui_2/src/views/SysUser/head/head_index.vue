<script setup>
import {ref} from 'vue'
import axios from '@/utils/axios'
// 从头文件中获取用户信息
const current = JSON.parse(sessionStorage.getItem("user")) || {};
// 设置基础路径
const base_squareUrl = "http://localhost:8000/media/userAvatar/";
// 获取用户名字
const name = current.username;
// 获取用户头像路径
const sqlurl = current.avatar;
const squareUrl = base_squareUrl + sqlurl;


// 获取用户的头像和名字信息
function getUserInitials(name) {
  if (!name) return "U"; // 默认显示U
  // 获取用户名首字母
  const ini = name
      .split(" ")
      .map((word) => word.charAt(0).toUpperCase())
      .join("");
  return ini;
}

import {useRoute} from "vue-router";
import {ElMessage, ElMessageBox} from "element-plus";
import router from "@/router";
import {Search} from "@element-plus/icons-vue";
const route = useRoute();
//创建响应式变量
const search_name = ref('')

//通过项目名字进行模糊查询
function find_by_name(){
    if(!search_name.value){
    ElMessage.error("请输入搜索内容！")
    return;
  }
  //跳转到搜索界面
  router.push({
    path:'/search',
    query:{
      keyword:search_name.value
    }
  })
}
//跳转到登录界面
function go_login(){
  router.push('/login');
}
//安全退出
function safe_exit(){
  //清楚头文件中关于用户的数据
  window.sessionStorage.clear();
  //然后跳转到登录界面
  router.push('/login');
}

//用户中心
function goto_usercenter(){
  router.push('/user_center');
}
//注册新管理员
function goto_register(){
  router.push('/sys_register');
}
</script>

<template>
  <el-menu
      class="menu-bar"
      mode="horizontal"
      :default-active="route.path"
      :ellipsis="false"
  >
    <div class="menu-left">
      <el-menu-item>
        <router-link to="/">
          <img
              :src="require('@/assets/images/图标_店主众筹-众筹票据.png')"
              height="65px"
              alt="众筹管理系统"
          />
        </router-link>
      </el-menu-item>
      <el-menu-item
      index="/sysuser_index">
        <router-link to="/sysuser_index">
          首页
        </router-link>
      </el-menu-item>
      <el-menu-item
      index="/sysuser_add">
        <router-link to="/sysuser_add">
          添加项目类别
        </router-link>
      </el-menu-item>
      <el-menu-item
      index="/sysuser_check">
        <router-link to="/sysuser_check">
          审核项目
        </router-link>
      </el-menu-item>
    </div>

    <div class="menu-center">
      <el-input
          v-model="search_name"
          type="text"
          size="large"
          placeholder="输入项目名称"
          class="search-input"
          @keyup.enter="find_by_name"
      >
        <template #suffix>
          <el-button :icon="Search" @click="find_by_name" circle />
        </template>
      </el-input>
    </div>

    <div class="menu-right">
      <!-- 如果用户已经登录，显示以下内容 -->
      <el-sub-menu v-if="name">
        <template #title>
          <el-avatar
              v-if="sqlurl"
              :src="squareUrl"
              size="60"
              shape="circle"
              class="user-avatar"
          ></el-avatar>
          <el-avatar
              v-else
              size="60"
              class="user-avatar"
          >
            {{ getUserInitials(name) }}
          </el-avatar>
          &nbsp;&nbsp;{{name}}
        </template>
        <el-menu-item @click="goto_register">注册新管理员</el-menu-item>
        <el-menu-item @click="goto_usercenter">个人信息</el-menu-item>
        <el-menu-item @click="safe_exit">安全退出</el-menu-item>
      </el-sub-menu>
      <!-- 如果用户没有登录 -->
      <el-sub-menu v-else>
        <template #title>
          <el-avatar
              size="60"
              shape="circle"
              class="default-avatar"
              @click="go_login"
          >
            登录
          </el-avatar>
        </template>
        <el-menu-item class="no-user-content">
          <p>首次使用？<a href="/#/register" class="register-link">点我注册</a></p>
        </el-menu-item>
      </el-sub-menu>
    </div>
  </el-menu>
</template>

<style scoped>
.menu-bar {
  background-color: #f5f7fa;
  padding: 10px 20px;
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.menu-left,
.menu-center,
.menu-right {
  display: flex;
  align-items: center;
}

.menu-center {
  flex-grow: 1;
  justify-content: center;
}

.menu-item-text {
  font-size: 16px;
  color: #333;
  font-weight: bold;
  margin: 0 10px;
}

.search-input {
  width: 300px;
  margin-left: 20px;
}

.user-avatar,
.default-avatar {
  border: 2px solid #409eff;
  cursor: pointer;
  margin-left: 20px;
}

.no-user-content {
  background-color: #f0f9ff;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  font-size: 14px;
  color: #606266;
}

.no-user-content p {
  margin: 10px 0;
}

.no-user-content ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.no-user-content ul li {
  margin: 5px 0;
}

.login-button {
  margin-top: 10px;
  border-radius: 5px;
}

.register-link {
  color: #25a4bb;
  text-decoration: underline;
}
.el-menu-item.is-active {
  font-weight: bold;  /* 选中项加粗 */
}
.search-input .el-icon {
  cursor: pointer; /* 显示为可点击 */
  color: #409eff; /* 设置图标颜色 */
  transition: color 0.4s;
}

.search-input .el-icon:hover {
  color: #ff66b5; /* 鼠标悬停时颜色 */
}
</style>