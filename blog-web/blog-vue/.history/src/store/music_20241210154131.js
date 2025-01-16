// store/music.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

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

    async playSong(index) {
      try {
        this.initAudioPlayer(); // 确保 audioPlayer 已初始化
        this.currentSongIndex = index;
        this.audioPlayer.src = this.playlist[index].src;
        await this.audioPlayer.load(); // 等待加载完成

        // 使用 Promise 处理播放
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
          this.a
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