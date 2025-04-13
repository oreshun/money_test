<script setup>

//注册表单数据
import {ref} from "vue";
import axios from "axios";
import {ElMessage} from "element-plus";
import router from "@/router";

const registerData = ref({
  useremail:'',
  username:'',
  password:'',
  re_password:'',
})

//参考表单对象
const registerRef = ref(null);

//自定义密码验证器
const validatePassword = (rule, value, callback) => {
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{7,}$/
  if (!value){
    callback(new Error('请输入密码'))
  }else if (!passwordRegex.test(value)) {
    callback(new Error('密码必须大于6个字符，且包含一个大写字母、一个小写字母和一个特殊字符'))
  } else {
    callback()
  }
}
//设置表单规则
const registerRules = {
  useremail:[
    {required:true,message:'请输入邮箱地址', trigger: 'blur'},
    {
      type:'email',
      message: '请输入有效的邮件地址',
      trigger:['blur','change'],
    }
  ],
  username:[
    {required:true,message:'请输入用户名', trigger: 'blur'},
    {min:3,max:20,message: "用户名长度在3到20个字符之间",trigger:'blur'},
  ],
  password:[
    {required:true,validator:validatePassword,trigger:'blur'},
  ],
  re_password:[
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerData.value.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ]
};

//进行注册实现
const registerBtn =()=>{
  //进行表单规则验证
  registerRef.value.validate(async (valid) => {
    if (valid) {
      //如果验证成功，进行注册请求，用post方法
      let response = await axios.post('http://localhost:8000/user/register',{
        useremail:registerData.value.useremail,
        username:registerData.value.username,
        password:registerData.value.password,
        operate:'u'
      })
      //获取后端返回的json
      let data = response.data;
      if (data.code === 200){
        //显示注册成功信息
        ElMessage.success(data.info)
        //注册成功后返回登录界面
        await router.push('/login')
      }else {
        ElMessage.error(data.info);
      }
    }else {
      console.log('表单验证失败')
    }
  })
}
</script>

<template>
  <div class="register-container">
    <div class="register">
      <el-form ref="registerRef" :model="registerData" :rules="registerRules" class="register-form">
        <h3 class="title">众筹管理系统</h3>
        <!--      邮箱输入-->
        <el-form-item prop="useremail">
          <el-input
              v-model="registerData.useremail"
              type="text"
              size="large"
              autocomplete="off"
              placeholder="邮箱"
          ></el-input>
        </el-form-item>
        <!--      账号名输入-->
        <el-form-item prop="username">
          <el-input
              v-model="registerData.username"
              type="text"
              size="large"
              autocomplete="off"
              placeholder="用户名"
          ></el-input>
        </el-form-item>
        <!--      密码输入框-->
        <el-form-item prop="password">
          <el-input
              v-model="registerData.password"
              type="password"
              size="large"
              autocomplete="off"
              placeholder="密码"
          ></el-input>
        </el-form-item>
        <el-form-item prop="re_password">
          <el-input
              v-model="registerData.re_password"
              type="password"
              size="large"
              autocomplete="off"
              placeholder="再次输入密码"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <!--      登录按钮、注册按钮实现-->
          <el-button
              size="large"
              type="primary"
              style="width: 100%;"
              class="register-button"
              @click="registerBtn"
          >
            <span>注册</span>
          </el-button>
        </el-form-item>
      </el-form>
      <div class="login-link"><a href="/#/login">已有账号？点击登录</a> </div>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-color: #f0f2f5;
  background-image: url("../assets/images/register.png");
  background-size: cover;
}

.register {
  width: 400px;
  padding: 30px;
  background-color: #ffffff;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.register-form {
  margin-bottom: 20px;
}

.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.register-button {
  width: 100%;
  background-color: #409EFF;
  border-color: #409EFF;
  border-radius: 5px;
  font-size: 16px;
}

.register-button:hover {
  background-color: #66b1ff;
  border-color: #66b1ff;
}

.login-link {
  text-align: center;
  margin-top: 15px;
}

.login-link a {
  color: #409EFF;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>