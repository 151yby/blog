<template>
  <div class="categories-manager">
    <!-- 顶部操作栏 -->
    <div class="action-bar">
      <button class="btn primary" @click="showCreateDialog = true">
        <i class="fas fa-plus"></i> 新建分类
      </button>
    </div>

    <!-- 分类列表 -->
    <div class="categories-grid">
      <div v-for="category in categories" :key="category.id" class="category-card">
        <div class="category-icon" :style="{ backgroundColor: category.color }">
          <i :class="category.icon"></i>
        </div>
        <div class="category-info">
          <h3>{{ category.name }}</h3>
          <p class="description">{{ category.description }}</p>
          <div class="stats">
            <span><i class="fas fa-file-alt"></i> {{ category.postCount }} 篇文章</span>
          </div>
        </div>
        <div class="category-actions">
          <button class="btn-icon" @click="handleEdit(category)">
            <i class="fas fa-edit"></i>
          </button>
          <button class="btn-icon" @click="handleDelete(category)">
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- 新建/编辑分类对话框 -->
    <div v-if="showCreateDialog" class="dialog-overlay" @click.self="showCreateDialog = false">
      <div class="dialog">
        <h2>{{ editingCategory ? '编辑分类' : '新建分类' }}</h2>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>分类名称</label>
            <input type="text" v-model="categoryForm.name" required>
          </div>
          <div class="form-group">
            <label>描述</label>
            <textarea v-model="categoryForm.description" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>图标</label>
            <div class="icon-selector">
              <button v-for="icon in availableIcons" :key="icon" type="button"
                :class="['icon-option', { active: categoryForm.icon === icon }]" @click="categoryForm.icon = icon">
                <i :class="icon"></i>
              </button>
            </div>
          </div>
          <div class="form-group">
            <label>颜色</label>
            <div class="color-selector">
              <button v-for="color in availableColors" :key="color" type="button"
                :class="['color-option', { active: categoryForm.color === color }]" :style="{ backgroundColor: color }"
                @click="categoryForm.color = color"></button>
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
import { ref, reactive, onMounted } from 'vue';
// import { useApi } from '@/composables/useApi';
// const api = useApi();

// State
const loading = ref(false);
const error = ref(null);

// Mock data
const mockCategories = [
  {
    id: 1,
    name: '技术',
    description: '技术相关的文章和教程',
    icon: 'fas fa-code',
    color: '#1976d2',
    postCount: 25
  },
  {
    id: 2,
    name: '生活',
    description: '日常生活的记录和感悟',
    icon: 'fas fa-coffee',
    color: '#388e3c',
    postCount: 15
  },
  {
    id: 3,
    name: '阅读',
    description: '读书笔记和心得分享',
    icon: 'fas fa-book',
    color: '#e64a19',
    postCount: 8
  },
  {
    id: 4,
    name: '设计',
    description: 'UI/UX设计相关内容',
    icon: 'fas fa-palette',
    color: '#7b1fa2',
    postCount: 12
  }
];

const categories = ref(mockCategories);

// API calls (commented out for now)
const fetchCategories = async () => {
  loading.value = true;
  error.value = null;
  try {
    // const response = await api.get('/categories');
    // categories.value = response.data;
    categories.value = mockCategories; // Using mock data
  } catch (err) {
    error.value = err.message;
    console.error('Failed to fetch categories:', err);
  } finally {
    loading.value = false;
  }
};

const createCategory = async (category) => {
  loading.value = true;
  error.value = null;
  try {
    // const response = await api.post('/categories', category);
    // return response.data;
    // Mock create
    const newCategory = {
      ...category,
      id: categories.value.length + 1,
      postCount: 0
    };
    categories.value.push(newCategory);
    return newCategory;
  } catch (err) {
    error.value = err.message;
    throw err;
  } finally {
    loading.value = false;
  }
};

