<template>
  <div class="b-video">
    <video src="../assets/imgs/Ocean - 19609.mp4" autoplay loop muted></video>
    <div class="subject-content">
      <h2>Welcome To My Blog</h2>
      <h1>Face life with a resilient will</h1>
      <div class="roll-box">
        <span></span>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.b-video {
  width: 100%;
  height: 100%;
  position: relative;
}

.b-video > video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.subject-content {
  position: absolute;
  width: 700px;
  height: 450px;
  left: 0;
  right: 0;
  bottom: 20%;
  top: 0;
  margin: auto;
  text-align: center;
  color: white;
}

.subject-content > h1 {
  font-size: 30px;
  letter-spacing: 5px;
  margin-top: 100px;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 1s ease forwards, colorChange 3s infinite ease-in-out;
  /* 添加渐变背景 */
  background: linear-gradient(90deg,#0a2a88,#ffffff,#0a2a88);
  background-size: 200%; /* 使渐变的宽度是文本的两倍 */
  background-clip: text; /*剪切背景 */
  -webkit-background-clip: text; /* 兼容Safari */
  color: transparent; /* 文本颜色透明 */
  animation-delay: 0.8s; /* 延迟 */
}

.subject-content > h2 {
  font-size: 35px;
  letter-spacing: 7px;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 1s ease forwards, colorChange 4s infinite ease-in-out;
  background: linear-gradient(90deg,#0a2a88,#ffffff,#0a2a88);
  background-size: 200%; 
  background-clip: text; 
  -webkit-background-clip: text;
  color: transparent; 
}

@keyframes colorChange {
  0% {
    background-position: 200%; /* 初始位置 */
  }
  100% {
    background-position: 0%; /* 结束位置 */
  }
  
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 