<template>
  <ResponseBox
      ref="childRef"
      :lm_name="props.lm_name"
      :loading="loading"
      :messages="messages" />
  <div
      v-for="(msg, index) in filteredMessages"
      :key="index"
      class="message"
      :class="msg.role === 'User' ? 'user' : 'bot'">
      <div class="bubble">
        <div class="message-text">{{ msg.text }}</div>
      </div>
  </div>
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
import { ref, computed } from "vue"
import ResponseBox from "./ResponseBox.vue"
import { scrollToBottom, handleFileUpload, tabs } from "../js/chatUtils.js"

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
  handleFileUpload({
    event,
    props,
    messages,
    currentTab,
    loading,
    chatContainer
  })
}

function normalizeText(text) {
  return text.replace(/\n{3,}/g, '\n\n').trim()
}

function enableRag() {
  return currentTab.value === 'rag' || currentTab.value === 'agentic_rag';
}
function endpoint() {
  if (currentTab.value === 'agentic' || currentTab.value === 'agentic_rag') {
    return '/api/agentic/chat'
  } else {
    return '/api/baseline/chat'
  }
}

async function handleEnter() {
  const userMsg = inputValue.value.trim()
  if (!userMsg) return
  loading.value = true

  messages.value.push({ role: 'User', text: userMsg, tab: currentTab.value })
  inputValue.value = ""
  scrollToBottom()
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
    tab: currentTab.value
  })
  scrollToBottom(chatContainer)
}
</script>

<style scoped>
.message.user {
  justify-content: flex-end;
}

.message.user .bubble {
  background-color: #6312ff;
  color: white;
  border-bottom-right-radius: 0;
}

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
