<template>
  <div class="app-container">
    <div class="sidebar">
      <h2>LLMs</h2>
      <ul>
        <li><a href="?model=openai">OpenAI</a></li>
        <li><a href="?model=llama">LLaMA</a></li>
        <!-- Add more models here -->
      </ul>
    </div>
    <div class="main-content">
      <Chat />

    </div>
  </div>
</template>

<script setup>
import Chat from './components/Chat.vue'
</script>

<style scoped>

.app-container {
  height: 100vh;
  width: 100vw;
  display: flex;
  overflow: hidden;
}

.sidebar {
  width: 220px;
  background-color: #1f1f1f;
  color: white;
  padding: 1rem;
  box-sizing: border-box;
  border-right: 1px solid #444;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin: 1rem 0;
}

.sidebar a {
  color: #ccc;
  text-decoration: none;
}

.sidebar a:hover {
  color: white;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>