<template>
  <div class="app-container">
    <Sidebar
        :selectedView="selectedView"
        @server-selected="selectedServer = $event"
        @view-selected="selectedView = $event"
        @model-selected="selectedModel = $event"
    />
    <div class="main-content">
      <Home v-if="selectedView === 'home'"/>
      <Chat v-if="selectedView === 'chat'" :lm_name="selectedModel" :base_url="selectedServer" />
      <Dashboard v-else-if="selectedView === 'evaluation'"/>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Sidebar from './components/Sidebar.vue'
import Home from './components/Home.vue'
import Chat from './components/Chat.vue'
import Dashboard from "./components/Dashboard.vue";
const selectedServer = ref("http://localhost:11434")
const selectedView = ref('home')
const selectedModel = ref("")

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