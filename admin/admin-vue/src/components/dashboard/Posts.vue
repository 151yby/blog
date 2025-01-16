<template>
  <div class="posts-manager">
    <!-- 顶部操作栏 -->
    <div class="action-bar">
      <div class="left">
        <button class="btn primary" @click="handleCreatePost">
          <i class="fas fa-plus"></i> 新建文章
        </button>
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input type="text" v-model="searchQuery" placeholder="搜索文章...">
        </div>
        <div class="filter-box">
          <select v-model="categoryFilter">
            <option value="">全部分类</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
          <select v-model="statusFilter">
            <option value="">全部状态</option>
            <option value="draft">草稿</option>
            <option value="published">已发布</option>
          </select>
        </div>
      </div>
      <div class="right">
        <button class="btn" @click="handleBatchDelete" :disabled="!selectedPosts.length">
          <i class="fas fa-trash"></i> 
          批量删除
        </button>
      </div>
    </div>

    <!-- 文章列表 -->
    <div class="posts-list">
      <div v-if="loading" class="loading">
        <i class="fas fa-spinner fa-spin"></i> 加载中...
      </div>
      <div v-else-if="!posts.length" class="empty-state">
        暂无文章
      </div>
      <div v-else v-for="post in filteredPosts" :key="post?.id" class="post-card">
        <!-- 选择框 -->
        <div class="checkbox-wrapper">
          <div 
            class="checkbox" 
            :class="{ checked: selectedPosts.includes(post.id) }"
            @click="toggleSelect(post.id)"
          ></div>
        </div>
        <div class="post-header">
          <div class="post-info">
            <h3 class="post-title">{{ post?.title || '无标题' }}</h3>
            <div class="post-meta">
              <span class="date">{{ formatDate(post?.date) }}</span>
              <span class="author">{{ post?.author || '未知作者' }}</span>
              <span v-if="post?.category" class="category" :style="{ backgroundColor: post.category.color }">
                {{ post.category.name }}
              </span>
              <span class="status" :class="post?.status">{{ getStatusText(post?.status) }}</span>
              <div class="tags">
                <span v-for="tag in (post?.tags || [])" :key="tag" class="tag">{{ tag }}</span>
              </div>
            </div>
          </div>
          <div class="post-actions">
            <button class="btn-icon" @click="handlePreview(post)" title="预览">
              <i class="fas fa-eye"></i>
            </button>
            <button class="btn-icon" @click="handleEdit(post)" title="编辑">
              <i class="fas fa-edit"></i>
            </button>
            <button class="btn-icon" @click="toggleStatus(post)" :title="post?.status === 'draft' ? '发布' : '转为草稿'">
              <i :class="post?.status === 'draft' ? 'fas fa-cloud-upload-alt' : 'fas fa-cloud-download-alt'"></i>
            </button>
            <button class="btn-icon delete" @click="handleDelete(post)" title="删除">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
        <div class="post-excerpt">
          {{ getExcerpt(post?.content || '') }}
        </div>
        <div class="post-stats">
          <span><i class="fas fa-eye"></i> {{ post?.views || 0 }}</span>
          <span><i class="fas fa-comment"></i> {{ post?.comments || 0 }}</span>
          <span><i class="fas fa-heart"></i> {{ post?.likes || 0 }}</span>
        </div>
      </div>
    </div>

    <!-- 分页器 -->
    <div class="pagination">
      <button class="btn" :disabled="currentPage === 1" @click="currentPage--">
        <i class="fas fa-chevron-left"></i>
      </button>
      <span class="page-info">第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
      <button class="btn" :disabled="currentPage === totalPages" @click="currentPage++">
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>

    <!-- 编辑器对话框 -->
    <div v-if="showEditor" class="editor-overlay" @click.self="closeEditor">
      <div class="editor">
        <div class="editor-header">
          <h2>{{ editingPost ? '编辑文章' : '新建文章' }}</h2>
          <button class="btn-icon" @click="closeEditor">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <form @submit.prevent="handleSubmit" class="editor-form">
          <div class="form-group">
            <label>标题</label>
            <input 
              type="text" 
              v-model="postForm.title" 
              placeholder="请输入文章标题"
              required
            >
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>分类</label>
              <select v-model="postForm.categoryId" required>
                <option value="">请选择分类</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>状态</label>
              <select v-model="postForm.status">
                <option value="draft">草稿</option>
                <option value="published">发布</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>标签</label>
            <div class="tags-input">
              <div v-for="tag in postForm.tags" :key="tag" class="tag">
                {{ tag }}
                <button type="button" @click="removeTag(tag)" class="remove-tag">×</button>
              </div>
              <input 
                type="text" 
                v-model="tagInput" 
                @keydown.enter.prevent="addTag"
                placeholder="输入标签后按回车"
              >
            </div>
          </div>
          <div class="form-group">
            <label>内容</label>
            <textarea 
              v-model="postForm.content" 
              rows="15" 
              placeholder="请输入文章内容（支持Markdown格式）"
              required
            ></textarea>
          </div>
          <div class="editor-actions">
            <button type="button" class="cancel" @click="closeEditor">取消</button>
            <button type="submit" class="primary" :disabled="submitting">
              {{ submitting ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, nextTick } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import axios from 'axios';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import dayjs from 'dayjs';

// API 配置
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';
const API = {
  posts: `${API_BASE_URL}/api/posts/`,
  categories: `${API_BASE_URL}/api/categories/`,
  tags: `${API_BASE_URL}/api/tags/`,
  upload: `${API_BASE_URL}/api/posts/upload-image/`
};

// 模拟数据
const mockPosts = [
  {
    id: 1,
    title: '2025年Web开发趋势展望',
    excerpt: '随着技术的不断发展，Web开发领域在2024年将会有哪些新的趋势和变化？本文将为您详细解析...',
    content: '文章内容...',
    date: '2024-01-15',
    author: 'Admin',
    category: { id: 1, name: '技术', color: '#1976d2' },
    tags: ['Web开发', '趋势', '技术'],
    status: 'published',
    views: 1250,
    comments: 8,
    likes: 45
  },
  {
    id: 2,
    title: 'Vue3组合式API最佳实践',
    excerpt: 'Vue3的组合式API为我们提供了更好的代码组织方式，本文将介绍一些实用的最佳实践...',
    content: '文章内容...',
    date: '2024-01-14',
    author: 'Admin',
    category: { id: 1, name: '技术', color: '#1976d2' },
    tags: ['Vue3', 'JavaScript', '前端'],
    status: 'draft',
    views: 980,
    comments: 5,
    likes: 32
  }
];

// 模拟分类数据
const mockCategories = [
  { id: 1, name: '技术', color: '#1976d2' },
  { id: 2, name: '生活', color: '#388e3c' },
  { id: 3, name: '阅读', color: '#e64a19' }
];

// 状态管理
const loading = ref(true);          // 加载状态，默认为true
const submitting = ref(false);       // 提交状态
const posts = ref([]);              // 文章列表，初始为空数组
const categories = ref([]);         // 分类列表，初始为空数组
const tags = ref([]);               // 标签列表
const searchQuery = ref('');        // 搜索关键词
const categoryFilter = ref('');     // 分类筛选
const statusFilter = ref('');       // 状态筛选
const selectedPosts = ref([]);      // 选中的文章
const currentPage = ref(1);         // 当前页码
const pageSize = ref(10);          // 每页显示数量
const total = ref(0);              // 总记录数
const showEditor = ref(false);      // 编辑器显示状态
const editingPost = ref(null);      // 正在编辑的文章
const tagInput = ref('');           // 标签输入
const useApi = ref(false);          // 默认使用模拟数据

// 表单状态
const postForm = reactive({
  title: '',           // 文章标题
  categoryId: '',      // 分类ID
  status: 'draft',     // 文章状态
  tags: [],           // 文章标签
  content: ''         // 文章内容
});

// 计算属性：总页数
const totalPages = computed(() => Math.ceil(total.value / pageSize.value));

// 计算属性：根据筛选条件过滤文章列表
const filteredPosts = computed(() => {
  return posts.value.filter(post => {
    if (!post) return false;

    const matchesSearch = (post.title || '').toLowerCase().includes((searchQuery.value || '').toLowerCase());
    const matchesCategory = !categoryFilter.value || post.category?.id === parseInt(categoryFilter.value);
    const matchesStatus = !statusFilter.value || post.status === statusFilter.value;
    return matchesSearch && matchesCategory && matchesStatus;
  });
});

// 初始化数据
const initData = async () => {
  loading.value = true;
  try {
    // 先设置模拟数据作为默认值
    posts.value = [...mockPosts];
    categories.value = [...mockCategories];
    total.value = mockPosts.length;

    if (useApi.value) {
      // 如果使用API，尝试获取真实数据
      await Promise.all([
        fetchPosts(),
        fetchCategories(),
        fetchTags()
      ]);
    } else {
      // 使用模拟数据时，从模拟文章中提取标签
      tags.value = Array.from(new Set(mockPosts.flatMap(post => post.tags || [])));
    }
  } catch (error) {
    console.error('初始化数据错误:', error);
    ElMessage.warning('初始化数据失败，使用模拟数据');
  } finally {
    loading.value = false;
  }
};

// 修改 fetchPosts 方法
const fetchPosts = async () => {
  if (!useApi.value) return;

  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value,
      category: categoryFilter.value,
      status: statusFilter.value
    };
    const response = await axios.get(API.posts, { params });
    if (response?.data?.results) {
      posts.value = response.data.results;
      total.value = response.data.count;
    }
  } catch (error) {
    console.error('获取文章列表错误:', error);
    ElMessage.warning('获取文章列表失败');
  }
};

