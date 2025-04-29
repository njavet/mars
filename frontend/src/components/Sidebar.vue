<template>
  <div class="sidebar">
    <h3>Ollama Server</h3>
    <select v-model="selectedServer">
      <option value="http://localhost:11434">Localhost</option>
    </select>
    <h3>Navigation</h3>
    <label v-for="option in options" :key="option.value" class="nav-option">
      <input
        type="radio"
        name="nav"
        :value="option.value"
        v-model="selectedView"
        @change="onSelectView"
      />
        {{ option.label }}
    </label>
    <div v-if="selectedView === 'chatbot' || selectedView === 'assistant'">
      <BotConfig
          v-model:selectedServer="selectedServer"
          v-model:selectedLM="selectedLM"
          v-model:selectedSystemMessage="selectedSystemMessage"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import BotConfig from "./BotConfig.vue";
const emit = defineEmits(['view-selected'])

const selectedView = ref('home')
const selectedServer = defineModel('selectedServer')
const selectedLM = defineModel('selectedLM')
const selectedSystemMessage = defineModel('selectedSystemMessage')
const options = [
  { value: 'home', label: 'Home'},
  { value: 'about', label: 'About'},
  { value: 'chatbot', label: 'Chatbot'},
  { value: 'assistant', label: 'Assistant'}
]

function onSelectView(event) {
  emit('view-selected', selectedView.value)
}
</script>

<style scoped>
.sidebar {
  width: 220px;
  flex-shrink: 0;
  background-color: #1f1f1f;
  color: white;
  padding: 1rem;
  box-sizing: border-box;
  border-right: 1px solid #444;
  text-align: left;
}

.sidebar select {
  width: 100%;
  padding: 0.5rem;
  margin-top: 1rem;
  background: #222;
  color: white;
  border: 2px solid gray;
  border-radius: 4px;
}

.nav-option {
  display: block;
  margin-bottom: 0.5rem;
  color: white;
}

input[type="radio"] {
  margin-right: 0.5rem;
}
</style>
