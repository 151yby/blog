// store/music.js
import { defineStore } from 'pinia';
import axios from 'axios';
import { ref, computed } from 'vue';
axios.defaults.baseURL = 'http://localhost:8000';

export const useMusicStore = defineStore('music', {
  state: () => ({
    currentSongIndex: 0,
    isPlaying: false,
    currentTime: '0:00',
    playlist: [
      { src: new URL('../assets/music/1n - デート2(1nCover).mp3', import.meta.url).href, title: '1n - デート2', cover: new URL('../assets/album-img/1n - デート2.jpg', import.meta.url).href },
      { src: new URL('../assets/music/ACK - 渐行渐远的风不再歌唱(Bright Mix)(Inst).mp3', import.meta.url).href, title: 'ACK', cover: new URL('../assets/album-img/ACK.jpg', import.meta.url).href },
      { src: new URL('../assets/music/AnselRabbit - Talking To The Moon.mp3', import.meta.url).href, title: 'AnselRabbit', cover: new URL('../assets/album-img/AnselRabbit.jpg', import.meta.url).href },
      { src: new URL('../assets/music/Biscuits - Rise.mp3', import.meta.url).href, title: 'Biscuits', cover: new URL('../assets/album-img/Biscuits - Rise.jpg', import.meta.url).href },
      { src: new URL('../assets/music/SWAGGER - Señorita.mp3', import.meta.url).href, title: 'SWAGGER', cover: new URL('../assets/album-img/SWAGGER.jpg', import.meta.url).href },
      { src: new URL('../assets/music/Yiiiko - Cornfield Chase in Golden hour.mp3', import.meta.url).href, title: 'Yiiiko', cover: new URL('../assets/album-img/Yiiiko.jpg', import.meta.url).href },
      { src: new URL('../assets/music/匿名的好友-en.mp3', import.meta.url).href, title: '匿名的好友', cover: new URL('../assets/album-img/匿名的好友.jpg', import.meta.url).href },
      { src: new URL('../assets/music/APT.-ROSÉ (로제).mp3', import.meta.url).href, title: 'APT.-ROSÉ', cover: new URL('../assets/album-img/APT..jpg', import.meta.url).href },
      { src: new URL('../assets/music/这样很好.mp3', import.meta.url).href, title: '这样很好', cover: new URL('../assets/album-img/这样很好.jpg', import.meta.url).href }
    ],
    audioPlayer: null // 初始化为 null
  }),

  getters: {
    currentSong() {
      return this.playlist[this.currentSongIndex];
    }
  },

  actions: {
    // 添加 setPlaylist 方法
    setPlaylist(newPlaylist) {
      // 转换数据结构以匹配播放器需要的格式
      this.playlist = newPlaylist.map(song => ({
        title: song['歌名'],
        singer: song['歌手'],
        music_id: song['music_id'],
        // 如果���有封面图，可以设置一个默认的
        cover: new URL('../assets/album-img/default-cover.jpg', import.meta.url).href
      }));
      this.currentSongIndex = 0;
    },

    // 添加 clearPlaylist 方法
    clearPlaylist() {
      this.playlist = [];
      this.currentSongIndex = 0;
    },

    initAudioPlayer() {
      if (!this.audioPlayer) {
        this.audioPlayer = new Audio();
        // 添加音频结束事件监听器
        this.audioPlayer.addEventListener('ended', this.nextSong);
        // 添加时间更新事件监听器
        this.audioPlayer.addEventListener('timeupdate', () => {
          this.updateCurrentTime();
        });
      }
    },
    
    // 获取搜索音乐 URL
    async fetchMusicUrl(musicId) {
      try {
        const response = await axios.post('api/download_music/', { music_id: musicId, ablum_cover: });
        const musicUrl = response.data.music_url;
        // 更新对应歌曲的 src
        const songIndex = this.playlist.findIndex(song => song.music_id === musicId);
        if (songIndex !== -1) {
          this.playlist[songIndex].src = musicUrl;
        }
        const albumsrc = this.playlist.findIndex(song => song.cover)

        return musicUrl;
      } catch (error) {
        console.error('获取音乐 URL 失败:', error);
        throw error;
      }
    },

    async playSong(index) {
      try {
        this.initAudioPlayer();
        this.currentSongIndex = index;
        const currentSong = this.playlist[index];

        // 如果是搜索的歌曲，需要先获取音乐 URL
        if (currentSong.music_id) {
          const response = await axios.post('/api/download_music/', {
            music_id: currentSong.music_id
          });
          currentSong.src = response.data.music_url;
        }

        this.audioPlayer.src = currentSong.src;
        await this.audioPlayer.load();

        const playPromise = this.audioPlayer.play();
        if (playPromise !== undefined) {
          await playPromise;
          this.isPlaying = true;
        }
      } catch (error) {
        console.error('Error playing audio:', error);
        this.isPlaying = false;
      }
    },

    async togglePlay() {
      try {
        this.initAudioPlayer();

        // 如果还没有设置音源，播放当前索引的歌曲
        if (!this.audioPlayer.src) {
          await this.playSong(this.currentSongIndex);
          return;
        }

        if (this.isPlaying) {
          this.audioPlayer.pause();
          this.isPlaying = false;
        } else {
          const playPromise = this.audioPlayer.play();
          if (playPromise !== undefined) {
            await playPromise;
            this.isPlaying = true;
          }
        }
      } catch (error) {
        console.error('Error toggling play:', error);
        this.isPlaying = false;
      }
    },

    async nextSong() {
      const nextIndex = (this.currentSongIndex + 1) % this.playlist.length;
      await this.playSong(nextIndex);
    },

    async prevSong() {
      const prevIndex = (this.currentSongIndex - 1 + this.playlist.length) % this.playlist.length;
      await this.playSong(prevIndex);
    },

    updateCurrentTime() {
      const currentTime = this.formatTime(this.audioPlayer?.currentTime || 0);
      this.currentTime = currentTime;
    },

    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
    },

    // 清理函数，在组件卸载时调用
    cleanup() {
      if (this.audioPlayer) {
        this.audioPlayer.removeEventListener('ended', this.nextSong);
        this.audioPlayer.pause();
        this.audioPlayer = null;
      }

    }
  }
});