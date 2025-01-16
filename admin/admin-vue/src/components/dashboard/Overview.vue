<template>
  <div class="overview">
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon articles">
          <i class="fas fa-file-alt"></i>
        </div>
        <div class="stat-info">
          <h3>文章总数</h3>
          <p class="number">{{ stats.articles }}</p>
          <p class="trend up">
            <i class="fas fa-arrow-up"></i>
            较上月增长 {{ stats.articlesGrowth }}%
          </p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon views">
          <i class="fas fa-eye"></i>
        </div>
        <div class="stat-info">
          <h3>总浏览量</h3>
          <p class="number">{{ stats.views }}</p>
          <p class="trend up">
            <i class="fas fa-arrow-up"></i>
            较上月增长 {{ stats.viewsGrowth }}%
          </p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon comments">
          <i class="fas fa-comments"></i>
        </div>
        <div class="stat-info">
          <h3>评论数</h3>
          <p class="number">{{ stats.comments }}</p>
          <p class="trend down">
            <i class="fas fa-arrow-down"></i>
            较上月下降 {{ stats.commentsGrowth }}%
          </p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon users">
          <i class="fas fa-users"></i>
        </div>
        <div class="stat-info">
          <h3>用户数</h3>
          <p class="number">{{ stats.users }}</p>
          <p class="trend up">
            <i class="fas fa-arrow-up"></i>
            较上月增长 {{ stats.usersGrowth }}%
          </p>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="chart-card">
      <div class="chart-header">
        <div class="tab-group">
          <div class="tab-item" :class="{ active: activeTab === 'visits' }" @click="switchTab('visits')">
            流量趋势
          </div>
          <div class="tab-item" :class="{ active: activeTab === 'trend' }" @click="switchTab('trend')">
            访问量
          </div>
        </div>
      </div>
      <div class="chart-content">
        <div v-show="activeTab === 'trend'" class="chart-container" ref="monthlyChartRef"></div>
        <div v-show="activeTab === 'visits'" class="chart-container" ref="dailyChartRef"></div>
      </div>
    </div>

    <!-- 饼图区域 -->
    <div class="charts-container">
      <div class="chart-box">
        <div class="chart-box-title">访问来源</div>
        <div class="chart-box-content" ref="sourceChartRef"></div>
      </div>
      <div class="chart-box">
        <div class="chart-box-title">文章类型热度</div>
        <div class="chart-box-content" ref="categoryChartRef"></div>
      </div>
    </div>

    <!-- 最近文章列表 -->
    <div class="recent-posts">
      <h2>最近发布</h2>
      <div class="post-list">
        <div v-for="post in recentPosts" :key="post.id" class="post-item">
          <div class="post-title">{{ post.title }}</div>
          <div class="post-meta">
            <span><i class="fas fa-calendar"></i> {{ post.date }}</span>
            <span><i class="fas fa-eye"></i> {{ post.views }}</span>
            <span><i class="fas fa-comments"></i> {{ post.comments }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import * as echarts from 'echarts';
// 导入API - 暂时注释
// import { dashboardApi } from '@/api';
// import { ElMessage } from 'element-plus';

const monthlyChartRef = ref(null);
const dailyChartRef = ref(null);
const sourceChartRef = ref(null);
const categoryChartRef = ref(null);
let monthlyChart = null;
let dailyChart = null;
let sourceChart = null;
let categoryChart = null;

// API集成相关状态 - 暂时注释
/*
const loading = ref(false);
*/

// 模拟数据 - 保留作为备用
const stats = ref({
  articles: 156,
  articlesGrowth: 12.5,
  views: 25678,
  viewsGrowth: 8.3,
  comments: 521,
  commentsGrowth: 2.1,
  users: 1234,
  usersGrowth: 5.7
});

const recentPosts = ref([
  {
    id: 1,
    title: '如何优化你的博客性能',
    date: '2023-12-25',
    views: 328,
    comments: 12
  },
  {
    id: 2,
    title: '2024年值得学习的编程语言',
    date: '2023-12-24',
    views: 256,
    comments: 8
  },
  {
    id: 3,
    title: '前端开发最佳实践指南',
    date: '2023-12-23',
    views: 198,
    comments: 5
  }
]);

// API方法 - 暂时注释
/*
const fetchDashboardData = async () => {
  loading.value = true;
  try {
    const response = await dashboardApi.getStats();
    stats.value = response.data.stats;
    monthlyData.months = response.data.monthlyData.months;
    monthlyData.values = response.data.monthlyData.values;
    dailyData.hours = response.data.dailyData.hours;
    dailyData.values = response.data.dailyData.values;
    sourceData.data = response.data.sourceData;
    categoryData.data = response.data.categoryData;
    recentPosts.value = response.data.recentPosts;
    
    // 重新初始化图表
    nextTick(() => {
      initCharts();
    });
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error);
    ElMessage.error('获取仪表盘数据失败');
  } finally {
    loading.value = false;
  }
};

const fetchRecentPosts = async () => {
  try {
    const response = await dashboardApi.getRecentPosts();
    recentPosts.value = response.data;
  } catch (error) {
    console.error('Failed to fetch recent posts:', error);
    ElMessage.error('获取最近文章失败');
  }
};
*/

// 月度数据
const monthlyData = {
  months: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
  values: [3000, 2000, 3200, 5000, 3200, 4200, 3200, 2100, 3000, 5200, 6000, 3000]
};

// 每日数据
const dailyData = {
  hours: ['6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
  values: [
    [100, 500, 2000, 20000, 35000, 55000, 65000, 35000, 15000, 35000, 65000, 45000, 20000, 5000, 2000, 1000, 500, 100],
    [50, 200, 1000, 5000, 8000, 18000, 22000, 8000, 5000, 12000, 22000, 18000, 8000, 2000, 1000, 500, 200, 50]
  ]
};

// 访问来源数据
const sourceData = {
  data: [
    { value: 40, name: '搜索引擎' },
    { value: 25, name: '直接访问' },
    { value: 20, name: '邮件营销' },
    { value: 15, name: '联盟广告' }
  ]
};

// 文章热度数据
const categoryData = {
  data: [
    { value: 35, name: 'Vue.js' },
    { value: 30, name: 'java' },
    { value: 20, name: 'Python' },
    { value: 15, name: 'Node.js' }
  ]
};

// 添加选项卡状态
const activeTab = ref('visits');

// 切换选项卡的函数
const switchTab = (tab) => {
  activeTab.value = tab;
  // 在下一个 tick 重新初始化图表
  nextTick(() => {
    if (tab === 'trend') {
      initMonthlyChart();
    } else {
      initDailyChart();
    }
  });
};

// 图表resize处理函数
const handleResize = () => {
  monthlyChart?.resize();
  dailyChart?.resize();
  sourceChart?.resize();
  categoryChart?.resize();
};

// 初始化月度图表
const initMonthlyChart = () => {
  if (monthlyChartRef.value) {
    if (monthlyChart) {
      monthlyChart.dispose();
    }
    monthlyChart = echarts.init(monthlyChartRef.value);
    const isDark = document.body.classList.contains('dark-mode');
    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        textStyle: {
          color: isDark ? '#fff' : '#333'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: monthlyData.months,
        axisLine: {
          lineStyle: {
            color: isDark ? '#666' : '#333'
          }
        },
        axisLabel: {
          color: isDark ? '#999' : '#666'
        }
      },
      yAxis: {
        type: 'value',
        axisLine: {
          lineStyle: {
            color: isDark ? '#666' : '#333'
          }
        },
        axisLabel: {
          color: isDark ? '#999' : '#666'
        },
        splitLine: {
          lineStyle: {
            color: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'
          }
        }
      },
      series: [{
        data: monthlyData.values,
        type: 'bar',
        itemStyle: {
          color: isDark ? '#177ddc' : '#1890ff'
        },
        barWidth: '60%'
      }]
    };
    monthlyChart.setOption(option);
  }
};

// 初始化每日图表
const initDailyChart = () => {
  if (dailyChartRef.value) {
    if (dailyChart) {
      dailyChart.dispose();
    }
    dailyChart = echarts.init(dailyChartRef.value);
    const isDark = document.body.classList.contains('dark-mode');
    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        },
        textStyle: {
          color: isDark ? '#fff' : '#333'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: dailyData.hours,
        axisLine: {
          lineStyle: {
            color: isDark ? '#666' : '#333'
          }
        },
        axisLabel: {
          color: isDark ? '#999' : '#666'
        }
      },
      yAxis: {
        type: 'value',
        axisLine: {
          lineStyle: {
            color: isDark ? '#666' : '#333'
          }
        },
        axisLabel: {
          color: isDark ? '#999' : '#666'
        },
        splitLine: {
          lineStyle: {
            color: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'
          }
        }
      },
      series: [
        {
          name: '总访问量',
          type: 'line',
          data: dailyData.values[0],
          smooth: true,
          areaStyle: {
            opacity: 0.3,
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: isDark ? '#177ddc' : '#1890ff' },
              { offset: 1, color: isDark ? 'rgba(23,125,220,0.1)' : 'rgba(24,144,255,0.1)' }
            ])
          },
          itemStyle: {
            color: isDark ? '#177ddc' : '#1890ff'
          }
        },
        {
          name: '独立访客',
          type: 'line',
          data: dailyData.values[1],
          smooth: true,
          areaStyle: {
            opacity: 0.3,
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: isDark ? '#49aa19' : '#52c41a' },
              { offset: 1, color: isDark ? 'rgba(73,170,25,0.1)' : 'rgba(82,196,26,0.1)' }
            ])
          },
          itemStyle: {
            color: isDark ? '#49aa19' : '#52c41a'
          }
        }
      ]
    };
    dailyChart.setOption(option);
  }
};

