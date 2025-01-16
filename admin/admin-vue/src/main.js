import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import '@fortawesome/fontawesome-free/css/all.min.css'
import './style.css'
import 'element-plus/dist/index.css'

// 配置 axios 默认值
axios.defaults.baseURL = 'http://localhost:8001'

// 添加请求拦截器
axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

const app = createApp(App)
app.use(router)
app.mount('#app')
