<template>
  <div class="app-container">
    <Sidebar
        @model-selected="selectedModel = $event"
        @server-selected="selectedServer = $event"
    />
    <div class="main-content" v-if="selectedModel">
      <Chat :lm_name="selectedModel" :base_url="selectedServer" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Sidebar from './components/Sidebar.vue'
import Chat from './components/Chat.vue'
const selectedModel = ref("")
const selectedServer = ref("http://localhost:11434")

</script>

<style scoped>
.app-container {
  display: flex;
  flex: 1;
  overflow: hidden;
  width: 100%;
  height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>