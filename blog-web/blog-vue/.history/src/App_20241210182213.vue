<script setup>
import NavBar from './components/NavBar.vue'
</script>

<template>
  <NavBar />
  <router-view />
</template>

<style>
.el-message {
  background-color: rgba(222, 218, 218, 0.9) !important; /* 自定义背景颜色 */
  border-radius: 8px !important; /* 自定义圆角 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important; /* 自定义阴影 */
  color: #333 !important; /* 自定义字体颜色 */
    z-index: 9999; /* 确保弹窗在最上层 */
  position: fixed; /* 固定位置 */
  top: 20px; /* 距离顶部的距离 */
  right: 20px; /* 距离右侧的距离 */
  padding: 15px 20px; /* 内边距 */
  border-radius: 8px; /* 圆角 */
  background-color: rgba(255, 255, 255, 0.9); /* 背景颜色 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); /* 阴影效果 */
  transition: opacity 0.3s ease, transform 0.3s ease; /* 过渡效果 */
  opacity: 0.9; /* 透明度 */
}
</style>