// 修改 fetchCategories 方法
const fetchCategories = async () => {
  if (!useApi.value) return;

  try {
    const response = await axios.get(API.categories);
    if (response?.data) {
      categories.value = response.data;
    }
  } catch (error) {
    console.error('获取分类列表错误:', error);
    ElMessage.warning('获取分类列表失败');
  }
};

// 修改 fetchTags 方法
const fetchTags = async () => {
  if (!useApi.value) return;

  try {
    const response = await axios.get(API.tags);
    if (response?.data) {
      tags.value = response.data;
    }
  } catch (error) {
    console.error('获取标签列表错误:', error);
    ElMessage.warning('获取标签列表失败');
  }
};

// 文章操作方法
const handleCreatePost = () => {
  editingPost.value = null;
  Object.assign(postForm, {
    title: '',
    categoryId: '',
    status: 'draft',
    tags: [],
    content: ''
  });
  showEditor.value = true;
};

const handleEdit = async (post) => {
  try {
    if (!useApi.value) {
      editingPost.value = post;
      Object.assign(postForm, {
        title: post.title,
        categoryId: post?.category?.id || '',
        status: post.status,
        tags: post.tags || [],
        content: post.content
      });
      showEditor.value = true;
      return;
    }

    const response = await axios.get(`${API.posts}${post.id}/`);
    editingPost.value = response.data;
    Object.assign(postForm, {
      title: response.data.title,
      categoryId: response.data.category?.id || '',
      status: response.data.status,
      tags: response.data.tags?.map(tag => tag.name) || [],
      content: response.data.content
    });
    showEditor.value = true;
  } catch (error) {
    console.error('获取文章详情错误:', error);
    if (useApi.value) {
      ElMessage.error('获取文章详情失败');
      // 如果API调用失败，使用传入的post数据
      editingPost.value = post;
      Object.assign(postForm, {
        title: post.title,
        categoryId: post?.category?.id || '',
        status: post.status,
        tags: post.tags || [],
        content: post.content
      });
      showEditor.value = true;
    }
  }
};

