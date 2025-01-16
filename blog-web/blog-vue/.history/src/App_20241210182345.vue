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
  position: fixed; /* 固定位置 */
  top: 20px; /* 距离顶部的距离 */
  right: 20px; 
  padding: 15px 20px; 
  border-radius: 8px; 
  transition: opacity 0.3s ease, transform 0.3s ease;
}
</style>
