<template>
  <div class="login-container">
    <div class="system-title">
      <h2>个人博客后台管理</h2>
      <p>Blog Management System</p>
    </div>
    <div class="login-card">
      <h1>{{ isLogin ? '登录' : '注册' }}</h1>
      <form @submit.prevent="handleSubmit">
        <div class="input-group">
          <input type="text" v-model="username" placeholder="用户名" required />
        </div>
        <div class="input-group" v-if="!isLogin">
          <input type="email" v-model="email" placeholder="电子邮件" required />
        </div>
        <div class="input-group">
          <input type="password" v-model="password" placeholder="密码" required />
        </div>
        <div v-if="!isLogin" class="input-group">
          <input type="password" v-model="confirmPassword" placeholder="确认密码" required />
        </div>
        
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <button type="submit" class="login-button">{{ isLogin ? '登录' : '注册' }}</button>
      </form>
      <p class="footer-text">
        {{ isLogin ? '还没有账户？' : '已有账户？' }}
        <a href="#" @click.prevent="toggleForm">{{ isLogin ? '注册' : '登录' }}</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const isLogin = ref(true);
const username = ref('');
const password = ref('');
const confirmPassword = ref('');
const email = ref('');
const errorMessage = ref('');

const API_URL = 'http://localhost:8001/Login';

const handleSubmit = async () => {
  try {
    errorMessage.value = '';
    if (isLogin.value) {
      // 登录逻辑
      const response = await axios.post('/Login/login', {
        username: username.value,
        password: password.value,
      });

      // 保存 token
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);

      // 设置默认 Authorization header
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;

      // 登录成功后跳转
      router.push('/dashboard');
    } else {
      // 注册逻辑
      if (password.value !== confirmPassword.value) {
        errorMessage.value = '两次输入的密码不匹配！';
        return;
      }

      const response = await axios.post('/api/register', {
        username: username.value,
        email: email.value,
        password: password.value,
      });

      if (response.status === 201) {
        // 注册成功，切换到登录状态
        isLogin.value = true;
        errorMessage.value = '注册成功，请登录';
        // 清空表单
        username.value = '';
        password.value = '';
        email.value = '';
        confirmPassword.value = '';
      }
    }
  } catch (error) {
    console.error('Error:', error);
    if (error.response) {
      errorMessage.value = error.response.data.message || error.response.data.detail || '请求失败，请重试';
    } else {
      errorMessage.value = '网络错误，请检查网络连接';
    }
  }
};

const toggleForm = () => {
  isLogin.value = !isLogin.value;
  errorMessage.value = '';
  username.value = '';
  password.value = '';
  email.value = '';
  confirmPassword.value = '';
};
</script>

<style scoped>
.login-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
  overflow: hidden;
  gap: 2rem;
}

.system-title {
  text-align: center;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
  animation: fadeInDown 1s ease-out;
}

.system-title h2 {
  font-size: 2.5rem;
  margin: 0;
  font-weight: 600;
  letter-spacing: 2px;
}

.system-title p {
  font-size: 1.2rem;
  margin: 0.5rem 0 0;
  opacity: 0.9;
  letter-spacing: 3px;
  text-transform: uppercase;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-container::before {
  content: '';
  position: absolute;
  width: 150%;
  height: 150%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 10%, transparent 60%);
  animation: rotate 25s linear infinite;
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

.login-card {
  background-color: rgba(255, 255, 255, 0.95);
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow:
    0 4px 20px rgba(0, 0, 0, 0.1),
    0 8px 32px rgba(0, 0, 0, 0.12);
  width: 400px;
  text-align: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 1;
  animation: fadeIn 1s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow:
    0 8px 25px rgba(0, 0, 0, 0.15),
    0 12px 40px rgba(0, 0, 0, 0.15);
}

h1 {
  font-size: 2rem;
  margin-bottom: 1.8rem;
  color: #333;
  font-weight: 600;
  background: linear-gradient(45deg, #23a6d5, #23d5ab);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.input-group {
  margin-bottom: 1rem;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.9);
}

input:focus {
  border-color: #23a6d5;
  box-shadow: 0 0 15px rgba(35, 166, 213, 0.15);
  outline: none;
}

/* From Uiverse.io by Allyhere */
.login-button {
  --clr-font-main: hsla(0 0% 20% / 100);
  --btn-bg-1: hsla(194 100% 69% / 1);
  --btn-bg-2: hsla(217 100% 56% / 1);
  --btn-bg-color: hsla(360 100% 100% / 1);
  --radii: 0.5em;
  cursor: pointer;
  padding: 0.9em 1.4em;
  min-width: 120px;
  min-height: 44px;
  font-size: var(--size, 1rem);
  font-weight: 500;
  transition: 0.8s;
  background-size: 280% auto;
  background-image: linear-gradient(325deg,
      var(--btn-bg-2) 0%,
      var(--btn-bg-1) 55%,
      var(--btn-bg-2) 90%);
  border: none;
  border-radius: var(--radii);
  color: var(--btn-bg-color);
  box-shadow:
    0px 0px 20px rgba(71, 184, 255, 0.5),
    0px 5px 5px -1px rgba(58, 125, 233, 0.25),
    inset 4px 4px 8px rgba(175, 230, 255, 0.5),
    inset -4px -4px 8px rgba(19, 95, 216, 0.35);
}

.login-button:hover {
  background-position: right top;
}

.login-button:is(:focus, :focus-visible, :active) {
  outline: none;
  box-shadow:
    0 0 0 3px var(--btn-bg-color),
    0 0 0 6px var(--btn-bg-2);
}

@media (prefers-reduced-motion: reduce) {
  .btn-donate {
    transition: linear;
  }
}


.footer-text {
  margin-top: 1.5rem;
  font-size: 0.95rem;
  color: #666;
}

.footer-text a {
  color: #23a6d5;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.footer-text a:hover {
  color: #23d5ab;
  text-decoration: none;
}

.error-message {
  color: #ff4d4f;
  margin: 8px 0;
  font-size: 14px;
}
</style>