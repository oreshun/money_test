<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import Cookies from 'js-cookie';
import { encrypt, decrypt } from '@/utils/jsencrypt';
import {Lock, Message, User, View,Hide} from '@element-plus/icons-vue';
import router from '@/router'

// 表单数据
const loginData = ref({
  email: '', // 修改为 email
  password: '',
  rememberMe: false,
});

// 参考表单对象
const loginRef = ref(null);


// 设置表单规则
const loginRules = {
  email: [{required: true, trigger: 'blur', message: '请输入你的邮箱'}],
  password: [{required: true, trigger: 'blur', message: '请输入你的密码'}],
};

// 登录逻辑实现
const handlogin = () => {
  // 进行表单规则验证
  loginRef.value.validate(async (valid) => {
    if (valid) {
      // 如果验证成功，进行登录请求
      let response = await axios.post('http://localhost:8000/user/login', {
        email: loginData.value.email, // 使用 email
        password: loginData.value.password,
      });
      // 获取后端返回的 json
      let data = response.data;
      if (data.code == 200) {
        // 显示成功信息
        ElMessage.success(data.info);
        // 将 token 信息存入头文件中
        window.sessionStorage.setItem('token', data.token);
        // 将用户信息存入 session 中
        window.sessionStorage.setItem('user', JSON.stringify(data.user));
        // 如果用户勾选了记住我的选项，就在 cookie 中存入用户的邮箱和密码
        if (loginData.value.rememberMe) {
          Cookies.set('email', loginData.value.email, {expires: 7}); // 七天有效期
          Cookies.set('password', encrypt(loginData.value.password), {expires: 7}); // 存入加密后的密码
          Cookies.set('rememberMe', loginData.value.rememberMe, {expires: 7}); // 存入用户是否点击记住我的选项
        } else {
          // 如果没有选择记住我选项，则移除 Cookie 中的用户数据
          Cookies.remove('email');
          Cookies.remove('password');
          Cookies.remove('rememberMe');
        }
        // 登录成功后判断用户的权限
        // 从 session 中获取用户的权限信息
        const currentuser = data.user;
        if (currentuser.identify === 'manager') {
          ElMessage.success('欢迎您，管理员');
          //登录成功后，进入管理员主页
          await router.push('/sysuser_index')
        } else if (currentuser.identify === 'user') {
          ElMessage.success('欢迎您，普通用户');
          await router.push('/')
        } else {
          ElMessage.success(currentuser.identify);
        }
      } else {
        ElMessage.error(data.info);
      }
    } else {
      console.log('验证失败');
    }
  });
};

// 在进行页面初始化时，查看本地的 cookie 里有没有用户
function getCookie() {
  const email = Cookies.get('email'); // 使用 email
  const password = Cookies.get('password');
  const rememberMe = Cookies.get('rememberMe');

  // 给表单赋值，用三元运算符
  loginData.value = {
    email: email === undefined ? loginData.value.email : email,
    password: password === undefined ? loginData.value.password : decrypt(password),
    rememberMe: rememberMe === undefined ? false : Boolean(rememberMe),
  };
}

// 调用一下上面的函数,进行初始化
getCookie();

//添加一个变量，控制密码是否显示
const pwdshow = ref(false);

//进行
</script>

<template>
  <div class="login">
    <el-form ref="loginRef" :model="loginData" :rules="loginRules" class="login-form">
      <h3 class="title">众筹管理系统</h3>
      <!-- 邮箱输入 -->
      <el-form-item prop="email">
        <el-input
            v-model="loginData.email"
            type="text"
            size="large"
            autocomplete="off"
            placeholder="邮箱"
        >
          <template #prefix>
            <el-icon>
              <Message/>
            </el-icon>
          </template>
        </el-input>
      </el-form-item>
      <!-- 密码输入框 -->
      <el-form-item prop="password">
        <el-input
            v-model="loginData.password"
            :type="pwdshow ? 'text' : 'password'"
            size="large"
            autocomplete="off"
            placeholder="密码"
        >
          <template #prefix>
            <el-icon>
              <Lock/>
            </el-icon>
          </template>
          <template #suffix>
            <!-- 显示/隐藏密码按钮 -->
            <el-icon @click="pwdshow = !pwdshow" style="cursor: pointer;">
              <component :is="pwdshow ? View : Hide" />
            </el-icon>
          </template>
        </el-input>
      </el-form-item>
      <el-checkbox v-model="loginData.rememberMe" style="margin: 0px 0px 25px 0px">记住我</el-checkbox>
      <!-- 登录按钮 -->
      <el-form-item style="width: 100%; display: flex; justify-content: center;">
        <el-button
            size="large"
            type="primary"
            @click="handlogin"
            style="width: 100%;"
        >
          <span>登 录</span>
        </el-button>
      </el-form-item>
      <div class="register-link"><a href="/#/register" style="color: #25a4bb">没有账号？点击注册</a></div>
    </el-form>
  </div>
</template>

<style scoped>
a {
  color: white;
}

.login {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-image: url("../assets/images/img.png");
  background-size: cover;
}

.title {
  margin: 0px auto 30px auto;
  text-align: center;
  color: #707070;
}

.login-form {
  border-radius: 6px;
  background: #ffffff;
  width: 400px;
  padding: 25px 25px 5px 25px;

  .el-input {
    height: 40px;

    input {
      display: inline-block;
      height: 40px;
    }
  }

  .input-icon {
    height: 39px;
    width: 14px;
    margin-left: 0px;
  }
}

.login-tip {
  font-size: 13px;
  text-align: center;
  color: #bfbfbf;
}

.login-code {
  width: 33%;
  height: 40px;
  float: right;

  img {
    cursor: pointer;
    vertical-align: middle;
  }
}

.el-login-footer {
  height: 40px;
  line-height: 40px;
  position: fixed;
  bottom: 0;
  width: 100%;
  text-align: center;
  color: #fff;
  font-family: Arial, serif;
  font-size: 12px;
  letter-spacing: 1px;
}

.login-code-img {
  height: 40px;
  padding-left: 12px;
}
</style>
