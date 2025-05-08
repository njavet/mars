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
          :key="system_message.key"
          :value="system_message.text"
          :title="system_message.text"
        >
          {{ system_message.key }}
        </option>
      </select>
    </div>
    <div class="upload-area">
      <label for="upload" class="sidebar-button">Upload Document</label>
        <input
            id="upload"
            type="file"
            accept=".docx"
            @change="emit('file-upload', $event)"
            hidden/>
      </div>
      <label for="upload-text" class="sidebar-button">Upload Text File</label>
        <input
          id="upload-text"
          type="file"
          accept=".txt"
          @change="emit('file-upload', $event)"
          hidden/>
    <button class="sidebar-button" @click="emit('improve')">Improve</button>
    <button class="sidebar-button" @click="emit('save')">Save</button>
  </div>
</template>

<script setup>
import {ref, onMounted } from 'vue'

const emit = defineEmits([
  'file-upload',
  'improve',
  'save'])
const props = defineProps({
  lms: Array
})
const selectedLM = defineModel('selectedLM')
const selectedSystemMessage = defineModel('selectedSystemMessage')
const systemMessages = ref([])

onMounted(async() => {
  const res = await fetch('/api/system-messages')
  const raw = await res.json()
  systemMessages.value = raw
  if (systemMessages.value.length > 0 && !selectedSystemMessage.value) {
    selectedSystemMessage.value = raw[0].text
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

.upload-area {
  background: #111;
}

.upload-area input[type="file"] {
  color: white;
}

.sidebar-button {
  cursor: pointer;
  font-size: 0.8rem;
  padding: 0.5rem 1rem;
  border: 2px solid gray;
  background: #555;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
}

.sidebar-button:hover {
  background: #666;
}
</style>