// 初始化访问来源图表
const initSourceChart = () => {
  if (sourceChartRef.value) {
    if (sourceChart) {
      sourceChart.dispose();
    }
    sourceChart = echarts.init(sourceChartRef.value);
    const isDark = document.body.classList.contains('dark-mode');
    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)',
      },
      legend: {
        orient: 'horizontal',
        bottom: 'bottom',
        textStyle: {
          color: isDark ? '#fff' : '#333'
        }
      },
      series: [
        {
          name: '访问来源',
          type: 'pie',
          radius: ['45%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center',
            color: isDark ? '#fff' : '#333'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 16,
              fontWeight: 'bold',
              color: isDark ? '#fff' : '#333',
            }
          },
          labelLine: {
            show: false
          },
          data: sourceData.data
        }
      ]
    };
    sourceChart.setOption(option);
  }
};

// 初始化文章热度图表
const initCategoryChart = () => {
  if (categoryChartRef.value) {
    if (categoryChart) {
      categoryChart.dispose();
    }
    categoryChart = echarts.init(categoryChartRef.value);
    const isDark = document.body.classList.contains('dark-mode');
    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)',
      },
      legend: {
        orient: 'horizontal',
        bottom: 'bottom',
        textStyle: {
          color: isDark ? '#fff' : '#333'
        }
      },
      series: [
        {
          name: '文章热度',
          type: 'pie',
          radius: '50%',
          data: categoryData.data,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          label: {
            show: true,
            position: 'outside',
            color: isDark ? '#fff' : '#333',
            formatter: '{b}: {d}%'
          },
          labelLine: {
            show: true,
            lineStyle: {
              color: isDark ? '#fff' : '#333'
            }
          }
        }
      ]
    };
    categoryChart.setOption(option);
  }
};

