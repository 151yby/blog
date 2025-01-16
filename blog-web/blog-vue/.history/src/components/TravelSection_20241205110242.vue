<template>
  <div id="travel">
    <div class="travel-wrap">
      <div class="travel-tit">
        <h2>旅行日记</h2>
        <p>Travel is the only way to live your life</p>
        <button>查看更多&gt;</button>
      </div>
      <ul class="photo-list"></ul> <!-- 照片列表 -->
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';

const photoData = [
  { id: 1, title: "旅行记忆 #1" },
  { id: 2, title: "旅行记忆 #2" },
  { id: 3, title: "旅行记忆 #3" },
  { id: 4, title: "旅行记忆 #4" },
  { id: 5, title: "旅行记忆 #5" },
  { id: 6, title: "旅行记忆 #6" },
  { id: 7, title: "旅行记忆 #7" },
  { id: 8, title: "旅行记忆 #8" }
];

const loadTravelPhotos = () => {
  const photoList = document.querySelector('.photo-list');
  photoData.forEach((item) => {
    const li = document.createElement('li');
    const img = document.createElement('img');
    img.src = new URL(`../assets/imgs/${item.id}.jpg`, import.meta.url).href;
    li.setAttribute('data-title', item.title);

    li.appendChild(img);
    photoList.appendChild(li);
  });
};

onMounted(() => {
  loadTravelPhotos();
});
</script>

<style scoped>
#travel {
  width: 100%;
  height: auto;
  padding: 20px;
}

.travel-wrap {
  width: 80%;
  margin: auto;
}

.travel-tit {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.travel-tit h2 {
  font-size: 24px;
  font-weight: bold;
}

.photo-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.photo-list li {
  margin: 10px;
  width: 200px;
  height: 150px;
  overflow: hidden;
  border-radius: 10px;
  transition: transform 0.3s;
}

.photo-list li:hover {
  transform: scale(1.1);
}

.photo-list img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style> 