<script setup>
import Header from "@/views/SysUser/head/head_index.vue";
import Footer from "@/views/SysUser/footer/Footer_index.vue";
import {Avatar, Timer, User} from "@element-plus/icons-vue";
import user_Header from "@/views/SysUser/head/user_head_index.vue";
import {ref} from 'vue'
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

//获取当前响应的路径
import {useRoute} from "vue-router";
const route = useRoute();
import Router from "@/router";
function goto_center(){
  Router.push('/user_center');
}
function goto_history(){
  Router.push('/user_history');
}
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header class="header" v-if="current.identify==='manager'">
        <Header />
      </el-header>
      <el-header class="header" v-else>
        <user_Header></user_Header>
      </el-header>
      <el-container>
        <el-aside>
          <el-menu
              active-text-color="#ffd04b"
              background-color="#2d3a4b"
              text-color="#fff"
              class="el-menu-vertical-demo"
              :default-active="route.path"
              :ellipsis="false"
          >
            <!--            个人资料界面-->
            <el-menu-item index="/user_center" @click="goto_center">
              <el-icon><user></user></el-icon>
              个人资料
            </el-menu-item>
            <el-menu-item index="/user_history" @click="goto_history">
              <el-icon><timer></timer></el-icon>
              浏览历史
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>浏览历史详细界面</el-main>
      </el-container>
      <el-footer><Footer></Footer></el-footer>
    </el-container>
  </div>
</template>

<style scoped>

</style>