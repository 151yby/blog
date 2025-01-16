<script setup>
import NavBar from './components/NavBar.vue'
</script>

<template>
  <NavBar />
  <router-view />
</template>

<style>
.el-message {
  background-color: rgba(222, 218, 218, 0.9) !important; 
  border-radius: 8px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
  color: #333 !important; 
  position: fixed; 
  top: 30px;
  right: 20px; 
  padding: 15px 20px; 
  border-radius: 8px; 
  transition: opacity 0.3s ease, transform 0.3s ease;
}
</style>
