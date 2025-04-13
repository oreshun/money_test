<script setup>
import {useRoute, useRouter} from 'vue-router';
import axios from '@/utils/axios'
import {ElMessage} from "element-plus";
import {onMounted, ref} from "vue";
// 从头文件中获取用户信息
const current = JSON.parse(sessionStorage.getItem("user")) || {};
const route = useRoute();
const router = useRouter();
const userId = route.params.id;  // 获取路径中的 id 参数
// 项目信息存储
const product = ref(null); // 初始化为 null，待数据加载后赋值
// 设置图片基础路径
const base_squareUrl = "http://localhost:8000/media/project_images/";
const base_avatar = "http://localhost:8000/media/userAvatar/";
//存储数字
const num = ref(0)
// 获取项目信息
const fetch_project = async () => {
  try {
    const response = await axios.post(
        "/project/getproject-pass",
        {
          project_id: Number(userId),
        },
        {
          headers: {
            Authorization: token,
          }
        }
    );
    const data = response.data;
    if (data.code === 200) {
      product.value = data.data.project; // 将后端返回的项目数据赋值给 `project`
      console.log(product.value)
    } else {
      ElMessage.error(data.info);
    }
  } catch (error) {
    console.error(error);
    ElMessage.error("获取项目信息失败：" + error.message);
  }
};

// 页面加载时获取数据
onMounted(async () => {
  await fetch_project(); // 获取项目信息
});

//从头文件中获取token信息
const token = sessionStorage.getItem("token");
const go_invesment = async () => {
  try {
    let response = await axios.post('/project_operate/investment',{
      'project_id':Number(userId),
      'user_id':current.id,
      'amount':num.value,
    },{
      headers: {
        Authorization: token,
      }
    })

    let data = response.data;
    if(data.code===200){
      ElMessage.success(data.info)
      window.history.back(); // 浏览器返回上一页
    }else if (data.code===201){
      ElMessage.success(data.info)
      window.history.back(); // 浏览器返回上一页
    }
    else {
      ElMessage.error(data.info)
    }
  }catch (e)
  {
    console.log(e)
  }
}
</script>

<template>
  <div v-if="product">
    <el-container class="container">
      <!-- 页面头部 -->
      <el-header class="header">
        <h1>确认订单</h1>
      </el-header>

      <!-- 警告信息 -->
      <el-main>
        <el-alert
            type="warning"
            title="该商品为虚拟产品，仅支持在线支付且无需物流地址及运费计算。"
            description="若商品是充值类产品，请将您的手机号或卡号填写准确。"
            show-icon
            class="alert-box"
        ></el-alert>

        <!-- 商品信息 -->
        <el-card class="product-card">
          <div class="product">
              <img :src="base_squareUrl+product.image" alt="商品图片" class="product-image" />
              <h2>{{ product.title }}</h2>
              <p class="product-price">
                {{ product.goal_amount }} 元 × 1
              </p>
          </div>
        </el-card>

        <!-- 订单汇总 -->
        <el-card class="summary-card">
          <div class="summary">
            <p>商品件数：1 件</p>
            <p>商品总价：{{ product.goal_amount }} 元</p>
            <p>运费：0 元</p>
          </div>
        </el-card>
        支付金额：<el-input-number v-model="num" :min="1" step="1000">
          <template #prefix>
            <span>￥</span>
          </template>
        </el-input-number>
        <!-- 提交按钮 -->
        <div class="checkout-btn">
          <el-button type="primary" size="large" round @click="go_invesment">
            去结算
          </el-button>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>
.container {
  width: 80%;
  margin: 20px auto;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.header h1 {
  margin: 0;
  padding: 20px 0;
  font-size: 1rem;
  text-align: center;
}

.alert-box {
  margin-bottom: 20px;
}

.product-card,
.payment-card,
.summary-card {
  margin-bottom: 20px;
  border: 1px solid #f0f0f0;
  padding: 10px;
  border-radius: 5px;
}

.product {
  display: flex;
  align-items: center;
}

.product-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 5px;
  margin-right: 20px;
}

.product-info h2 {
  margin: 0;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.product-price {
  color: #f56c6c;
  font-size: 1rem;
  margin-top: 10px;
}

.payment-card h3 {
  margin: 0 0 10px;
}

.summary {
  font-size: 1rem;
}

.summary .total {
  font-size: 1.2rem;
  font-weight: bold;
  color: #f56c6c;
}

.checkout-btn {
  text-align: center;
  margin-top: 20px;
}
</style>