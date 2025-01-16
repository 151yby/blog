<template>
  <div class="tags-manager">
    <!-- 顶部操作栏 -->
    <div class="action-bar">
      <div class="left">
        <button class="btn primary" @click="showCreateDialog = true">
          <i class="fas fa-plus"></i> 新建标签
        </button>
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input type="text" v-model="searchQuery" placeholder="搜索标签...">
        </div>
      </div>
    </div>

    <!-- 标签列表 -->
    <div class="tags-grid">
      <div v-for="tag in filteredTags" :key="tag.id" class="tag-card">
        <div class="tag-header" :style="{ backgroundColor: tag.color }">
          <i class="fas fa-tag"></i>
          <span class="tag-name">{{ tag.name }}</span>
          <div class="tag-actions">
            <button class="btn-icon" @click="handleEdit(tag)">
              <i class="fas fa-edit"></i>
            </button>
            <button class="btn-icon" @click="handleDelete(tag)">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
        <div class="tag-content">
          <div class="tag-stats">
            <div class="stat-item">
              <i class="fas fa-file-alt"></i>
              <span>{{ tag.postCount }} 篇文章</span>
            </div>
            <div class="stat-item">
              <i class="fas fa-eye"></i>
              <span>{{ tag.views }} 次浏览</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 新建/编辑标签对话框 -->
    <div v-if="showCreateDialog" class="dialog-overlay" @click.self="showCreateDialog = false">
      <div class="dialog">
        <h2>{{ editingTag ? '编辑标签' : '新建标签' }}</h2>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>标签名称</label>
            <input type="text" v-model="tagForm.name" required>
          </div>
          <div class="form-group">
            <label>颜色</label>
            <div class="color-selector">
              <button 
                v-for="color in availableColors" 
                :key="color"
                type="button"
                :class="['color-option', { active: tagForm.color === color }]"
                :style="{ backgroundColor: color }"
                @click="tagForm.color = color"
              ></button>
            </div>
          </div>
          <div class="dialog-actions">
            <button type="button" class="btn" @click="showCreateDialog = false">取消</button>
            <button type="submit" class="btn primary">确定</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue';

// State
const loading = ref(false);
const error = ref(null);

// Mock data
const mockTags = [
  {
    id: 1,
    name: 'JavaScript',
    color: '#f7df1e',
    postCount: 15,
    views: 1250
  },
  {
    id: 2,
    name: 'Vue.js',
    color: '#42b883',
    postCount: 8,
    views: 986
  },
  {
    id: 3,
    name: 'Python',
    color: '#3776ab',
    postCount: 12,
    views: 1568
  },
  {
    id: 4,
    name: 'React',
    color: '#61dafb',
    postCount: 6,
    views: 842
  },
  {
    id: 5,
    name: 'Node.js',
    color: '#339933',
    postCount: 9,
    views: 1123
  },
  {
    id: 6,
    name: 'Docker',
    color: '#2496ed',
    postCount: 4,
    views: 567
  }
];

const tags = ref(mockTags);

// API calls (commented out for now)
const fetchTags = async () => {
  loading.value = true;
  error.value = null;
  try {
    // const response = await api.get('/tags');
    // tags.value = response.data;
    tags.value = mockTags; // Using mock data
  } catch (err) {
    error.value = err.message;
    console.error('Failed to fetch tags:', err);
  } finally {
    loading.value = false;
  }
};

const createTag = async (tag) => {
  loading.value = true;
  error.value = null;
  try {
    // const response = await api.post('/tags', tag);
    // return response.data;
    // Mock create
    const newTag = {
      ...tag,
      id: tags.value.length + 1,
      postCount: 0,
      views: 0
    };
    tags.value.push(newTag);
    return newTag;
  } catch (err) {
    error.value = err.message;
    throw err;
  } finally {
    loading.value = false;
  }
};

