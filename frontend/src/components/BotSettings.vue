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
import {onMounted, watch} from 'vue'
import { useAppState, useBotState } from '../composables/useState.js'
import { fetchModels } from '../js/utils.js'

const {
  libs,
  servers,
  models,
  systemMessages,
} = useAppState()

const {
  selectedLib,
  selectedServer,
  selectedModel,
  selectedSystemMessage,
  agentic
} = useBotState()

onMounted(async () => {
  if (!selectedServer.value && servers.value.length > 1) {
    selectedServer.value = servers.value[0]
  }
  if (libs.value.length > 0 && !selectedLib.value) {
    selectedLib.value = libs.value[0]
  }
  if (models.value.length > 0 && !selectedModel.value) {
    selectedModel.value = models.value[0]
  }
  if (systemMessages.value.length > 0 && !selectedSystemMessage.value) {
    selectedSystemMessage.value = systemMessages.value[0].text
  }
})

watch(selectedServer, async(server) => {
  models.value = await fetchModels(server)
  if (models.value.length > 0 && !selectedModel.value) {
    selectedModel.value = models.value[0]
  }
}, {immediate: true})
</script>

<style scoped>
.bot-settings-container {
  display: flex;
  flex-direction: column;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  gap: 1rem;
  border-bottom: 1px solid gray;
}

.select {
  width: 100%;
}
</style>
