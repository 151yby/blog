<script setup>
import NavBar from './components/NavBar.vue'
</script>

<template>
  <NavBar />
  <router-view />
</template>

<style>
.el-message {
  background-color: rgba(222, 218, 218, 0.4) !important; 
  border-radius: 8px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
  color: #333 !important; 
  position: fixed !important; 
  top: 20px !important;
  right: 20px !important; 
  padding: 15px 20px !important; 
  border-radius: 8px !important; 
  transition: transform 0.3s ease !important;
}
</style>
