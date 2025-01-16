<template>
  <div class="settings-manager">
    <div class="settings-grid">
      <!-- 个人信息设置 -->
      <div class="settings-card">
        <h2>个人信息</h2>
        <form @submit.prevent="handleProfileSubmit" class="settings-form">
          <div class="form-group">
            <label>头像</label>
            <div class="avatar-uploader">
              <img :src="profile.avatar" alt="avatar" class="avatar-preview">
              <div class="avatar-actions">
                <button type="button" class="btn" @click="handleAvatarUpload">
                  <i class="fas fa-upload"></i> 上传新头像
                </button>
                <input
                  type="file"
                  ref="avatarInput"
                  style="display: none"
                  accept="image/*"
                  @change="onAvatarChange"
                >
              </div>
            </div>
          </div>
          <div class="form-group">
            <label>用户名</label>
            <input type="text" v-model="profile.username" required>
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input type="email" v-model="profile.email" required>
          </div>
          <div class="form-group">
            <label>个人简介</label>
            <textarea v-model="profile.bio" rows="3"></textarea>
          </div>
          <button type="submit" class="btn primary">保存个人信息</button>
        </form>
      </div>

      <!-- 安全设置 -->
      <div class="settings-card">
        <h2>安全设置</h2>
        <form @submit.prevent="handlePasswordSubmit" class="settings-form">
          <div class="form-group">
            <label>当前密码</label>
            <input type="password" v-model="security.currentPassword" required>
          </div>
          <div class="form-group">
            <label>新密码</label>
            <input type="password" v-model="security.newPassword" required>
          </div>
          <div class="form-group">
            <label>确认新密码</label>
            <input type="password" v-model="security.confirmPassword" required>
          </div>
          <button type="submit" class="btn primary">修改密码</button>
        </form>
      </div>

      <!-- 网站设置 -->
      <div class="settings-card">
        <h2>网站设置</h2>
        <form @submit.prevent="handleSiteSubmit" class="settings-form">
          <div class="form-group">
            <label>网站标题</label>
            <input type="text" v-model="site.title" required>
          </div>
          <div class="form-group">
            <label>网站描述</label>
            <textarea v-model="site.description" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>每页文章数</label>
            <input type="number" v-model="site.postsPerPage" min="1" required>
          </div>
          <div class="form-group">
            <label>评论设置</label>
            <div class="checkbox-group">
              <label class="checkbox">
                <input type="checkbox" v-model="site.enableComments">
                <span class="checkmark"></span>
                启用评论功能
              </label>
              <label class="checkbox">
                <input type="checkbox" v-model="site.moderateComments">
                <span class="checkmark"></span>
                评论需要审核
              </label>
            </div>
          </div>
          <button type="submit" class="btn primary">保存网站设置</button>
        </form>
      </div>

      <!-- 主题设置 -->
      <div class="settings-card">
        <h2>主题设置</h2>
        <form @submit.prevent="handleThemeSubmit" class="settings-form">
          <div class="form-group">
            <label>主题模式</label>
            <div class="theme-selector">
              <button
                type="button"
                class="theme-option"
                :class="{ active: theme.mode === 'light' }"
                @click="theme.mode = 'light'"
              >
                <i class="fas fa-sun"></i>
                浅色模式
              </button>
              <button
                type="button"
                class="theme-option"
                :class="{ active: theme.mode === 'dark' }"
                @click="theme.mode = 'dark'"
              >
                <i class="fas fa-moon"></i>
                深色模式
              </button>
              <button
                type="button"
                class="theme-option"
                :class="{ active: theme.mode === 'auto' }"
                @click="theme.mode = 'auto'"
              >
                <i class="fas fa-adjust"></i>
                跟随系统
              </button>
            </div>
          </div>
          <div class="form-group">
            <label>主题色</label>
            <div class="color-selector">
              <button
                v-for="color in availableColors"
                :key="color"
                type="button"
                class="color-option"
                :class="{ active: theme.primaryColor === color }"
                :style="{ backgroundColor: color }"
                @click="theme.primaryColor = color"
              ></button>
            </div>
          </div>
          <button type="submit" class="btn primary">保存主题设置</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

// 个人信息
const profile = reactive({
  avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=1',
  username: 'admin',
  email: 'admin@example.com',
  bio: '这是一个示例简介'
});

// 安全设置
const security = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
});

// 网站设置
const site = reactive({
  title: '我的博客',
  description: '这是一个基于Vue3和Django的个人博客系统',
  postsPerPage: 10,
  enableComments: true,
  moderateComments: true
});

// 主题设置
const theme = reactive({
  mode: 'light',
  primaryColor: '#1976d2'
});

// 可选主题色
const availableColors = [
  '#1976d2', // 蓝色
  '#388e3c', // 绿色
  '#e64a19', // 橙色
  '#7b1fa2', // 紫色
  '#c2185b', // 粉色
  '#00796b', // 青色
  '#f57c00', // 橙黄
  '#455a64'  // 蓝灰
];

// 头像上传相关
const avatarInput = ref(null);

const handleAvatarUpload = () => {
  avatarInput.value.click();
};

const onAvatarChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    // 实现头像上传逻辑
    console.log('Upload avatar:', file);
  }
};

// 表单提交方法
const handleProfileSubmit = () => {
  // 实现个人信息保存逻辑
  console.log('Save profile:', profile);
};

const handlePasswordSubmit = () => {
  if (security.newPassword !== security.confirmPassword) {
    alert('两次输入的密码不一致');
    return;
  }
  // 实现密码修改逻辑
  console.log('Change password:', security);
  // 清空表单
  security.currentPassword = '';
  security.newPassword = '';
  security.confirmPassword = '';
};

const handleSiteSubmit = () => {
  // 实现网站设置保存逻辑
  console.log('Save site settings:', site);
};

const handleThemeSubmit = () => {
  // 实现主题设置保存逻辑
  console.log('Save theme settings:', theme);
};
</script>

<style scoped>
.settings-manager {
  padding: 20px;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.settings-card {
  border-radius: 12px;
  padding: 24px;
}

.settings-card h2 {
  margin: 0 0 20px 0;
  color: var(--text-color);
  font-size: 1.2rem;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: var(--text-color);
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  padding: 8px 12px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  background: var(--bg-color);
  color: var(--text-color);
}

.form-group textarea {
  resize: vertical;
}

.avatar-uploader {
  display: flex;
  gap: 16px;
  align-items: center;
}

.avatar-preview {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: var(--text-color);
}

.checkbox input {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.checkbox input:checked + .checkmark {
  background: #1976d2;
  border-color: #1976d2;
}

.checkbox input:checked + .checkmark::after {
  content: '\2714';
  color: white;
  font-size: 14px;
}

.theme-selector {
  display: flex;
  gap: 12px;
}

.theme-option {
  flex: 1;
  padding: 12px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  background: var(--bg-color);
  color: var(--text-color);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.theme-option.active {
  background: #1976d2;
  color: white;
  border-color: #1976d2;
}

.color-selector {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
  gap: 8px;
}

.color-option {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.color-option.active {
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* 深色模式适配 */
:root.dark-mode {
  .form-group input,
  .form-group textarea {
    border-color: rgba(255, 255, 255, 0.1);
  }

  .theme-option {
    border-color: rgba(255, 255, 255, 0.1);
  }

  .checkmark {
    border-color: rgba(255, 255, 255, 0.2);
  }
}
</style> 