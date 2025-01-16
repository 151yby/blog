<template>
  <div class="sidebar" :class="{ open: isOpen }">
    <button class="toggle-sidebar" @click="toggleSidebar">
      <img class="music-icon" src="../assets/imgs/音乐图标.jpg">
    </button>
    <div class="player">
      <img id="albumCover" class="album-cover" :src="currentSong.cover" :class="{'pause': !isPlaying}">
      <div class="song-info">
        <span id="songTitle">{{ currentSong.title }}</span>
        <span id="currentTime">{{ currentTime }}</span>
      </div>
      <div class="controls">
        <button @click="prevSong">&#9664;&#9664;</button>
        <button @click="togglePlay" id="playButton" class="control-button">{{ isPlaying ? '❚❚' : '▶' }}</button>
        <button @click="nextSong">&#9654;&#9654;</button>
        <button @click="toggleMusicList" class="toggle-music-list">&#9776;</button>
      </div>
    </div>
    <ul id="musicList" :class="{ 'open': isMusicListOpen }">
      <li v-for="(song, index) in playlist" :key="index" @click="playSong(index)">{{ song.title }}</li>
    </ul>
  </div>
</template>

<script setup>
  import { useMusicStore } from '../store/music';
  import { onMounted, onUnmounted, ref, computed } from 'vue';

  const musicStore = useMusicStore();

  // 使用计算属性从 store 中获取数据
  const currentSong = computed(() => musicStore.currentSong);
  const isPlaying = computed(() => musicStore.isPlaying);
  const currentTime = computed(() => musicStore.currentTime);
  const playlist = computed(() => musicStore.playlist);

  // 控制侧边栏的展开/收起
  const isOpen = ref(false);
  const toggleSidebar = () => {
    isOpen.value = !isOpen.value;
  };

  // 控制歌曲列表的展开/收起
  const isMusicListOpen = ref(false);
  const toggleMusicList = () => {
    isMusicListOpen.value = !isMusicListOpen.value;
  };

  // 组件挂载时初始化
  onMounted(() => {
    musicStore.initAudioPlayer();
  });

  // 组件卸载时清理
  onUnmounted(() => {
    musicStore.cleanup();
  });

  // 绑定 store 的方法
  const playSong = (index) => {
    musicStore.playSong(index);
  };

  const togglePlay = () => {
    musicStore.togglePlay();
  };

  const nextSong = () => {
    musicStore.nextSong();
  };

  const prevSong = () => {
    musicStore.prevSong();
  };
</script>

<style scoped>
.sidebar {
  z-index: 1000;
  position: fixed;
  right: -248px;
  top: 31%;
  transform: translateY(-50%);
  width: 240px;
  padding: 2px 20px;
  background-color: rgba(255, 255, 255, 0.903);
  box-shadow: -2px 0 5px rgba(221, 221, 221, 0.7);
  border-radius: 10px;
  transition: right 0.3s ease; /* 添加过渡效果 */
}

.sidebar.open {
  right: 0; /* 将侧边栏移入视口 */
}

.toggle-sidebar {
  margin: none;
  padding: none;
  border: none;
  background: none;
  cursor: pointer;
}

.music-icon {
  position: relative;
  top: 28px;
  left: -20px;
  width: 27px;
  height: 26px;
  border-radius: 100%;
  background-color: rgba(252, 246, 246, 0.3);
}

.player {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.album-cover {
  position: relative;
  top: -20px;
  right: 62%;
  width: 60px;
  height: 60px;
  margin-bottom: -80px;
  margin-left: 170px;
  border-radius: 100%; 
  transition: transform 0.5s ease;
  animation: rotate 5s linear infinite;
  animation-play-state: paused;
  transform-origin: center; /* 确保旋转中心为图片中心 */
}

.album-cover.playing{
  animation-play-state: running;
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.song-info {
  position: relative;
  left: 50px;
  top: 0px;
  display: flex;
  justify-content: space-between;
  width: 63%;
  margin-bottom: 10px;
}

.controls {
  position: relative;
  right: -30px;
  display: flex;
  justify-content: space-between;
  width: 70%;
  margin-top: 0px;
  margin-left: 55px;
}

.controls button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 15px;
}

#musicList {
  list-style-type: none;
  padding: 0;
  margin-top: 0px;
  height: auto; 
  max-height: 0px;
  opacity: 0;
  transform: translateY(-20px); /* 初始位移 */
  transition: opacity 0.3s ease ,transform 1s ease; 
  transition: max-height 0.3s ease ,transform 1s ease; 
  overflow: hidden;
}

#musicList.open {
  max-height: 300px; /* 设置展开后的最大高度 */
  opacity: 1;
  transform: translateY(0px); /* 初始位移 */
}

#musicList li {
  cursor: pointer;
  padding: 5px;
}

#musicList li:hover {
  background-color: rgb(193, 191, 191); /* 鼠标悬停效果 */
}


.toggle-music-list {
  margin-top: 10px;
  background-color: #fff;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.toggle-music-list:hover {
  background-color: rgba(0, 0, 0, 0.4);
}
</style> 