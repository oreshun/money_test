<script setup>
// 用于存储类别数据
import axios from "axios";
import {onMounted, ref} from "vue";
import {PictureFilled, Search, UploadFilled} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";
import Footer from "@/views/SysUser/footer/Footer_index.vue";
import Header from "@/views/SysUser/head/user_head_index.vue";
const categories = ref([]);
// API Token
const token = sessionStorage.getItem("token");
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
onMounted(()=>{
  fetchCategories();
})

//参考表单对象
const ruleFormRef = ref(null);
//注册表单数据
const ruleForm = ref({
  title:'',
  category:'',
  goal_amount:0,
  project_time:[],
  description:'',
  user_id:JSON.parse(sessionStorage.getItem("user")).id,
  project_file:'',
  image:''
})
const rules = {
  title:[
    {required:true,message:'请输入项目标题',trigger:'blur'}
  ],
  category:[
    {
      required:true,
      message:'请选择类别',
      trigger:'blur'
    }
  ],
  goal_amount:[
    {required:true,message:'请输入项目目标金额',trigger:'blur'}
  ],
  project_time:[
    {required:true,message:'选择项目起始和结束时间',trigger:'change'}
  ]
}

// 上传前校验
const beforeUpload = (file) => {
  const isLt5M = file.size / 1024 / 1024 < 10; // 限制大小为10Mb
  if (!isLt5M) {
    ElMessage.error("上传文件大小不能超过 10MB!");
    return false;
  }
  return true;
};
// 上传前校验
const beforeUpload_image = (file) => {
  //首先检查是否满足要求
  //检验文件类型
  const allowedTypes = ["image/png", "image/jpeg",'image/jpg'];
  if(!allowedTypes.includes(file.type)){
    ElMessage.error("仅支持上传 JPG, PNG, JPEG格式的图片")
    return false;
  }
  const isLt5M = file.size / 1024  < 500; // 限制大小为500kb
  if (!isLt5M) {
    ElMessage.error("上传文件大小不能超过 500kb!");
    return false;
  }
  return true;
};
//文件上传设置
const uploadResources = async (option) => {
  //从用户选择的文件中取第一个文件
  const file = option.file;
  //若未选择文件，则直接返回
  if (!file) return;
  //创建FormData传输文件
  const formData = new FormData();
  //添加键值对，将文件以键名的方式附加到表单中
  formData.append('file', file);
  formData.append('user_id', JSON.parse(sessionStorage.getItem("user")).id);
  //向后端发送请求
  try {
    const response = await axios.post('http://localhost:8000/project_operate/upload_file', formData,{
      headers: {
        "Content-Type": "multipart/form-data",
        'Authorization':token
      }
    });
    let data = response.data;
    //显示上传成功通知
    if(data.code === 200){
      ElMessage.success(data.info)
      ruleForm.value.project_file = data.file;
    }else {
      ElMessage.error(data.info)
    }
  }catch (e){
    ElMessage.error(e.message)
  }
}
//项目图片上传设置
const uploadpicture = async (option) => {
  //获取用户上传的图片
  const image = option.file
  if(!image) return;

  //创建formdata传输文件
  const formData = new FormData();
  formData.append('image', image);
  formData.append('user_id', JSON.parse(sessionStorage.getItem("user")).id);
  try{
    //向后端发送请求
    const response = await axios.post('http://localhost:8000/project_operate/upload_file', formData,{
      headers:{
        "Content-Type": "multipart/form-data",
        'Authorization':token
      }
    });
    let data = response.data;
    if (data.code === 200){
      ElMessage.success(data.info)
      ruleForm.value.image = data.file;
    }else {
      ElMessage.error(data.info)
    }
  }catch (e){
    ElMessage.error(e.message)
  }
}
//图片预览设置
const handlePreview=(file)=>{
  window.open(file.url || file.response.url);
}
//上传图片删除逻辑处理
const handleRemove = async ()=>{
  if (!ruleForm.value.image) {
    return; // 文件未上传，无需删除
  }
  try{
    //直接传入图片的路径
    const response = await axios.post('http://localhost:8000/project_operate/delete_file', {
      'file_path':ruleForm.value.image,
    },{
      headers: {
        "Content-Type": "multipart/form-data",
        "Authorization":token
      }
    });
    let data = response.data;
    if(data.code === 200){
      ElMessage.success("文件删除成功")
      //再次设置为空
      ruleForm.value.image = ''
    }else {
      ElMessage.error("文件删除失败" + data.info)
    }
  }catch (e){
    ElMessage.error("删除文件失败"+e.message)
  }
}
//上传文件的删除处理
const handleRemove_file = async ()=>{
  if (!ruleForm.value.project_file) {
    return; // 文件未上传，无需删除
  }
  try{
    //直接传入图片的路径
    const response = await axios.post('http://localhost:8000/project_operate/delete_file', {
      'file_path':ruleForm.value.project_file,
    },{
      headers: {
        "Content-Type": "multipart/form-data",
        "Authorization":token
      }
    });
    let data = response.data;
    if(data.code === 200){
      ElMessage.success("文件删除成功")
      ruleForm.value.project_file = ''
    }else {
      ElMessage.error("文件删除失败" + data.info)
    }
  }catch (e){
    ElMessage.error("删除文件失败"+e.message)
  }
}
//表单提交
const submitForm =()=>{
  //进行表单验证
  ruleFormRef.value.validate(async (valid) => {
    if (valid) {
      //如果验证成功，进行提交请求
      let response = await axios.post('http://localhost:8000/project/add_project',ruleForm.value,{
        headers:{
          'Content-Type': 'application/json', // 默认 axios 使用 JSON 格式
          'Authorization':token
        }
      });
      let data = response.data
      if(data.code === 200){
        ElMessage.success("项目发布成功,请等待审核")
        setTimeout(()=>{
          location.reload();
        },1000)
      }else {
        ElMessage.error("项目发布失败"+data.info)
      }
    }else {
      console.log('验证失败')
    }
  })
}
//重置界面
const resetForm = async () =>{
  location.reload();
}
</script>

