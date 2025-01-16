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
#travel{
    width: 100%;
    height: 700px;
}

/* 旅行内容包装器 */
.travel-wrap{
    position: relative;
    top: 20px;
    width: 80%;
    height: 640px;
    margin: auto;
}

/* 旅行标题区域 */
.travel-tit{
    position: relative;
    width: 100%;
    height: 80px;
    right: 50px;
    top: 60px;
}

/* 旅行主标题 */
.travel-tit>h2{
    width: 200px;
    height: 40px;
    float: left;
    border-bottom: black solid 1px;
    text-align: center;
    margin-left: 63px;
}

/* 旅行副标题 */
.travel-tit>p{
    position: absolute;
    width: 300px;
    height: 30px;
    float: left;
    font-family: 'Times New Roman', Times, serif;
    top: 50px;
    margin-left: 47px;
}

/* 查看更多按钮 */
.travel-tit>button{
    width: 100px;
    height: 35px;
    float: right;
    margin-top: 20px;
    background-color: #fff;
}

/*  照片墙样式 */
.photo-list{
    position: relative;
    width: 1400px;
    height: 520px;
    overflow: hidden;
    margin-top: 10px;
    right: 130px;
    top: 50px;
}

/* 照片项样式 */
.photo-list>li{
    position: relative;
    float: left;
    width: 310px;
    height: 240px;
    margin: 7px 12px;
    left: 35px;
    border-radius: 10px;
    overflow: hidden;
    transition: all 0.4s ease;
    cursor: pointer;
}

/* 照片悬停效果 */
.photo-list>li:hover{
    transform: translateY(-10px);
    box-shadow: 0 15px 25px rgba(0,0,0,0.2);
}

/* 照片图片样式 */
.photo-list>li>img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s ease;
    filter: brightness(0.9);
}

/* 照片悬停时的图片效果 */
.photo-list>li:hover img {
    transform: scale(1.1);
    filter: brightness(1.1);
}

/* 照片标题遮罩层 */
.photo-list>li::after {
    content: attr(data-title);
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    padding: 20px;
    background: linear-gradient(transparent, rgba(0,0,0,0.7));
    color: white;
    font-size: 16px;
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.3s ease;
}

/* 照片标题悬停效果 */
.photo-list>li:hover::after {
    opacity: 1;
    transform: translateY(0);
}

/* 照片加载动画 */
@keyframes photoFadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style> 