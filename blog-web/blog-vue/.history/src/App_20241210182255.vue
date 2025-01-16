<script setup>
import NavBar from './components/NavBar.vue'
</script>

<template>
  <NavBar />
  <router-view />
</template>

<style>
.el-message {
  border-radius: 8px !important; 
  color: #333 !important; 
  position: fixed; 
  top: 20px;
  right: 20px; 
  padding: 15px 20px; 
  border-radius: 8px; 
  background-color: rgba(255, 255, 255, 0.9); 
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); 
  transition: opacity 0.3s ease, transform 0.3s ease;
  opacity: 0.9; /* 透明度 */
}
</style>
