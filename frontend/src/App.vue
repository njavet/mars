<template>
  <div class="app-container">
    <Sidebar
        :selectedView="selectedView"
        @view-selected="selectedView = $event"
        v-model:selectedLM="selectedLM"
        v-model:ragEnabled="ragEnabled"
        v-model:selectedPreprompt="selectedPreprompt"
    />
    <div class="main-content">
      <Home v-if="selectedView === 'home'"/>
      <Chatbot
          v-if="selectedView === 'chatbot'"
          :lm_name="selectedLM"
          :enable_rag="ragEnabled"
          :preprompt="selectedPreprompt"
      />
      <Assistant
          v-else-if="selectedView === 'assistant'"
          :lm_name="selectedLM"
          :enable_rag="ragEnabled"
          :preprompt="selectedPreprompt"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Sidebar from './components/Sidebar.vue'
import Home from './components/Home.vue'
import Chatbot from './components/Chatbot.vue'
import Assistant from "./components/Assistant.vue";

// state
const selectedView = ref('')
const selectedLM = ref('')
const ragEnabled = ref(false)
const selectedPreprompt = ref('')

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