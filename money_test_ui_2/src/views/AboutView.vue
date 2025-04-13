<template>
  <div class="mb-4">
    <el-button @click="handleLogin">测试登录</el-button>
<!--    <el-button type="primary" @click="handleUserList">测试获取用户信息列表</el-button>-->

  </div>
</template>

<script setup>

import axios from "axios";

const handleLogin = async () => {
  let result = await axios.get('http://localhost:8000/user/test')
  let data = result.data;
  if (data.code == 200){
    console.log("登录成功，token=")
  }else {
    console.log("登录出错")
  }

}
</script>
