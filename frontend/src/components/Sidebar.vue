<template>
  <div class="sidebar">
    <h3>Ollama Server</h3>
    <select v-model="selectedServer">
      <option disabled value="">Select a Server</option>
      <option value="http://localhost">localhost</option>
      <option value="http://sandiego.zhaw.ch">sandiego</option>
      <option value="http://sanfrancisco.zhaw.ch">sanfrancisco</option>
      <option value="http://losangeles.zhaw.ch">losangeles</option>
      <option value="http://sacramento.zhaw.ch">sacramento</option>
      <option value="http://sanjose.zhaw.ch">sanjose</option>
      <option value="http://fresko.zhaw.ch">fresko</option>
      <option value="http://trinity.zhaw.ch">trinity</option>
      <option value="http://elpaso.zhaw.ch">elpaso</option>
      <option value="http://lubbock.zhaw.ch">lubbock</option>
      <option value="http://honolulu.zhaw.ch">honolulu</option>
      <option value="http://hilo.zhaw.ch">hilo</option>
    </select>
    <h3>Ollama Server Port</h3>
    <select v-model="selectedPort">
      <option disabled value="">Select a Port</option>
      <option :value="11434">11434</option>
      <option :value="8800">8800</option>
      <option :value="8801">8801</option>
      <option :value="8802">8802</option>
      <option :value="8803">8803</option>
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
          v-model:selectedPort="selectedPort"
          v-model:selectedLM="selectedLM"
          v-model:selectedSystemMessage="selectedSystemMessage"
      />
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue";
import BotConfig from "./BotConfig.vue";
const emit = defineEmits(['view-selected'])

const selectedView = ref('home')
const selectedServer = defineModel('selectedServer')
const selectedPort = defineModel('selectedPort')
const selectedLM = defineModel('selectedLM')
const selectedSystemMessage = defineModel('selectedSystemMessage')
const options = [
  { value: 'home', label: 'Home'},
  { value: 'about', label: 'About'},
  { value: 'chatbot', label: 'Chatbot'},
  { value: 'assistant', label: 'Assistant'},
  { value: 'evaluation', label: 'Evaluation'}
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