const updateTag = async (id, tag) => {
  loading.value = true;
  error.value = null;
  try {
    // const response = await api.put(`/tags/${id}`, tag);
    // return response.data;
    // Mock update
    const index = tags.value.findIndex(t => t.id === id);
    if (index !== -1) {
      tags.value[index] = {
        ...tags.value[index],
        ...tag
      };
      return tags.value[index];
    }
  } catch (err) {
    error.value = err.message;
    throw err;
  } finally {
    loading.value = false;
  }
};

const deleteTag = async (id) => {
  loading.value = true;
  error.value = null;
  try {
    // await api.delete(`/tags/${id}`);
    // Mock delete
    tags.value = tags.value.filter(t => t.id !== id);
  } catch (err) {
    error.value = err.message;
    throw err;
  } finally {
    loading.value = false;
  }
};

// 可选颜色
const availableColors = [
  '#f7df1e', // JavaScript
  '#42b883', // Vue
  '#3776ab', // Python
  '#61dafb', // React
  '#339933', // Node
  '#2496ed', // Docker
  '#e34c26', // HTML
  '#264de4', // CSS
  '#764abc'  // Redux
];

// 搜索和状态管理
const searchQuery = ref('');
const showCreateDialog = ref(false);
const editingTag = ref(null);
const tagForm = reactive({
  name: '',
  color: availableColors[0]
});

// 计算属性
const filteredTags = computed(() => {
  return tags.value.filter(tag =>
    tag.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// 方法
const handleEdit = (tag) => {
  editingTag.value = tag;
  Object.assign(tagForm, tag);
  showCreateDialog.value = true;
};

const handleDelete = async (tag) => {
  if (confirm(`确定要删除标签"${tag.name}"吗？注意：删除标签不会删除相关文章，但会移除文章与该标签的关联！`)) {
    try {
      await deleteTag(tag.id);
    } catch (err) {
      console.error('Failed to delete tag:', err);
    }
  }
};

const handleSubmit = async () => {
  try {
    if (editingTag.value) {
      await updateTag(editingTag.value.id, tagForm);
    } else {
      await createTag(tagForm);
    }
    showCreateDialog.value = false;
    editingTag.value = null;
    // Reset form
    Object.assign(tagForm, {
      name: '',
      color: availableColors[0]
    });
  } catch (err) {
    console.error('Failed to save tag:', err);
  }
};

// Initialize
onMounted(() => {
  fetchTags();
});
</script>

<style scoped>
.tags-manager {
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

.tags-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.tag-card {
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.tag-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
}

.tag-header {
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(0, 0, 0, 0.8);
}

.tag-name {
  flex: 1;
  font-weight: 500;
  font-size: 1.1rem;
}

.tag-actions {
  display: flex;
  gap: 8px;
}

.tag-content {
  padding: 16px;
}

.tag-stats {
  display: flex;
  justify-content: space-around;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-color);
  opacity: 0.8;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.2);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  color: rgba(0, 0, 0, 0.6);
}

.btn-icon:hover {
  background: rgba(255, 255, 255, 0.3);
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
  background-color: var(--background-lighter);
  border-radius: 12px;
  padding: 24px;
  width: 90%;
  max-width: 500px;
  box-shadow: var(--box-shadow);
}

.dialog h2 {
  margin: 0 0 20px 0;
  color: var(--text-primary);
  font-size: 18px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: var(--text-primary);
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--background-light);
  color: var(--text-primary);
  transition: all 0.3s;
}

.form-group input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px var(--primary-color) + '1A';
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
  box-shadow: var(--box-shadow);
}

.dialog-actions {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 深色模式适配 */
:root.dark-mode {
  .search-box input {
    border-color: rgba(255, 255, 255, 0.1);
  }

  .tag-header {
    color: rgba(255, 255, 255, 0.9);
  }

  .btn-icon {
    color: rgba(255, 255, 255, 0.9);
  }

  .form-group input {
    border-color: rgba(255, 255, 255, 0.1);
  }
}
</style> 