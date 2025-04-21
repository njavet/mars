<template>
  <div class="app-container">
    <Chat />
  </div>
</template>

<script setup>
import Chat from './components/Chat.vue'
</script>

<style scoped>
.app-container {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>