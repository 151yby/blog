<template>
  <div class="dashboard-container">
    <!-- 左侧边栏 -->
    <div class="sidebar">
      <div class="logo">
        <img v-if="!isDarkMode" src="../assets/logo.gif" alt="Logo">
        <img v-else src="../assets/logo-dark.gif" alt="Logo Dark">
        <span>博客管理系统</span>
      </div>
      <nav class="nav-menu">
        <div class="nav-item" :class="{ active: currentMenu === 'dashboard' }" @click="switchMenu('dashboard')">
          <i class="fas fa-home"></i>
          <span>Dashboard</span>
        </div>
        <div class="nav-item" :class="{ active: currentMenu === 'posts' }" @click="switchMenu('posts')">
          <i class="fas fa-file-alt"></i>
          <span>文章管理</span>
        </div>
        <div class="nav-item" :class="{ active: currentMenu === 'categories' }" @click="switchMenu('categories')">
          <i class="fas fa-folder"></i>
          <span>分类管理</span>
        </div>
        <div class="nav-item" :class="{ active: currentMenu === 'tags' }" @click="switchMenu('tags')">
          <i class="fas fa-tags"></i>
          <span>标签管理</span>
        </div>
        <div class="nav-item" :class="{ active: currentMenu === 'comments' }" @click="switchMenu('comments')">
          <i class="fas fa-comments"></i>
          <span>评论管理</span>
        </div>
        <div class="nav-item" :class="{ active: currentMenu === 'settings' }" @click="switchMenu('settings')">
          <i class="fas fa-cog"></i>
          <span>系统设置</span>
        </div>
      </nav>
    </div>

    <!-- 右侧主内容区 -->
    <div class="main-content">
      <!-- 顶部导航栏 -->
      <header class="top-bar">
        <div class="breadcrumb">
          <span>{{ menuTitles[currentMenu] }}</span>
        </div>
        <div class="header-right">
          <div class="notification">
            <i class="fas fa-bell"></i>
            <span class="badge">3</span>
          </div>
          <div class="theme-switch" @click="toggleTheme">
            <i :class="isDarkMode ? 'fas fa-sun' : 'fas fa-moon'"></i>
          </div>
          <div class="avatar">
            <img v-if = !isDarkMode src="../assets//avatar.gif" alt="用户头像">
            <img v-else src="../assets/avatar-dark.gif" alt="">
            <span class="user-name">{{ username }}</span>
          </div>
           
          <button class="logout-btn" @click="handleLogout">退出登录</button>
        </div>
      </header>

      <!-- 内容区域 -->
      <div class="content">
        <Suspense>
          <component :is="currentComponent" />
        </Suspense>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, defineAsyncComponent } from 'vue';
import { useRouter } from 'vue-router';


// 菜单状态
const currentMenu = ref('dashboard');
const menuTitles = {
  dashboard: '仪表盘',
  posts: '文章管理',
  categories: '分类管理',
  tags: '标签管理',
  comments: '评论管理',
  settings: '系统设置'
};

// 主题切换
const isDarkMode = ref(false);

// 初始化主题
onMounted(() => {
  // 检查本地存储中的主题设置
  const currentTheme = localStorage.getItem('theme');
  if (currentTheme === 'dark-mode') {
    isDarkMode.value = true;
    document.body.classList.add('dark-mode');
  }
});

// 切换主题的函数
const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
  if (isDarkMode.value) {
    document.body.classList.add('dark-mode');
    localStorage.setItem('theme', 'dark-mode');
  } else {
    document.body.classList.remove('dark-mode');
    localStorage.setItem('theme', 'light-mode');
  }
  // 重新初始化图表以更新颜色
  nextTick(() => {
    if (currentComponent.value && currentComponent.value.initCharts) {
      currentComponent.value.initCharts();
    }
  });
};

// 用户信息
const username = ref(localStorage.getItem('username') || '管理员');
const router = useRouter();

// 切换菜单
const switchMenu = (menu) => {
  currentMenu.value = menu;
};

// 退出登录
const handleLogout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  router.push('/login');
};


//动态组件加载
const currentComponent = computed(() => {
  const componentMap = {
    dashboard: defineAsyncComponent(() => import('../components/dashboard/Overview.vue')),
    posts: defineAsyncComponent(() => import('../components/dashboard/Posts.vue')),
    categories: defineAsyncComponent(() => import('../components/dashboard/Categories.vue')),
    tags: defineAsyncComponent(() => import('../components/dashboard/tags.vue')),
    comments: defineAsyncComponent(() => import('../components/dashboard/Comments.vue')),
    settings: defineAsyncComponent(() => import('../components/dashboard/settings.vue'))
  };
  return componentMap[currentMenu.value];
});

</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
  background-color: var(--bg-color);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

/* 侧边栏样式 */
.sidebar {
  width: 220px;
  background-color: var(--primary-color);
  color: #fff;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 10;
}

.logo {
  height: 50px;
  padding: 0px;
  text-align: center;
}

.logo img {
  position: relative;
  left: -25px;
  top: 10px;
  width: 40px;
  height: 40px;
}

.logo span {
  position: relative;
  top: -5px;
  left: -20px;
  font-size: 1rem;
  font-weight: 600;
}

.nav-menu {
  flex: 1;
  padding: 20px 0;
}

.nav-item {
  padding: 12px 24px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-item::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 2px;
  background-color: white;
  visibility: hidden;
  transform: scaleX(0);
  transition: all 0.2s ease-in-out;
}

.nav-item:hover::after {
  visibility: visible;
  transform: scaleX(1);
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.nav-item.active {
  background-color: #1890ff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.nav-item i {
  margin-right: 12px;
  width: 20px;
  text-align: center;
}

/* 主内容区域样式 */
.main-content {
  flex: 1;
  margin-left: 220px;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  background-color: var(--bg-color);
}

/* 顶部导航栏 */
.top-bar {
  position: sticky;
  top: 0;
  z-index: 5;
  height: 50px;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.breadcrumb {
  font-size: 1.1rem;
  color: var(--text-color);
}

/* 导航栏右侧 */
.header-right {
  display: flex;
  align-items: center;
  /* gap: 10px; */
}

.notification {
  position: relative;
  height: 50px;
  padding: 0 15px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.1s ease;
}

.notification:hover {
  background-color: rgba(128, 124, 124, 0.1);
}

.notification i {
  font-size: 1.2rem;
}

.badge {
  position: absolute;
  top: 5px;
  right: 0px;
  background-color: #ff4d4f;
  color: white;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
}

/* 主题切换按钮样式 */
.theme-switch {
  height: 50px;
  padding: 0 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-color);
}

.theme-switch:hover {
  background-color: rgba(128, 124, 124, 0.1);
}

.theme-switch i {
  font-size: 1.2rem;
}

/* 用户信息区域 */
.avatar {
  width: 100px;
  height: 50px;
  padding: 0 15px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.avatar:hover {
  background-color: rgba(128, 124, 124, 0.1);
}

.avatar img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  margin-right: 10px;
}

.user-name {
  color: var(--text-color);
  font-size: 0.9rem;
}

.logout-btn {
  width: 30%;
  padding: 8px;
  border: 1px solid #ff4d4f;
  border-radius: 4px;
  background: transparent;
  color: #ff4d4f;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: #ff4d4f;
  color: white;
}

/* 内容区域 */
.content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background-color: var(--bg-color);
}
</style> 