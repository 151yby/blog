// blog-vue/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import About from '../views/About.vue';
import Travel from '../views/Travel.vue';
import Blog from '../views/Blog.vue';
import Message from '../views/Message.vue';
import Login from '../views/Login.vue'; 
import { useMusicStore } from '../store/music';


const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/about', name: 'About', component: About },
  { path: '/travel', name: 'Travel', component: Travel },
  { path: '/blog', name: 'Blog', component: Blog },
  { path: '/message', name: 'Message', component: Message },
  // { path: '/login', name: 'Login', component: Login }, // 登录页面路由
  // { path: '/login', name: 'Register', component: Login },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 全局导航守卫
router.beforeEach((to, from, next) => {
  const musicStore = useMusicStore();
  musicStore.initAudioPlayer(); // 确保音频播放器在路由切换时保持初始化
  next(); // 继续导航
})
export default router;