const handlePreview = (post) => {
  // 在新窗口中预览文章
  const previewWindow = window.open('', '_blank');
  const renderedContent = DOMPurify.sanitize(marked(post.content || ''));
  previewWindow.document.write(`
    <html>
      <head>
        <title>${post.title} - 预览</title>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }
          img { max-width: 100%; }
          pre { background: #f4f4f4; padding: 15px; border-radius: 5px; }
          code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
        </style>
      </head>
      <body>
        <h1>${post.title}</h1>
        <div>${renderedContent}</div>
      </body>
    </html>
  `);
};

const handleDelete = async (post) => {
  if (!post?.id) return;

  try {
    await ElMessageBox.confirm(
      '确定要删除这篇文章吗？此操作不可恢复！',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    );

    if (useApi.value) {
      await axios.delete(`${API.posts}${post.id}/`);
    } else {
      const index = posts.value.findIndex(p => p.id === post.id);
      if (index > -1) {
        posts.value.splice(index, 1);
      }
    }

    ElMessage.success('删除成功');
    fetchPosts();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
      console.error('删除文章错误:', error);
    }
  }
};

const handleBatchDelete = async () => {
  if (!selectedPosts.value.length) return;

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedPosts.value.length} 篇文章吗？此操作不可恢复！`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    );

    if (useApi.value) {
      await axios.post(`${API.posts}batch-delete/`, { ids: selectedPosts.value });
    } else {
      posts.value = posts.value.filter(post => !selectedPosts.value.includes(post.id));
    }

    ElMessage.success('批量删除成功');
    selectedPosts.value = [];
    fetchPosts();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败');
      console.error('批量删除文章错误:', error);
    }
  }
};

// 标签操作方法
const addTag = () => {
  const tag = tagInput.value.trim();
  if (tag && !postForm.tags.includes(tag)) {
    postForm.tags.push(tag);
  }
  tagInput.value = '';
};

const removeTag = (tag) => {
  const index = postForm.tags.indexOf(tag);
  if (index > -1) {
    postForm.tags.splice(index, 1);
  }
};

// 表单提交方法
const handleSubmit = async () => {
  if (submitting.value) return;

  submitting.value = true;
  try {
    const postData = {
      title: postForm.title.trim(),
      category_id: parseInt(postForm.categoryId) || null,
      status: postForm.status,
      content: postForm.content.trim(),
      tags: postForm.tags.map(tag => tag.trim()).filter(Boolean)
    };

    if (useApi.value) {
      if (editingPost.value) {
        await axios.put(`${API.posts}${editingPost.value.id}/`, postData);
      } else {
        await axios.post(API.posts, postData);
      }
    } else {
      // 使用模拟数据的保存逻辑
      if (editingPost.value) {
        const index = posts.value.findIndex(p => p.id === editingPost.value.id);
        if (index > -1) {
          const category = categories.value.find(c => c.id === parseInt(postData.category_id));
          posts.value[index] = {
            ...posts.value[index],
            ...postData,
            category: category || posts.value[index].category
          };
        }
      } else {
        const category = categories.value.find(c => c.id === parseInt(postData.category_id));
        posts.value.unshift({
          id: Math.max(0, ...posts.value.map(p => p.id)) + 1,
          ...postData,
          date: dayjs().format('YYYY-MM-DD'),
          author: 'Admin',
          category: category || { id: 0, name: '未分类', color: '#999999' },
          views: 0,
          comments: 0,
          likes: 0
        });
      }
    }

    ElMessage.success(editingPost.value ? '更新成功' : '创建成功');
    showEditor.value = false;
    await fetchPosts();
  } catch (error) {
    console.error('保存文章错误:', error);
    ElMessage.error(editingPost.value ? '更新失败' : '创建失败');
  } finally {
    submitting.value = false;
  }
};

// 状态切换方法
const toggleStatus = async (post) => {
  try {
    if (useApi.value) {
      await axios.post(`/api/posts/${post.id}/toggle_status/`);
    } else {
      // 使用模拟数据时的状态切换
      const index = posts.value.findIndex(p => p.id === post.id);
      if (index > -1) {
        posts.value[index].status = post.status === 'draft' ? 'published' : 'draft';
      }
    }

    ElMessage.success(
      post.status === 'draft' ? '文章已发布' : '文章已转为草稿'
    );
    fetchPosts();
  } catch (error) {
    ElMessage.error('更改文章状态失败');
    console.error('切换文章状态错误:', error);
  }
};

// 工具方法
const formatDate = (date) => {
  if (!date) return '未知日期';
  return dayjs(date).format('YYYY-MM-DD HH:mm');
};

const getStatusText = (status) => {
  const statusMap = {
    draft: '草稿',
    published: '已发布'
  };
  return statusMap[status] || '未知状态';
};

const getExcerpt = (content = '', length = 200) => {
  if (!content) return '';
  const plainText = content.replace(/[#*`]/g, '');
  return plainText.length > length ? plainText.slice(0, length) + '...' : plainText;
};

