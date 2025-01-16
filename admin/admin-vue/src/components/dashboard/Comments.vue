<template>
  <div class="comments-manager">
    <!-- 顶部操作栏 -->
    <div class="action-bar">
      <div class="left">
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input type="text" v-model="searchQuery" placeholder="搜索评论...">
        </div>
        <div class="filter-box">
          <select v-model="statusFilter">
            <option value="all">全部状态</option>
            <option value="pending">待审核</option>
            <option value="approved">已通过</option>
            <option value="rejected">已拒绝</option>
          </select>
        </div>
      </div>
      <div class="right">
        <button class="btn" @click="handleBatchDelete" :disabled="!selectedComments.length">
          <i class="fas fa-trash"></i> 批量删除
        </button>
      </div>
    </div>

    <!-- 评论列表 -->
    <div class="comments-list">
      <div v-for="comment in filteredComments" :key="comment.id" class="comment-card">
        <div class="comment-header">
          <div class="user-info">
            <img :src="comment.avatar" :alt="comment.author" class="avatar">
            <div class="details">
              <span class="author">{{ comment.author }}</span>
              <span class="email">{{ comment.email }}</span>
            </div>
          </div>
          <div class="meta-info">
            <span class="date">{{ comment.date }}</span>
            <span :class="['status', comment.status]">{{ getStatusText(comment.status) }}</span>
          </div>
        </div>
        <div class="comment-content">
          <div class="post-title">
            文章：<a href="#" @click.prevent="viewPost(comment.postId)">{{ comment.postTitle }}</a>
          </div>
          <div class="comment-text">{{ comment.content }}</div>
        </div>
        <div class="comment-actions">
          <label class="checkbox">
            <input type="checkbox" v-model="selectedComments" :value="comment.id">
            <span class="checkmark"></span>
          </label>
          <div class="action-buttons">
            <button 
              v-if="comment.status === 'pending'" 
              class="btn success" 
              @click="handleApprove(comment)"
            >
              <i class="fas fa-check"></i> 通过
            </button>
            <button 
              v-if="comment.status === 'pending'" 
              class="btn danger" 
              @click="handleReject(comment)"
            >
              <i class="fas fa-times"></i> 拒绝
            </button>
            <button class="btn-icon" @click="handleReply(comment)">
              <i class="fas fa-reply"></i>
            </button>
            <button class="btn-icon" @click="handleDelete(comment)">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 回复评论对话框 -->
    <div v-if="showReplyDialog" class="dialog-overlay" @click.self="showReplyDialog = false">
      <div class="dialog">
        <h2>回复评论</h2>
        <form @submit.prevent="submitReply">
          <div class="form-group">
            <label>回复内容</label>
            <textarea v-model="replyForm.content" rows="4" required></textarea>
          </div>
          <div class="dialog-actions">
            <button type="button" class="btn" @click="showReplyDialog = false">取消</button>
            <button type="submit" class="btn primary">发送回复</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue';

// 模拟数据
const comments = ref([
  {
    id: 1,
    author: '张三',
    email: 'zhangsan@example.com',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=1',
    content: '这篇文章写得很好，对我帮助很大！',
    date: '2024-01-15 14:30',
    status: 'approved',
    postId: 1,
    postTitle: '2024年Web开发趋势展望'
  },
  {
    id: 2,
    author: '李四',
    email: 'lisi@example.com',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=2',
    content: '文章中关于Vue3的部分还可以再详细一些。',
    date: '2024-01-15 15:45',
    status: 'pending',
    postId: 1,
    postTitle: '2024年Web开发趋势展望'
  },
  {
    id: 3,
    author: '王五',
    email: 'wangwu@example.com',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=3',
    content: '期待更多相关内容！',
    date: '2024-01-15 16:20',
    status: 'rejected',
    postId: 2,
    postTitle: 'Vue3组合式API最佳实践'
  }
]);

