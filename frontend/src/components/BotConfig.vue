<template>
  <div class="bot-config">
    <h3>Settings</h3>

    <div class="model-controls">
      <select class="select" v-model="selectedLM">
        <option disabled value="">Select a model</option>
        <option v-for="model in models" :key="model" :value="model">
          {{ model }}
        </option>
      </select>

      <select class="select" v-model="selectedPreprompt">
        <option disabled value="">Select a preprompt</option>
        <option
          v-for="(prompt, index) in preprompts"
          :key="index"
          :value="prompt"
          :title="prompt.text"
        >
          {{ prompt.name }}
        </option>
      </select>

    </div>

    <label class="rag-checkbox">
      <input type="checkbox" v-model="ragEnabled" />
      Enable RAG
    </label>

    <p v-if="selectedPreprompt" class="selected-text">
      {{ selectedPreprompt.text }}
    </p>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const selectedServer = defineModel('selectedServer')
const selectedLM = defineModel('selectedLM')
const ragEnabled = defineModel('ragEnabled')
const selectedPreprompt = defineModel('selectedPreprompt')

const models = ref([])
const preprompts = ref([])

onMounted(async () => {
  const res0 = await fetch(`/api/lms?base_url=${selectedServer.value}`)
  models.value = await res0.json()
  const res1 = await fetch('/api/preprompts')
  preprompts.value = await res1.json()
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

.selected-text {
  margin: 0;
  font-style: italic;
  color: #999;
}
</style>
