import { defineStore } from 'pinia';

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
    audioPlayer: new Audio() // 创建音频对象
  }),
  actions: {
    playSong(index) {
      this.currentSongIndex = index;
      this.audioPlayer.src = this.playlist[index].src;
      this.audioPlayer.play();
      this.isPlaying = true;

      // 更新当前歌曲信息
      this.updateCurrentSongInfo();
      this.audioPlayer.onended = this.nextSong; // 播放结束后自动播放下一首
    },

    window.onload = function () {
      this.currentSongIndex = 0;
      this.audioPlayer.src = this.playlist[0].src;
      this.audioPlayer.play();
      this.isPlaying = true;
    },


    togglePlay() {
      if (this.isPlaying) {
        this.audioPlayer.pause();
      } else {
        this.audioPlayer.play();
      }
      this.isPlaying = !this.isPlaying;
      this.updateCurrentSongInfo();
    },
    nextSong() {
      this.currentSongIndex = (this.currentSongIndex + 1) % this.playlist.length;
      this.playSong(this.currentSongIndex);
    },
    prevSong() {
      this.currentSongIndex = (this.currentSongIndex - 1 + this.playlist.length) % this.playlist.length;
      this.playSong(this.currentSongIndex);
    },
    updateCurrentSongInfo() {
      // 更新当前歌曲标题和封面
      const currentSong = this.playlist[this.currentSongIndex];
      document.getElementById('songTitle').innerText = currentSong.title;
      document.getElementById('albumCover').src = currentSong.cover;
      document.getElementById('playButton').innerHTML = this.isPlaying ? '&#10074;&#10074;' : '&#9654;'; // 更新播放按钮图标
    },
    updateCurrentTime() {
      const currentTime = this.formatTime(this.audioPlayer.currentTime);
      this.currentTime = currentTime;
      document.getElementById('currentTime').innerText = currentTime; // 更新当前时间显示
    },
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
    }
  }
}); 

