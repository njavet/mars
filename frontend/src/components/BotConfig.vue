<template>
  <div class="bot-config">
    <h3>Settings</h3>

    <div class="model-controls">
      <label>Language Model</label>
      <select class="select" v-model="selectedLM">
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
          :key="index"
          :value="system_message.text"
          :title="system_message.text"
        >
          {{ system_message.name }}
        </option>
      </select>

    </div>

    <label>Tool use</label>
    <label class="rag-checkbox">
      <input type="checkbox" v-model="ragEnabled" />
      Enable RAG
    </label>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const selectedServer = defineModel('selectedServer')
const selectedLM = defineModel('selectedLM')
const ragEnabled = defineModel('ragEnabled')
const selectedSystemMessage = defineModel('selectedSystemMessage')

const models = ref([])
const systemMessages = ref([])

onMounted(async () => {
  const res0 = await fetch(`/api/lms?base_url=${selectedServer.value}`)
  models.value = await res0.json()
  if (models.value.length > 0 && !selectedLM.value) {
    selectedLM.value = models.value[0]
  }

  const res1 = await fetch('/api/system-messages')
  systemMessages.value = await res1.json()
  if (systemMessages.value.length > 0 && !selectedSystemMessage.value) {
    selectedSystemMessage.value = systemMessages.value[0].text
  }
})
</script>

<style scoped>
.bot-config {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  border-top: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
  gap: 0.75rem;
}

.select {
  width: 100%;
}

.model-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.rag-checkbox {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

</style>
