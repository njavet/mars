<template>
  <div class="app-container">
    <Sidebar
        :selectedView="selectedView"
        :baseUrl="selectedServer"
        @view-selected="selectedView = $event"
        v-model:selectedServer="selectedServer"
        v-model:selectedLM="selectedLM"
        v-model:ragEnabled="ragEnabled"
        v-model:selectedSystemMessage="selectedSystemMessage"
    />
    <div class="main-content">
      <Home v-if="selectedView === 'home'"/>
      <About v-if="selectedView === 'about'" />
      <Chatbot
          v-if="selectedView === 'chatbot'"
          :base_url="selectedServer"
          :lm_name="selectedLM"
          :enable_rag="ragEnabled"
          :system_message="selectedSystemMessage"
      />
      <Assistant
          v-else-if="selectedView === 'assistant'"
          :base_url="selectedServer"
          :lm_name="selectedLM"
          :enable_rag="ragEnabled"
          :system_message="selectedSystemMessage"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Sidebar from './components/Sidebar.vue'
import Home from './components/Home.vue'
import About from './components/About.vue'
import Chatbot from './components/Chatbot.vue'
import Assistant from "./components/Assistant.vue";

// state
const selectedView = ref('home')
const selectedServer = ref("http://localhost:11434")
const selectedLM = ref('')
const ragEnabled = ref(false)
const selectedSystemMessage = ref('')

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