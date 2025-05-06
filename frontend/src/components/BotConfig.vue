<template>
  <div class="bot-config">
    <h3>Settings</h3>

    <div class="model-controls">
      <label>Language Model</label>
      <select class="select" v-model="selectedLM">
        <option disabled value="">Select a model</option>
        <option v-for="model in props.lms" :key="model" :value="model">
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
          {{ system_message.key }}
        </option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  lms: Array
})
const selectedLM = defineModel('selectedLM')
const selectedSystemMessage = defineModel('selectedSystemMessage')
const systemMessages = ref([])

onMounted(async() => {
  const res1 = await fetch('/api/system-messages')
  systemMessages.value = await res1.json()
  console.log(systemMessages.value)
  if (systemMessages.value.length > 0 && !selectedSystemMessage.value) {
    selectedSystemMessage.value = systemMessages.value[0].key
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
</style>
