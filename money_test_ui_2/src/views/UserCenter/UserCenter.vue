<script setup>
import Header from "@/views/SysUser/head/head_index.vue";
import Footer from "@/views/SysUser/footer/Footer_index.vue";
import {Avatar, Calendar, Message, Operation, Phone, Timer, User, UserFilled} from "@element-plus/icons-vue";
import {ref} from 'vue'
import user_Header from "../SysUser/head/user_head_index.vue";
// 从头文件中获取用户信息,这只是一个副本，对其进行的修改不会映射到头文件中
const current = JSON.parse(sessionStorage.getItem("user")) || {
  username: '',
  user_email: '',
  phonenumber: '',
  user_birthday: '',
  remark: ''
};
// 临时存储编辑后的数据
const editedData = ref({ ...current });
//首先创建一个变量存储原本的邮箱
const or_email = current.user_email
//从头文件中获取token信息
const token = sessionStorage.getItem("token");
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
import {ElMessage} from "element-plus";
import axios from "axios";
function goto_center(){
  Router.push('/user_center');
}
function goto_history(){
  Router.push('/user_history');
}

//实现头像上传功能
//触发文件上传输入框
const fileInput = ref(null);//使用ref引用input的DOM元素
//通过调用alter_avatar函数，模拟点击隐藏文件选择框
const alter_avatar =()=>{
  fileInput.value.click();
};
//处理文件上传
const handleFileChange = async (event) => {
  //从用户选择的文件取第一个文件
  const file = event.target.files[0];
  //若未选择文件，则直接返回
  if (!file) return;

  //检验文件类型
  const allowedTypes = ["image/jpeg", "image/png", "image/gif"];
  if (!allowedTypes.includes(file.type)) {
    ElMessage.error("仅支持上传 JPG, PNG, GIF 格式的图片");
    return;
  }

  //创建FormData传输文件
  const formData = new FormData();
  //添加键值对，将文件以键名avatar附加到表单中
  formData.append("avatar", file);
  formData.append("useremail",current.user_email);
  try {
    //向后端发送请求
    const response = await axios.post("http://localhost:8000/user/uploadavatar", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        'Authorization':token
      },
    });
    let data = response.data;
    //更新头像路径
    if (data.code===200) {
      //更新用户信息
      current.avatar = response.data.new_avatar_url;
      sessionStorage.setItem("user", JSON.stringify(current));//更新缓存
      ElMessage.success("头像更新成功");
      location.reload();//重新加载界面
    }else {
      ElMessage.error(data.info);
    }
  }catch (error){
    ElMessage.error("上传失败，请检查网络连接");
  }
};

//处理编辑内容
//默认是不可编辑的
const isEditing = ref(false);

//点击编辑按钮后，内容可以编辑
const alter_jiemian = ()=>{
  isEditing.value = !isEditing.value;
}

// 返回按钮：还原数据并退出编辑模式
const back_t = () => {
  // 恢复 `editedData` 为 `current` 的数据
  editedData.value = { ...current };
  isEditing.value = false;
};

