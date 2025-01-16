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
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
  color: #333 !important; 
  position: fixed; 
  top: 20px;
  right: 20px; 
  padding: 15px 20px; 
  border-radius: 8px; 
  transition: opacity 0.3s ease, transform 0.3s ease;
}
</style>
