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