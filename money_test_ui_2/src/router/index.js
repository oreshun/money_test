import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import {ElMessageBox} from "element-plus";

const routes = [
  {
    path: '/',
    name: 'index',
    component: () => import( '@/views/index.vue')
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import( '../views/UserLogin.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import( '../views/UserRegister.vue')
  },
  {
    path: '/sysuser_index',
    name: 'sysuser_index',
    component: () => import( '../views/SysUser/SysUser_index.vue'),
    meta:{
      requiresAuth: true, // 需要登录才能访问
    }
  },
  {
    path: '/sysuser_add',
    name: 'sysuser_add',
    component: () => import( '../views/SysUser/SysUser_add.vue'),
    meta:{
      requiresAuth: true, // 需要登录才能访问
    }
  },
  {
    path: '/sysuser_check',
    name: 'sysuser_check',
    component: () => import( '../views/SysUser/SysUser_check.vue'),
    meta:{
      requiresAuth: true, // 需要登录才能访问
    }
  },
  {
    path:'/user_center',
    name: 'user_center',
    component: () => import( '@/views/UserCenter/UserCenter.vue'),
    meta:{
      requiresAuth: true, // 需要登录才能访问
    }
  },
  {
    path: '/user_history',
    name: 'user_history',
    component: () => import( '@/views/UserCenter/UserComponent/user_histroy.vue')
  },
  {
    path: '/test/1',
    name: 'test',
    component: () => import( '@/views/UserCenter/test.vue')
  },
  {
    path:'/project/:id',//动态路由，‘：id’代表项目的唯一标识
    name: 'project',
    component:()=>import('@/views/project/Project_Detail.vue'),
    props:true,//允许路由参数作为props传入组件
  },
  {
    path:'/project/investment/:id',
    name: 'project_investment',
    props:true,
    component:()=>import('@/views/project/Project_Investment.vue')
  },
  {
    path: '/search',
    name: 'search_project',
    component:()=>import('@/views/project/Project_search.vue')
  },
  {
    path: '/project-category/:id',
    name: 'project-category',
    props:true,
    component:()=>import('@/views/project/Project_search_by_category.vue')
  },
  {
    path: '/user_add_project',
    name: 'user_add_project',
    component:()=>import('@/views/project/Project_Pub.vue'),
    meta:{
      requiresAuth: true, // 需要登录才能访问
    }
  },
  {
    path: '/sys_register',
    name: 'sys_register',
    component:()=>import('@/views/SysUser/SysUser_register.vue'),
    meta:{
      requiresAuth: true, // 需要登录才能访问
    }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router

router.beforeEach((to, from, next) => {
  // 从头文件中获取用户信息
  const user = JSON.parse(sessionStorage.getItem("user"));
  //如果目标路由需要登录，并且用户没登陆
  if(to.meta.requiresAuth && !user){
    ElMessageBox.confirm(
        "您尚未登录，是否跳转到登录页面？",
        "未登录",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }
    )
        .then(() => {
          // 确认跳转到登录页面
          next({ path: "/login", query: { next: to.fullPath } });
        })
        .catch(() => {
          // 用户取消，不跳转
          next(false);
        });
  }else {
    next();
  }
})