// 搜索和筛选方法
const handleSearch = () => {
  currentPage.value = 1;
  fetchPosts();
};

const handleFilter = () => {
  currentPage.value = 1;
  fetchPosts();
};

const handlePageChange = (page) => {
  currentPage.value = page;
  fetchPosts();
};

// 图片上传方法
const handleImageUpload = async (file) => {
  try {
    if (!file) {
      ElMessage.warning('请选择要上传的图片');
      return;
    }

    // 验证文件类型和大小
    const isImage = /^image\/(jpeg|png|gif|webp)$/.test(file.type);
    if (!isImage) {
      ElMessage.warning('只能上传图片文件');
      return;
    }

    const isLt2M = file.size / 1024 / 1024 < 2;
    if (!isLt2M) {
      ElMessage.warning('图片大小不能超过 2MB');
      return;
    }

    if (useApi.value) {
      const formData = new FormData();
      formData.append('image', file);
      const response = await axios.post(API.upload, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      const imageUrl = response.data.url;
      insertImageMarkdown(`![](${imageUrl})`);
    } else {
      const imageUrl = URL.createObjectURL(file);
      insertImageMarkdown(`![](${imageUrl})`);
    }

    ElMessage.success('图片上传成功');
  } catch (error) {
    console.error('上传图片错误:', error);
    ElMessage.error('图片上传失败');
  }
};

// 辅助方法：插入图片Markdown
const insertImageMarkdown = (markdown) => {
  const textarea = document.querySelector('.editor textarea');
  if (!textarea) return;

  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;
  const content = postForm.content;

  postForm.content =
    content.substring(0, start) +
    '\n' + markdown + '\n' +
    content.substring(end);

  // 更新光标位置
  nextTick(() => {
    textarea.focus();
    const newPosition = start + markdown.length + 2;
    textarea.setSelectionRange(newPosition, newPosition);
  });
};

// 选择框相关方法
const toggleSelect = (postId) => {
  const index = selectedPosts.value.indexOf(postId);
  if (index === -1) {
    selectedPosts.value.push(postId);
  } else {
    selectedPosts.value.splice(index, 1);
  }
};

// 关闭编辑器
const closeEditor = () => {
  if (submitting.value) return;
  
  showEditor.value = false;
  editingPost.value = null;
  Object.assign(postForm, {
    title: '',
    categoryId: '',
    status: 'draft',
    tags: [],
    content: ''
  });
  tagInput.value = '';
};

// 生命周期钩子
onMounted(() => {
  initData();
});
</script>

<style scoped>
.posts-manager {
  padding: 20px;
  background: var(--bg-color);
  min-height: calc(100vh - 60px);
}

/* 顶部操作栏 */
.action-bar {
  margin-bottom: 20px;
  padding: 16px;
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  width: 250px;
}

.search-box input {
  width: 77%;
  padding: 8px 32px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--background-lighter);
  color: var(--text-color);
  transition: all 0.3s;
}