// 导出初始化图表方法供父组件调用
const initCharts = () => {
  // 使用 setTimeout 确保在主题切换后再初始化图表
  setTimeout(() => {
    // 确保完全销毁现有图表实例
    if (monthlyChart) {
      monthlyChart.dispose();
      monthlyChart = null;
    }
    if (dailyChart) {
      dailyChart.dispose();
      dailyChart = null;
    }
    if (sourceChart) {
      sourceChart.dispose();
      sourceChart = null;
    }
    if (categoryChart) {
      categoryChart.dispose();
      categoryChart = null;
    }

    // 重新初始化所有图表
    nextTick(() => {
      if (activeTab.value === 'trend') {
        initMonthlyChart();
      } else {
        initDailyChart();
      }
      initSourceChart();
      initCategoryChart();
    });
  }, 0);
};

// 监听主题变化
const watchTheme = () => {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.attributeName === 'class') {
        initCharts();
      }
    });
  });

  observer.observe(document.body, {
    attributes: true,
    attributeFilter: ['class']
  });

  return observer;
};

let themeObserver = null;

defineExpose({
  initCharts
});

onMounted(() => {
  // API调用 - 暂时注释
  /*
  fetchDashboardData();
  const refreshInterval = setInterval(fetchDashboardData, 300000); // 每5分钟刷新一次
  */
  
  initCharts();
  window.addEventListener('resize', handleResize);
  // 启动主题监听
  themeObserver = watchTheme();
  
  // 清理定时器 - 暂时注释
  /*
  return () => {
    clearInterval(refreshInterval);
  };
  */
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  // 清理主题监听
  if (themeObserver) {
    themeObserver.disconnect();
  }
  // 清理图表实例
  monthlyChart?.dispose();
  dailyChart?.dispose();
  sourceChart?.dispose();
  categoryChart?.dispose();
});
</script>