//出生日期选择器的绑定数据
const brith = ref("")
//进行数据修改后的提交
const submit_infomation=async () => {
    // 确保 brith 是一个日期字符串，如果是 Date 对象，转换为 'YYYY-MM-DD' 格式
  // const userBirthday = brith.value instanceof Date
  //   ? brith.value.toISOString().split('T')[0]  // 提取 'YYYY-MM-DD'
  //   : brith.value; // 如果 brith 已经是一个正确的字符串格式，不进行转换
  const userBirthday = brith.value ? new Date(brith.value).toISOString().split('T')[0] : "";
  //创建表单项以传输信息
  const formData = new FormData();
  if (editedData.value.username) formData.append('username', editedData.value.username);
  if (editedData.value.user_email) formData.append('user_email', editedData.value.user_email);
  if (editedData.value.phonenumber) formData.append('phonenumber', editedData.value.phonenumber);
  if (brith) formData.append('user_birthday', userBirthday);
  if (editedData.value.remark) formData.append('remark', editedData.value.remark);
  formData.append('or_email', or_email);
  //添加原本的邮箱
  try {
    //提交数据
    let response = await axios.post("http://localhost:8000/user/uploadinfomation",formData,{
      headers: {
        'Authorization':token
      },
    });
    let data = response.data;
    if (data.code == 200){
      ElMessage.success("信息更新成功！！")
      //更新缓存
      sessionStorage.setItem("user", JSON.stringify(data.user));
      // 延迟重新加载页面，以确保弹窗显示
      setTimeout(() => {
        location.reload(); // 重新加载界面
      }, 1000);
    }else {
      ElMessage.error(data.info);
      // 延迟重新加载页面，以确保弹窗显示
      setTimeout(() => {
        location.reload(); // 重新加载界面
      }, 1000);
    }
  }catch (error){
      console.log(error)
      ElMessage.error("更新失败，请检查网络设置")
  }
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
        <el-aside class="aside">
          <el-menu
              active-text-color="#ffd04b"
              background-color="#2d3a4b"
              text-color="#fff"
              class="el-menu-vertical-demo"
              :default-active="route.path"
              :ellipsis="false"
          >
            <el-menu-item index="/user_center" @click="goto_center">
              <el-icon><user /></el-icon>
              个人资料
            </el-menu-item>
            <el-menu-item index="/user_history" @click="goto_history">
              <el-icon><timer /></el-icon>
              浏览历史
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="main">
          <div class="avatar-section">
            <el-avatar
                v-if="sqlurl"
                :src="squareUrl"
                size="80"
                shape="circle"
                class="user-avatar"
                @click="alter_avatar"
                title="点击更换头像"
            >
            </el-avatar>
            <el-avatar v-else size="80" class="user-avatar" @click="alter_avatar" title="点击更换头像">
              {{ getUserInitials(name) }}
            </el-avatar>
            <!--            隐藏的文件输入框-->
            <input type="file" ref="fileInput" accept="image/*" @change="handleFileChange" style="display: none" />
            <div class="user-info">
              <h2 class="user-name">{{ name }}</h2>
            </div>
          </div>
          <div class="data-section">
            <el-card shadow="hover" class="info-card">
              <h2>基本信息</h2>
              <el-divider />
              <ul class="info-list">
                <li class="li-hover">
                  <el-icon class="info-icon"><user /></el-icon> 用户名称
                  <span v-if="!isEditing" class="info-value">{{ current.username }}</span>
<!--                  编辑模式，输入框-->
                  <input v-if="isEditing" v-model="editedData.username" class="info-value-input" />
                </li>
                <li class="li-hover">
                  <el-icon class="info-icon"><phone /></el-icon> 手机号码
                  <span v-if="!isEditing" class="info-value">{{ current.phonenumber }}</span>
                  <input v-if="isEditing" v-model="editedData.phonenumber" class="info-value-input" />
                </li>
                <li class="li-hover">
                  <el-icon class="info-icon"><message /></el-icon> 用户邮箱
                  <span v-if="!isEditing" class="info-value">{{ current.user_email }}</span>
                  <input v-if="isEditing" v-model="editedData.user_email" class="info-value-input" />
                </li>
                <li class="li-hover">
                  <el-icon class="info-icon"><calendar /></el-icon> 注册日期
                  <span class="info-value">{{ current.register_time }}</span>
                </li>
                <li class="li-hover">
                  <el-icon class="info-icon"><calendar /></el-icon> 出生日期
                  <span v-if="!isEditing" class="info-value">{{ current.user_birthday }}</span>
                  <el-date-picker
                      v-if="isEditing"
                      v-model="brith"
                      type="date"
                      placeholder="请选择一个日期"
                      style="padding-left: 10px"
                  />
                </li>
                <li class="li-hover">
                  <el-icon class="info-icon"><message /></el-icon> 备注
                  <span v-if="!isEditing" class="info-value">{{ current.remark }}</span>
                  <el-input
                      v-if="isEditing"
                      v-model="editedData.remark"
                      style="width: 240px"
                      type="textarea"
                      placeholder="这个用户很懒，什么都没写"
                      input-style="margin-left: 10px"
                  />
                </li>
              </ul>
              <div class="btn">
<!--                这个编辑按钮默认显现，点击后消失-->
                <el-button v-if="!isEditing" type="primary" plain @click="alter_jiemian">编辑</el-button>
<!--                这两个按钮只有在点击编辑按钮后才会显现-->
                <el-button v-if="isEditing" type="primary" plain @click="submit_infomation">提交</el-button>
                <el-button v-if="isEditing" plain @click="back_t">返回</el-button>
              </div>
            </el-card>
          </div>
        </el-main>
      </el-container>
      <el-footer class="footer">
        <Footer />
      </el-footer>
    </el-container>
  </div>
</template>

<style scoped>
.common-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.header {
  background-color: #35495e;
  color: white;
  text-align: center;
  padding: 10px;
  font-size: 18px;
}

.aside {
  background-color: #2d3a4b;
  padding: 20px;
}

.el-menu-vertical-demo {
  border-right: none;
}

.main {
  padding: 20px;
  background-color: white;
}

.avatar-section {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.user-avatar {
  cursor: pointer;/*将头像设置为可点击的*/
  border: 2px solid #ffd04b;
  margin-right: 15px;
  position: relative;
}

.user-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.user-name {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.data-section {
  margin-top: 20px;
}

.info-card {
  padding: 20px;
  border-radius: 8px;
}

.info-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.info-list li {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  text-align: left;
}

.info-list li:last-child {
  border-bottom: none;
}
.info-icon {
  margin-right: 10px; /* 图标与文字间隔 */
}
.info-value {
  padding: 15px;
  font-weight: bold;
  color: #333;
}

.footer {
  background-color: #35495e;
  color: white;
  text-align: center;
  padding: 10px;
}
.alter_btn{
  cursor: pointer;/*将图标设置为可点击的*/
  color: #598df3;
  display: none;  /* 初始状态为隐藏 */
  opacity: 0;     /* 初始透明度为0 */
}
.li-hover:hover .alter_btn{
  font-size: 20px;
  display: block;  /* 初始状态为显示 */
  opacity: 1;     /* 初始透明度为1 */
  transition: opacity 0.3s ease; /* 透明度变化动画 */
}
.info-value-input{
  border: #cacaca solid 1px;
  border-radius: 4px;
  padding: 5px 15px;
  margin-left: 10px;
}
</style>