.search-box input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.search-box i {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-light);
}

.filter-box {
  display: flex;
  gap: 8px;
}

.filter-box select {
  padding: 8px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--background-lighter);
  color: var(--text-color);
  min-width: 120px;
}

/* 文章列表 */
.posts-list {
  display: grid;
  gap: 16px;
  margin-bottom: 0px;
}

.post-card {
  height: 130px;
  background: var(--background-lighter);
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 11px 16px;
  transition: all 0.3s;
  position: relative;
  padding-left: 50px; /* 为选择框留出空间 */
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.post-info {
  flex: 1;
  min-width: 0;
}

.post-title {
  margin: 0 0 8px;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-color);
}

.post-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 14px;
  color: var(--text-light);
}

.category {
  padding: 2px 8px;
  border-radius: 12px;
  color: #fff;
  font-size: 12px;
}

.status {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.status.draft {
  background: var(--warning-color);
  color: #fff;
}

.status.published {
  background: var(--success-color);
  color: #fff;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 2px 8px;
  background: var(--tag-bg);
  color: var(--text-light);
  border-radius: 12px;
  font-size: 12px;
}

.post-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: var(--text-light);
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  background: var(--hover-bg);
  color: var(--primary-color);
}

.btn-icon.delete:hover {
  background: var(--danger-color);
  color: #fff;
}

