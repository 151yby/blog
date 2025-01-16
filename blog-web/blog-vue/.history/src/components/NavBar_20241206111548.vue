<template>
  <div class='nav' ref="nav">
    <div class="nav-wrap">
      <ul class="nav-list">
        <li><router-link to="/">首页</router-link></li>
        <li><router-link to="/about">简介</router-link></li>
        <li><router-link to="/travel">旅行</router-link></li>
        <li><router-link to="/blog">日志</router-link></li>
        <li><router-link to="/message">留言板</router-link></li>
        <li class="theme-switch">
          <div class="theme-switch-wrapper">
            <div class="theme-switch-button" @click="toggleTheme">
              <i class="moon">🌙</i>
              <i class="sun">☀️</i>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const nav = ref(null); // 使用 ref 获取导航栏元素

// 导航栏透明度控制
onMounted(() => {
  nav.value.onmouseover = function () {
    nav.value.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
  };
  nav.value.onmouseout = function () {
    nav.value.style.backgroundColor = 'rgba(0, 0, 0, 0)';
  };

  // 导航栏滚动时的显示/隐藏效果
  let lastScrollTop = 0;
  window.addEventListener('scroll', () => {
    let currentScroll = window.pageYOffset || document.documentElement.scrollTop;
    if (currentScroll > lastScrollTop) {
      // 向下滚动时隐藏导航栏
      nav.value.classList.add('hidden');
    } else {
      // 向上滚动时显示导航栏
      nav.value.classList.remove('hidden');
    }
    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
  });
});

const isDarkMode = ref(false);
// 切换主题的函数
const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
  document.body.classList.toggle('dark-mode', isDarkMode.value);
};

// 检查本地存储中的主题设置
onMounted(() => {
  const currentTheme = localStorage.getItem('theme');
  if (currentTheme) {
    isDarkMode.value = currentTheme === 'dark-mode';
    document.body.classList.add(currentTheme);
  }
});

// 根据系统主题自动设置
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
  document.body.classList.add('dark-mode');
}

// 监听系统主题变化
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
  if (e.matches) {
    document.body.classList.add('dark-mode');
  } else {
    document.body.classList.remove('dark-mode');
  }
});
</script>

<style scoped>
/* =============== 导航栏样式 =============== */
.nav {
    width: 100%;
    height: 60px;
    background-color: rgba(0,0,0,0.7);
    position: fixed;
    z-index: 999;
    backdrop-filter: blur(5px);
    transform: translateY(0);
    transition: transform 0.4s ease, background-color 0.4s ease,opacity 0.4s ease;;
    opacity: 1;
}

/* 导航栏滚动隐藏效果 */
.nav.hidden {
    transform: translateY(-100%);
    opacity: 0;
}

/* 导航栏内容包装器 */
.nav-wrap {
    width: 80%;
    height: 60px;
    margin: auto;
}

/* Logo样式 */
.logo {
    width: 80px;
    height: 60px;
    float: left;
    text-align: center;
    line-height: 60px;
    font-size: 15px;
}

/* 导航列表样式 */
.nav-list {
    position: relative;
    width: 600px;
    height: 60px;
    float: right;
}

/* 导航列表项样式 */
.nav-list > li {
    position: relative;
    float: left;
    width: 70px;
    height: 60px;
    text-align: center;
    line-height: 60px;
    font-size: 15px;
    margin-right: 5px;
}

/* 导航链接样式 */
.nav-list > li > a {
    display: block;
    width: 100%;
    height: 100%;
    color: #fff;
}

/* 导航项下划线动画效果 */
.nav-list > li::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 2px;
    background-color: white;
    visibility: hidden;
    transform: scaleX(0);
    transition: all 0.2s ease-in-out 0s;
}

/* 下划线悬停动画 */
.nav-list > li:hover::after {
    visibility: visible;
    transform: scaleX(1);
    left: 0;
    transition: all 0.2s ease-in-out 0.2s;
}

/* 导航链接悬停效果 */
.nav-list > li > a:hover {
    cursor: pointer;
    color: gray;
}
</style> 