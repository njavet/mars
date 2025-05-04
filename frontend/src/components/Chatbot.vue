<template>
  <ResponseBox
      ref="childRef"
      :lm_name="props.lm_name"
      :loading="loading"
      :messages="messages" />
  <div class="input-area horizontal">
    <input
      type="text"
      v-model="inputValue"
      @keydown.enter="handleEnter"
      :disabled="!props.lm_name"
      :title="!props.lm_name ? 'Select a model first' : ''"
      placeholder="Type your message..."
      autofocus/>
    <div class="upload-area">
      <label for="upload" class="upload-button">@</label>
      <input
          id="upload"
          type="file"
          accept=".docx"
          @change="onFileUpload"
          :disabled="!props.lm_name"
          hidden/>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import ResponseBox from "./ResponseBox.vue"
import { handleFileUpload } from "../js/chatUtils.js"

const childRef = ref(null)
const loading = ref(false)
const messages = ref([])
const inputValue = ref('')
const props = defineProps({
  base_url: String,
  lm_name: String,
  system_message: String,
})

function onFileUpload(event) {
  if (!childRef.value) return
  handleFileUpload({
    event,
    props,
    messages,
    tab: childRef.value.currentTab,
    loading,
  })
}

function enableRag() {
  const cond0 = childRef.value.currentTab === 'rag'
  const cond1 = childRef.value.currentTab === 'agentic_rag'
  return cond0 || cond1
}

function endpoint() {
  const cond0 = childRef.value.currentTab === 'agentic'
  const cond1 = childRef.value.currentTab === 'agentic_rag'
  if (cond0 || cond1) {
    return '/api/agentic/chat'
  } else {
    return '/api/baseline/chat'
  }
}

async function handleEnter() {
  const userMsg = inputValue.value.trim()
  if (!userMsg) return
  loading.value = true

  messages.value.push({
    role: 'User',
    text: userMsg,
    tab: childRef.value.currentTab})
  inputValue.value = ""
  const res = await fetch(endpoint(), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      base_url: props.base_url,
      lm_name: props.lm_name,
      enable_rag: enableRag(),
      system_message: props.system_message,
      query: userMsg
    })
  })
  const data = await res.json()
  loading.value = false
  messages.value.push({
    role: 'Bot',
    text: data.response || 'Error.',
    tab: childRef.value.currentTab
  })
}
</script>

<style scoped>
.upload-area {
  background: #111;
}

.upload-area input[type="file"] {
  color: white;
}

.input-area {
  padding: 1rem;
  background: #222;
}

.input-area.horizontal {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.input-area input {
  border: 2px solid gray;
  padding: 10px;
  border-radius: 6px;
  font-size: 1em;
  background-color: #333;
  color: white;
  outline: none;
}

.input-area.horizontal input[type="text"] {
  flex: 1;
}

.upload-button {
  cursor: pointer;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border: 2px solid gray;
  background: #555;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
}
.upload-button:hover {
  background: #666;
}
</style>