.post-excerpt {
  margin: 12px 0;
  color: var(--text-light);
  font-size: 14px;
  line-height: 2;
}

.post-stats {
  line-height: 25px;
  display: flex;
  gap: 16px;
  color: var(--text-light);
  font-size: 14px;
}

.post-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 分页器 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
}

.page-info {
  color: var(--text-light);
}

/* 编辑器 */
.editor-overlay {
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

.editor {
  background: var(--background-light);
  border-radius: 8px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 1000px;
  max-height: 90vh;
  overflow-y: auto;
}

.editor-header {
  padding: 16px 24px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.editor-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--text-color);
}

.editor-form {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: var(--text-color);
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--background-lighter);
  color: var(--text-color);
  font-size: 14px;
  transition: all 0.3s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
  outline: none;
}

.form-group textarea {
  min-height: 200px;
  resize: vertical;
  line-height: 1.6;
}

.editor-actions {
  padding: 16px 24px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background: var(--background-lighter);
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}

.editor-actions button {
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 500;
  transition: all 0.3s;
}

.editor-actions button.primary {
  background: var(--primary-color);
  color: white;
  border: none;
}

.editor-actions button.primary:hover {
  background: var(--primary-hover);
}

.editor-actions button.cancel {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-color);
}

.editor-actions button.cancel:hover {
  background: var(--background-light);
  border-color: var(--text-color);
}

/* 按钮样式 */
.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn.primary {
  background: var(--primary-color);
  color: #fff;
}

.btn.primary:hover {
  background: var(--primary-hover);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 加载和空状态 */
.loading,
.empty-state {
  padding: 40px;
  text-align: center;
  color: var(--text-light);
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.loading i {
  margin-right: 8px;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .action-bar {
    flex-direction: column;
    gap: 16px;
  }

  .left {
    width: 100%;
  }

  .search-box {
    width: 100%;
  }

  .filter-box {
    width: 100%;
    flex-direction: column;
  }

  .post-header {
    flex-direction: column;
    gap: 12px;
  }

  .post-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .editor {
    width: 95%;
  }
}

/* 选择框样式 */
.checkbox-wrapper {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
}

.checkbox {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border-color);
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.checkbox.checked {
  background: var(--primary-color);
  border-color: var(--primary-color);
}

.checkbox.checked::after {
  content: '✓';
  color: white;
  font-size: 14px;
}
</style> 