const updateCategory = async (id, category) => {
  loading.value = true;
  error.value = null;
  try {
    // const response = await api.put(`/categories/${id}`, category);
    // return response.data;
    // Mock update
    const index = categories.value.findIndex(c => c.id === id);
    if (index !== -1) {
      categories.value[index] = {
        ...categories.value[index],
        ...category
      };
      return categories.value[index];
    }
  } catch (err) {
    error.value = err.message;
    throw err;
  } finally {
    loading.value = false;
  }
};

const deleteCategory = async (id) => {
  loading.value = true;
  error.value = null;
  try {
    // await api.delete(`/categories/${id}`);
    // Mock delete
    categories.value = categories.value.filter(c => c.id !== id);
  } catch (err) {
    error.value = err.message;
    throw err;
  } finally {
    loading.value = false;
  }
};

// 可选图标
const availableIcons = [
  'fas fa-code',
  'fas fa-coffee',
  'fas fa-book',
  'fas fa-palette',
  'fas fa-music',
  'fas fa-film',
  'fas fa-camera',
  'fas fa-pen',
  'fas fa-heart',
  'fas fa-star'
];

// 可选颜色
const availableColors = [
  '#1976d2',
  '#388e3c',
  '#e64a19',
  '#7b1fa2',
  '#c2185b',
  '#00796b',
  '#f57c00',
  '#455a64'
];

// 表单状态
const showCreateDialog = ref(false);
const editingCategory = ref(null);
const categoryForm = reactive({
  name: '',
  description: '',
  icon: 'fas fa-code',
  color: '#1976d2'
});

// 方法
const handleEdit = (category) => {
  editingCategory.value = category;
  Object.assign(categoryForm, category);
  showCreateDialog.value = true;
};

const handleDelete = async (category) => {
  if (confirm(`确定要删除分类"${category.name}"吗？注意：删除分类将会同时删除该分类下的所有文章！`)) {
    try {
      await deleteCategory(category.id);
    } catch (err) {
      console.error('Failed to delete category:', err);
    }
  }
};

const handleSubmit = async () => {
  try {
    if (editingCategory.value) {
      await updateCategory(editingCategory.value.id, categoryForm);
    } else {
      await createCategory(categoryForm);
    }
    showCreateDialog.value = false;
    editingCategory.value = null;
    // Reset form
    Object.assign(categoryForm, {
      name: '',
      description: '',
      icon: 'fas fa-code',
      color: '#1976d2'
    });
  } catch (err) {
    console.error('Failed to save category:', err);
  }
};

// Initialize
onMounted(() => {
  fetchCategories();
});
</script>

<style scoped>
.categories-manager {
  padding: 20px;
}

.action-bar {
  margin-bottom: 20px;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.category-card {
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  transition: all 0.3s ease;
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
}

.category-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.category-icon i {
  font-size: 20px;
  color: white;
}

.category-info {
  flex: 1;
}

.category-info h3 {
  margin: 0 0 8px 0;
  color: var(--text-color);
  font-size: 1.1rem;
}

.description {
  margin: 0 0 12px 0;
  color: var(--text-color);
  opacity: 0.8;
  font-size: 0.9rem;
}

.stats {
  font-size: 0.85rem;
  color: var(--text-color);
  opacity: 0.7;
}

.stats i {
  margin-right: 4px;
}

.category-actions {
  display: flex;
  gap: 8px;
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

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--background-light);
  color: var(--text-primary);
  transition: all 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px var(--primary-color) + '1A';
}

.icon-selector,
.color-selector {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
  gap: 8px;
}

.icon-option,
.color-option {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.icon-option {
  background-color: var(--background-light);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.icon-option:hover {
  background-color: var(--primary-color) + '1A';
  color: var(--primary-color);
}

.icon-option.active {
  background-color: var(--primary-color);
  color: #fff;
  transform: scale(1.1);
  box-shadow: var(--box-shadow);
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
  .icon-option {
    background: rgba(255, 255, 255, 0.1);
  }

  .form-group input,
  .form-group textarea {
    border-color: rgba(255, 255, 255, 0.1);
  }
}
</style> 