import axios from 'axios'//引入axios

// 创建axios实例

const instance = axios.create({

  baseURL: '/api',//配置公共url，在所有实际的请求url前添加'/api'

  timeout: 60000

})

export default instance;