<template>
  <div class="app-container">
    <Sidebar
        :selectedView="selectedView"
        @server-selected="selectedServer = $event"
        @view-selected="selectedView = $event"
    />
    <div class="main-content">
      <Home v-if="selectedView === 'home'"/>
      <Chatbot v-if="selectedView === 'chatbot'" :base_url="selectedServer" />
      <Assistant v-else-if="selectedView === 'assistant'"/>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Sidebar from './components/Sidebar.vue'
import Home from './components/Home.vue'
import Chatbot from './components/Chatbot.vue'
import Assistant from "./components/Assistant.vue";
const selectedServer = ref("http://localhost:11434")
const selectedView = ref('home')
</script>

<style scoped>
.app-container {
  flex: 1;
  display: flex;
  overflow: hidden;
}
.main-content {
   flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>