<style scoped>
.overview {
  padding: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  /* box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); */
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(220, 212, 212, 0.578);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
}

.stat-icon i {
  font-size: 24px;
  color: white;
}

.stat-icon.articles {
  background: linear-gradient(135deg, #1976d2, #64b5f6);
}

.stat-icon.views {
  background: linear-gradient(135deg, #388e3c, #81c784);
}

.stat-icon.comments {
  background: linear-gradient(135deg, #e64a19, #ff7043);
}

.stat-icon.users {
  background: linear-gradient(135deg, #7b1fa2, #ba68c8);
}

.stat-info h3 {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-color);
  opacity: 0.8;
}

.stat-info .number {
  margin: 8px 0;
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--text-color);
}

.trend {
  font-size: 0.8rem;
  margin: 0;
}

.trend.up {
  color: #4caf50;
}

.trend.down {
  color: #f44336;
}

.trend i {
  margin-right: 4px;
}

.charts-section {
  margin-bottom: 30px;
}

.chart-card {
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
}

.card{
  display: flex;
  width: 45%;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
}

.chart-header {
  margin-bottom: 20px;
  border-bottom: 1px solid var(--border-color);
  box-shadow: 0px 1px rgba(0, 0, 0, 0.1);
}

.tab-group {
  display: flex;
  gap: 20px;
}

.tab-item {
  padding: 12px 0;
  cursor: pointer;
  font-size: 1.1rem;
  color: var(--text-color);
  position: relative;
  transition: all 0.3s ease;
}

.tab-item::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #1976d2;
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.tab-item:hover {
  color: var(--sidebar-active);
}

.tab-item.active {
  color: var(--sidebar-active);
}

.tab-item.active::after {
  transform: scaleX(1);
}

.chart-content {
  position: relative;
  min-height: 400px;
}

.chart-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 400px;
  transition: opacity 0.3s ease;
}

.recent-posts {
  border-radius: 12px;
  padding: 20px;
}

.recent-posts h2 {
  margin: 0 0 20px 0;
  color: var(--text-color);
  font-size: 1.2rem;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.post-item {
  padding: 15px;
  border-radius: 8px;
  background: var(--bg-color);
  transition: all 0.3s ease;
}

.post-item:hover {
  transform: translateX(5px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.post-title {
  font-size: 1rem;
  color: var(--text-color);
  margin-bottom: 8px;
}

.post-meta {
  display: flex;
  gap: 15px;
  font-size: 0.8rem;
  color: var(--text-color);
  opacity: 0.7;
}

.post-meta span {
  display: flex;
  align-items: center;
}

.post-meta i {
  margin-right: 4px;
}

/* 饼图样式 */
.charts-container {
  display: flex;
  justify-content: space-between;
  gap: 30px;
  margin-bottom: 30px;
}

.chart-box {
  flex: 1;
  background-color: var(--background-lighter);
  border-radius: 12px;
  padding: 20px;
  box-shadow: var(--box-shadow);
  min-height: 300px;
}

.chart-box:hover {
  box-shadow: var(--box-shadow-hover);
  transform: translateY(-5px);
  transition: all 0.3s ease;
}

.chart-box-title {
  font-size: 16px;
  color: var(--text-primary);
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-color);
  font-weight: 500;
}

.chart-box-content {
  height: 250px;
  width: 100%;
}
</style> 