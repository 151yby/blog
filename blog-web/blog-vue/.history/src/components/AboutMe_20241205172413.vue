<template>
  <div class="intro">
    <div class="intro-wrap">
      <div class="intro-content">
        <h2 class="intro-title">关于我</h2>
        <p class="intro-subtitle">About Me</p>
        <div class="intro-text">
          <p>热爱生活，热爱编程</p>
          <p>喜欢动漫，游戏，旅行，记录生活的点点滴滴</p>
        </div>
        <div class="intro-skills">
          <div class="skill-item">
            <span class="skill-name">HTML5/CSS3</span>
            <div class="skill-bar">
              <div class="skill-progress" style="width: 80%"></div>
            </div>
          </div>
          <div class="skill-item">
            <span class="skill-name">JavaScript</span>
            <div class="skill-bar">
              <div class="skill-progress" style="width: 80%"></div>
            </div>
          </div>
          <div class="skill-item">
            <span class="skill-name">爬虫</span>
            <div class="skill-bar">
              <div class="skill-progress" style="width: 85%"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="intro-image">
        <img src="../assets/imgs/凯.jpg" alt="个人照片">
      </div>
    </div>
  </div>
</template>

<script setup>
import 
</script>

<style scoped>
.intro {
  width: 100%;
  min-height: 600px;
  background: linear-gradient(135deg, #f6f8fd 0%, #f1f4f9 100%);
  padding: 80px 0;
}

.intro-wrap {
  width: 80%;
  margin: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 50px;
  background: rgba(255, 255, 255, 20);
  backdrop-filter: blur(5px);
  padding: 20px 40px;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 10);
}

.intro-title {
  font-size: 36px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.intro-subtitle {
  font-size: 18px;
  color: #666;
  margin-bottom: 30px;
  font-family: 'Times New Roman', Times, serif;
  font-weight: bold;
}

.intro-text {
  margin-bottom: 40px;
}

.intro-text p {
  font-size: 16px;
  color: black;
  line-height: 1.5;
  margin-bottom: 15px;
}

.intro-skills {
  width: 100%;
}

.skill-item {
  margin-bottom: 20px;
}

.skill-name {
  display: block;
  font-size: 14px;
  color: black;
  margin-bottom: 8px;
  font-style: italic;
}

.skill-bar {
  width: 100%;
  height: 6px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.skill-progress {
  height: 100%;
  background: linear-gradient(90deg, #4a90e2, #67b8e3);
  border-radius: 3px;
  transition: width 1.5s ease;
}
</style> 