<template>
  <!--  普通用户首页-->
  <div class="common-layout">
    <el-container>
      <el-header><Header></Header></el-header>
      <el-main>
        <el-form
            ref="ruleFormRef"
            style="max-width: 600px"
            :model="ruleForm"
            :rules="rules"
            label-width="auto"
            class="demo-ruleForm"
            status-icon
        >
          <el-form-item prop="title">
            <template #label>
              项目标题
            </template>
            <el-input
                v-model="ruleForm.title"
                type="text"
                size="large"
                placeholder="项目标题"
            ></el-input>
          </el-form-item>
          <el-form-item prop="category">
            <template #label>
              项目类别
            </template>
            <el-select
                v-model="ruleForm.category"
                placeholder="请选择类别"
                style="width: 240px"
            >
              <el-option
                  v-for="item in categories"
                  :key="item.category_id"
                  :value="item.category_name"
                  :label="item.category_name"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item prop="goal_amount">
            <template #label>
              项目目标金额
            </template>
            <el-input-number v-model="ruleForm.goal_amount" :min="0" :step="1000">
              <template #prefix>
                <span>￥</span>
              </template>
            </el-input-number>
          </el-form-item>
          <el-form-item prop="project_time">
            <template #label>
              项目持续时间
            </template>
            <el-date-picker
                v-model="ruleForm.project_time"
                type="datetimerange"
                start-placeholder="项目开始时间"
                end-placeholder="项目结束时间"
                value-format="YYYY-MM-DD HH:mm:ss"
                format="YYYY-MM-DD HH:mm:ss"
            />
          </el-form-item>
          <el-form-item prop="description">
            <template #label>
              项目详细描述
            </template>
            <el-input
                style="width: 100%"
                :autosize="{ minRows: 3, maxRows: 9 }"
                type="textarea"
                placeholder="请输入项目描述..."
                v-model="ruleForm.description"
            />
          </el-form-item>
          <el-form-item prop="project_file">
            <template #label>
              项目相关资源
            </template>
            <el-upload
                class="upload-demo"
                drag
                :http-request="uploadResources"
                :before-upload="beforeUpload"
                :on-remove="handleRemove_file"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                拖动文件到此处 或 <em>点击此处上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  文件小于10Mb,最多上传1个文件
                </div>
              </template>
            </el-upload>
          </el-form-item>
          <el-form-item prop="image">
            <template #label>
              项目图片
            </template>
            <el-upload
                class="upload-demo"
                :http-request="uploadpicture"
                :before-upload="beforeUpload_image"
                :on-preview="handlePreview"
                :on-remove="handleRemove"
                list-type="picture"
            >
              <el-button type="primary">点击上传项目图片</el-button>
              <template #tip>
                <div class="el-upload__tip">
                  jpg/png 文件小于500kb
                </div>
              </template>
            </el-upload>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">
              提交
            </el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </el-main>
      <el-footer><Footer></Footer></el-footer>
    </el-container>
  </div>
</template>

<style scoped>
</style>