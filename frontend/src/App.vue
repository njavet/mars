<template>
  <div class="app-container">
    <Sidebar @model-selected="selectedModel = $event"/>
    <div class="main-content" v-if="selectedModel">
      <Chat :model="selectedModel" />
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue";
import Sidebar from './components/Sidebar.vue'
import Chat from './components/Chat.vue'
const selectedModel = ref("")

</script>

<style scoped>
.app-container {
  display: flex;
  flex: 1;
  overflow: hidden;
  width: 100%;
  height: 100%;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>