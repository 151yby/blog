<template>
  <div id="leave-message">
    <form action="" class="message-box">
      <input type="text" class="message-box-style" placeholder="昵称">
      <input type="text" class="message-box-style" placeholder="邮箱">
      <textarea class="message-box-style" placeholder="输入您的留言"></textarea>
      <button type="submit" class="submit-btn">提交留言</button>
      <div class="pain-container">
        <img src="../assets/imgs/佩恩.gif" alt="佩恩">
      </div>
    </form>
  </div>
</template>

<script setup>
</script>

<style scoped>
#leave-message {
  position: relative;
  margin: auto;
  top: 100px;
  width: 1330px;
  height: 520px;
  background: url('../assets/imgs/雪山2.webp') center center/cover no-repeat;
  padding: 40px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  border-radius: 15px;
  overflow: hidden;
}

.message-box {
  width: 1100px;
  height: 500px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(5px);
  padding: 20px 40px;
  border-radius: 20px;
  position: relative;
  margin: auto;
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: grid;
  grid-template-rows: auto auto 1fr;
  gap: 15px;
  align-items: start;
}

.message-box-style {
  width: 60%;
  height: 50px;
  border: none;
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  padding: 10px 20px;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-size: 16px;
  color: white;
  justify-self: center;
  margin: 10px 15px;
}

.message-box > textarea {
  height: 200px;
}

.message-box > input::placeholder,
.message-box > textarea::placeholder {
  color: rgba(255, 255, 255, 1);
}

/* 输入框焦点效果 */
.message-box > input:focus {
    border-bottom: 2px solid rgba(255, 255, 255, 0.8);
    outline: none;
    background: rgba(255, 255, 255, 0.2);
    box-shadow: 0 5px 15px rgba(255, 255, 255, 0.1);
}

.message-box > textarea:focus {
    border-bottom: 2px solid rgba(255, 255, 255, 0.8);
    outline: none;
    background: rgba(255, 255, 255, 0.2);
    box-shadow: 0 5px 15px rgba(255, 255, 255, 0.1);

.submit-btn {
  width: 120px;
  height: 45px;
  position: relative;
  justify-self: center;
  margin: auto;
  background: transparent;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 15px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.8);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 255, 255, 0.2);
}

.submit-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(255, 255, 255, 0.2);
}

.pain-container {
  position: absolute;
  bottom: 30px;
  right: 30px;
  width: 180px;
  height: 180px;
  opacity: 0.9;
  transition: all 0.3s ease;
  filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.3));
}

.pain-container:hover {
  opacity: 1; 
  transform: scale(1);
  filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.5));
}

.pain-container img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  margin-left: 5px;
  margin-top: 15px;
}
</style> 