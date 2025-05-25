<template>
  <div class="bot-settings-container">
    <h3>Settings</h3>

    <label>Library</label>
    <select class="select" v-model="selectedLib">
      <option disabled value="">Select a Library</option>
      <option
          v-for="lib in libs"
          :key="lib"
          :value="lib">
        {{ lib }}
      </option>
    </select>

    <label>Ollama Server</label>
    <select class="select" v-model="selectedServer">
      <option disabled value="">Select a Server</option>
      <option
          v-for="server in servers"
          :key="server"
          :value="server">
        {{ server }}
      </option>
    </select>

    <label>Language Model</label>
    <select class="select" v-model="selectedModel">
      <option disabled value="">Select a model</option>
      <option v-for="model in models" :key="model" :value="model">
        {{ model }}
      </option>
    </select>

    <label>System Message</label>
    <select class="select" v-model="selectedSystemMessage">
      <option disabled value="">Select a system message</option>
      <option
        v-for="(system_message, index) in systemMessages"
        :key="system_message.key"
        :value="system_message.text"
        :title="system_message.text"
      >
        {{ system_message.key }}
      </option>
    </select>

    <label>Bot Mode</label>
    <label class="select">
      <input
          type="checkbox"
          v-model="agentic"/>
      Agentic
    </label>
  </div>
</template>

<script setup>
import {ref, onMounted, watch} from 'vue'
import { useAppState } from '../composables/useAppState.js'
const {
  libs,
  selectedLib,
  servers,
  selectedServer,
  models,
  selectedModel,
  systemMessages,
  selectedSystemMessage,
  agentic
} = useAppState()


</script>

<style scoped>
.bot-settings-container {
  display: flex;
  flex-direction: column;
  padding-top: 0.5rem;
  gap: 1rem;
  border-bottom: 10px solid #ccc;
}

.select {
  width: 100%;
}
</style>
