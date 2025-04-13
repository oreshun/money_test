import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue' // 引入所有图标，并命名为 Icons
//引入样式
import '@/assets/styles/reset.css'
import '@/assets/styles/border.css'
import locale from 'element-plus/es/locale/lang/zh-cn';



const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(ElementPlus, { locale });
app.use(ElementPlus)
app.use(store)
app.use(router)
app.mount('#app')
