<template>
  <canvas ref="canvas" class="particle-canvas"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const canvas = ref(null);
let ctx = null;
let particles = [];
let animationId = null;

// 粒子类
class Particle {
  constructor(x, y, color) {
    this.x = x;
    this.y = y;
    this.color = color;
    this.size = Math.random() * 8 + 2;
    this.speedX = Math.random() * 8 - 4;
    this.speedY = Math.random() * 8 - 4;
    this.life = 1;
    this.alpha = 1;
    this.rotation = Math.random() * Math.PI * 2;
    this.rotationSpeed = (Math.random() - 0.5) * 0.2;
    this.shape = Math.random() > 0.5 ? 'circle' : 'star';
  }

  update() {
    this.x += this.speedX;
    this.y += this.speedY;
    this.speedY += 0.1;
    this.alpha -= 0.015;
    this.life -= 0.015;
    this.rotation += this.rotationSpeed;
    this.size = Math.max(0, this.size - 0.1);
  }

  draw() {
    if (this.life <= 0) return;
    ctx.save();
    ctx.globalAlpha = this.alpha;
    ctx.fillStyle = this.color;
    ctx.strokeStyle = this.color;
    ctx.translate(this.x, this.y);
    ctx.rotate(this.rotation);

    if (this.shape === 'circle') {
      ctx.beginPath();
      ctx.arc(0, 0, this.size, 0, Math.PI * 2);
      ctx.fill();
    } else {
      this.drawStar();
    }

    ctx.restore();
  }

  drawStar() {
    const spikes = 5;
    const outerRadius = this.size;
    const innerRadius = this.size / 2;

    ctx.beginPath();
    for (let i = 0; i < spikes * 2; i++) {
      const radius = i % 2 === 0 ? outerRadius : innerRadius;
      const angle = (i * Math.PI) / spikes;
      const x = Math.cos(angle) * radius;
      const y = Math.sin(angle) * radius;
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    }
    ctx.closePath();
    ctx.fill();
  }
}

// 设置canvas尺寸
const setCanvasSize = () => {
  if (canvas.value) {
    canvas.value.width = window.innerWidth;
    canvas.value.height = window.innerHeight;
  }
};

// 创建粒子
const createParticles = (e) => {
  const colors = 
  [
    '#FF69B4',
    '#87CEEB',
    '#FFD700',
    '#98FB98',
    '#DDA0DD',
    '#F0E68C',
    '#87CEFA'
  ];
 ['#ff7979', '#7ed6df', '#f6e58d', '#badc58', '#dff9fb'];

  const mouseX = e.clientX;
  const mouseY = e.clientY;

  if (particles.length > 150) {
    particles.length = 0;
  }

  for (let i = 0; i < 20; i++) {
    const color = colors[Math.floor(Math.random() * colors.length)];
    particles.push(new Particle(mouseX, mouseY, color));
  }
};

// 动画循环
const animate = () => {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height);

  for (let i = particles.length - 1; i >= 0; i--) {
    particles[i].update();
    particles[i].draw();

    if (particles[i].life <= 0) {
      particles.splice(i, 1);
    }
  }

  animationId = requestAnimationFrame(animate);

  if (particles.length === 0) {
    cancelAnimationFrame(animationId);
    animationId = null;
  }
};

// 清理函数
const cleanup = () => {
  if (animationId) {
    cancelAnimationFrame(animationId);
    animationId = null;
  }
  particles = [];
  if (ctx) {
    ctx.clearRect(0, 0, canvas.value.width, canvas.value.height);
  }
};

// 事件处理函数
const handleClick = (e) => {
  createParticles(e);
  if (!animationId) {
    animate();
  }
};

const handleTouch = (e) => {
  e.preventDefault();
  createParticles({
    clientX: e.touches[0].clientX,
    clientY: e.touches[0].clientY
  });
  if (!animationId) {
    animate();
  }
};

const handleVisibilityChange = () => {
  if (document.hidden) {
    cleanup();
  }
};

// 生命周期钩子
onMounted(() => {
  ctx = canvas.value.getContext('2d');
  setCanvasSize();

  window.addEventListener('resize', setCanvasSize);
  window.addEventListener('click', handleClick);
  window.addEventListener('touchstart', handleTouch);
  document.addEventListener('visibilitychange', handleVisibilityChange);
});

onUnmounted(() => {
  cleanup();
  window.removeEventListener('resize', setCanvasSize);
  window.removeEventListener('click', handleClick);
  window.removeEventListener('touchstart', handleTouch);
  document.removeEventListener('visibilitychange', handleVisibilityChange);
});
</script>

<style scoped>
.particle-canvas {
  position: fixed;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 9999;
}
</style> 