// 状态管理
const searchQuery = ref('');
const statusFilter = ref('all');
const selectedComments = ref([]);
const showReplyDialog = ref(false);
const replyForm = reactive({
  content: '',
  commentId: null
});

// 计算属性
const filteredComments = computed(() => {
  return comments.value.filter(comment => {
    const matchesSearch = comment.content.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         comment.author.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesStatus = statusFilter.value === 'all' || comment.status === statusFilter.value;
    return matchesSearch && matchesStatus;
  });
});

// 方法
const getStatusText = (status) => {
  const statusMap = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝'
  };
  return statusMap[status] || status;
};

const handleApprove = (comment) => {
  // 实现通过评论逻辑
  console.log('Approve comment:', comment);
};

const handleReject = (comment) => {
  // 实现拒绝评论逻辑
  console.log('Reject comment:', comment);
};

const handleReply = (comment) => {
  replyForm.commentId = comment.id;
  showReplyDialog.value = true;
};

const handleDelete = (comment) => {
  if (confirm(`确定要删除这条评论吗？`)) {
    // 实现删除评论逻辑
    console.log('Delete comment:', comment);
  }
};

const handleBatchDelete = () => {
  if (confirm(`确定要删除选中的 ${selectedComments.value.length} 条评论吗？`)) {
    // 实现批量删除逻辑
    console.log('Batch delete comments:', selectedComments.value);
    selectedComments.value = [];
  }
};

const submitReply = () => {
  // 实现提交回复逻辑
  console.log('Submit reply:', replyForm);
  showReplyDialog.value = false;
  replyForm.content = '';
  replyForm.commentId = null;
};

const viewPost = (postId) => {
  // 实现查看文章逻辑
  console.log('View post:', postId);
};
</script>

<style scoped>
.comments-manager {
  padding: 20px;
}

.action-bar {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left {
  display: flex;
  gap: 16px;
  align-items: center;
}

.search-box {
  position: relative;
}

.search-box input {
  padding: 8px 32px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  width: 200px;
  background: var(--bg-color);
  color: var(--text-color);
}

.search-box i {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-color);
  opacity: 0.5;
}

.filter-box select {
  padding: 8px 12px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  background: var(--border-color);
  color: var(--text-color);
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-card {
  border-radius: 12px;
  padding: 20px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.user-info {
  display: flex;
  gap: 12px;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.details {
  display: flex;
  flex-direction: column;
}

.author {
  font-weight: 500;
  color: var(--text-color);
}

.email {
  font-size: 0.9rem;
  color: var(--text-color);
  opacity: 0.7;
}

.meta-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.date {
  font-size: 0.9rem;
  color: var(--text-color);
  opacity: 0.7;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.status.pending {
  background: #ffd700;
  color: #000;
}

.status.approved {
  background: #4caf50;
  color: #fff;
}

.status.rejected {
  background: #f44336;
  color: #fff;
}

.comment-content {
  margin-bottom: 16px;
}

.post-title {
  margin-bottom: 8px;
  font-size: 0.9rem;
  color: var(--text-color);
  opacity: 0.8;
}

.post-title a {
  color: #1976d2;
  text-decoration: none;
}

.post-title a:hover {
  text-decoration: underline;
}

.comment-text {
  color: var(--text-color);
  line-height: 1.5;
}

.comment-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
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

.btn-icon {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.05);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  color: var(--text-color);
}

.btn-icon:hover {
  background: rgba(0, 0, 0, 0.1);
}

.btn.success {
  background: #4caf50;
  color: white;
}

.btn.danger {
  background: #f44336;
  color: white;
}

/* 对话框样式 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog {
  background: var(--border-color);
  border-radius: 12px;
  padding: 24px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.dialog h2 {
  margin: 0 0 20px 0;
  color: var(--text-color);
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: var(--text-color);
}

.form-group textarea {
  width: 93%;
  padding: 8px 16px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  resize: vertical;
  background: var(--background-lighter);
  color: var(--text-color);
}

.dialog-actions {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

</style> 