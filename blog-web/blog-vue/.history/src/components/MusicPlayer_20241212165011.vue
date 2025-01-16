<template>
  <div class="sidebar" :class="{ open: isOpen }">
    <button class="toggle-sidebar" @click="toggleSidebar">
      <img class="music-icon" src="../assets/imgs/音乐图标.jpg">
    </button>
    <div class="player">
      <img id="albumCover" class="album-cover" :src="currentSong.cover" :class="{'paused': !isPlaying}">
      <div class="song-info">
        <span id="songTitle">{{ currentSong.title || currentSong['歌名'] }}</span>
        <span id="currentTime">{{ currentTime }}</span>
      </div>
      <div class="controls">
        <button @click="prevSong">&#9664;&#9664;</button>
        <button @click="togglePlay" id="playButton" class="control-button">{{ isPlaying ? '❚❚' : '▶' }}</button>
        <button @click="nextSong">&#9654;&#9654;</button>
        <button @click="toggleMusicList" class="toggle-music-list">&#9776;</button>
      </div>
    </div>
    <div class="music-list-container" :class="{ 'open': isMusicListOpen }">
      <div class="search-container">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="搜索歌曲或歌手名" 
          @keyup.enter="searchSongs" 
        />
        <button class="search-button" @click="searchSongs">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </button>
      </div>
      <div class="music-list-scroll">
        <ul id="musicList" :class="{ 'open': isMusicListOpen }">
          <li 
            v-for="(song, index) in playlist" 
            :key="index" 
            @click="playSong(index)" 
            class="music-item"
            :class="{ 'active': index === currentSongIndex }"
          >
            <div class="song-info-list">
              <div class="song-title">{{ song.title || song['歌名'] }}</div>
              <div class="song-singer">{{ song.singer || song['歌手'] }}</div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useMusicStore } from '../store/music';
import { onMounted, onUnmounted, ref, computed } from 'vue';
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000';
const musicStore = useMusicStore();

const currentSong = computed(() => musicStore.currentSong);
const isPlaying = computed(() => musicStore.isPlaying);
const currentTime = computed(() => musicStore.currentTime);
const playlist = computed(() => musicStore.playlist);
const currentSongIndex = computed(() => musicStore.currentSongIndex);
const searchQuery = ref('');

const isOpen = ref(false);
const toggleSidebar = () => {
  isOpen.value = !isOpen.value;
};

const isMusicListOpen = ref(false);
const toggleMusicList = () => {
  isMusicListOpen.value = !isMusicListOpen.value;
};

const searchSongs = async () => {
  if (searchQuery.value.trim() === '') {
    musicStore.clearPlaylist();
    return;
  }
  try {
    const response = await axios.post('/api/search_music/', { query: searchQuery.value });
    musicStore.setPlaylist(response.data);
  } catch (error) {
    console.error("搜索音乐时出错:", error);
  }
};

onMounted(() => {
  musicStore.initAudioPlayer();
});

onUnmounted(() => {
  musicStore.cleanup();
});

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
  top: 34%;
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
  animation-play-state: running;   /* 默认运行动画 */
}

.album-cover.paused {
  animation-play-state: paused;     /* 停止播放暂停动画 */
}

@keyframes rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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


.music-list-container {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  opacity: 0;
  transform: translateY(-20px);
  transition: 
    max-height 0.4s ease,
    opacity 0.4s ease,
    transform 1s ease;
}

.music-list-container.open {
  max-height: 350px;
  opacity: 1;
  transform: translateY(0px);
}

.music-list-scroll {
  max-height: 250px;
  overflow-y: auto;
  margin-top: 10px;
  padding-right: 5px;
}

/* 自定义滚动条样式 */
.music-list-scroll::-webkit-scrollbar {
  width: 6px;
}

.music-list-scroll::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.music-list-scroll::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.music-list-scroll::-webkit-scrollbar-thumb:hover {
  background: #555;
}

#musicList {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.music-item {
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s ease;
  margin-bottom: 4px;
}

.music-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.music-item.active {
  background-color: rgba(0, 0, 0, 0.1);
}

.song-info-list {
  display: flex;
  flex-direction: column;
}

.song-title {
  font-size: 14px;
  color: #333;
  margin-bottom: 2px;
}

.song-singer {
  font-size: 12px;
  color: #666;
}

.search-container {
  display: flex;
  align-items: center;
  margin: 10px 0;
  padding: 0 5px;
  border: 1px solid #ddd;
  border-radius: 20px;
  background-color: #fff;
}

.search-container input {
  flex-grow: 1;
  border: none;
  padding: 8px 12px;
  outline: none;
  border-radius: 15px;
  background-color: rgb(157, 160, 152);
}

.search-button { 
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.search-button svg {
  width: 20px;
  height: 20px;
  color: #666;
  transition: color 0.3s ease;
}

.search-button:hover svg {
  color: #333;
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
  background-color: rgba(0, 0, 0, 0.1);
}
</style> 