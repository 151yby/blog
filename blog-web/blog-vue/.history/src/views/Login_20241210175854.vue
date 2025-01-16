<template>
  <div class="auth-container">
    <h2 v-if="isLogin">用户登录</h2>
    <h2 v-else>用户注册</h2>
    <form @submit.prevent="isLogin ? handleLogin() : handleRegister()" class="auth-form">
      <input type="text" v-model="username" placeholder="用户名" required />
      <input type="email" v-if="!isLogin" v-model="email" placeholder="电子邮件" required />
      <input type="password" v-model="password" placeholder="密码" required />
      <button type="submit">{{ isLogin ? '登录' : '注册' }}</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p v-if="successMessage" class="success">{{ successMessage }}</p>
    <p @click="toggleForm" class="toggle-form">
      {{ isLogin ? '没有账户？注册' : '已有账户？登录' }}
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const router = useRouter();
const isLogin = ref(true);
const username = ref('');
const email = ref('');
const password = ref('');
const errorMessage = ref('');
const successMessage = ref('');

const handleLogin = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/login/', {
      username: username.value,
      password: password.value,
    });
   
    // 显示登录成功的弹窗提示
    ElMessage({
      message: '登录成功！',
      type: 'success',
    });
    // 登录成功后的重定向逻辑
    router.push('/'); // 重定向到主页
  } catch (error) {
    if (error.response) {
      errorMessage.value = error.response.data.error; // 显示错误消息
    } else {
      errorMessage.value = '登录请求失败，请重试。';
    }
  }
};

const handleRegister = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/register/', {
      username: username.value,
      email: email.value,
      password: password.value,
    });
    successMessage.value = response.data.message; // 注册成功消息
    // 注册成功后，切换到登录状态
    isLogin.value = true;

    email.value = ''; // 清空电子邮件输入框
    password.value = ''; // 清空密码输入框
    errorMessage.value = ''; // 清除错误消息
    successMessage.value = ''; // 清除成功消息
  } catch (error) {
    if (error.response) {
      errorMessage.value = error.response.data.error; // 显示错误消息
    } else {
      errorMessage.value = '注册请求失败，请重试。';
    }
  }
};

const toggleForm = () => {
  isLogin.value = !isLogin.value; // 切换登录和注册状态
};
</script>

<style scoped>
.el-message {
  width: 100px;
  height: ;
  z-index: 9999; /* 确保弹窗在最上层 */
  position: fixed; /* 固定位置 */
  top: 40px; /* 距离顶部的距离 */
  right: 20px; /* 距离右侧的距离 */
  padding: 15px 20px; /* 内边距 */
  border-radius: 8px; /* 圆角 */
  background-color: rgba(115, 104, 104, 0.9); /* 背景颜色 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); /* 阴影效果 */
  transition: opacity 0.3s ease, transform 0.3s ease; /* 过渡效果 */
  opacity: 0.9; /* 透明度 */
  font-size: 100px;
}

.auth-container {
  position: relative;
  margin: auto;
  top: 100px;
  width: 400px;
  padding: 20px;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.auth-form {
  display: flex;
  flex-direction: column;
}

.auth-form input {
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.auth-form button {
  padding: 10px;
  border: none;
  border-radius: 4px;
  background-color: #4facfe;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.auth-form button:hover {
  background-color: #00f2fe; /* 悬停时按钮颜色 */
}

.error {
  color: red;
  margin-top: 10px;
}

.success {
  color: green;
  margin-top: 10px;
}

.toggle-form {
  margin-top: 15px;
  color: #007bff;
  cursor: pointer;
}
</style>