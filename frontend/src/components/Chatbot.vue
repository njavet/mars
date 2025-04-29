<template>
  <div class="chat-wrapper">
    <div class="tab-bar">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        :class="{ active: currentTab === tab.key }"
        @click="currentTab = tab.key"
        >
        {{ tab.label }}
      </button>
    </div>
    <div class="chat-area" ref="chatContainer">
      <LoadingAnimation :loading="loading" baseText="Thinking"/>
      <div v-if="shouldShowWelcome" class="message bot">
        <div class="bubble">
          <div class="message-text">Hi! Please select a model to start chatting.</div>
        </div>
      </div>
      <div
        v-for="(msg, index) in filteredMessages"
        :key="index"
        class="message"
        :class="msg.role === 'User' ? 'user' : 'bot'">
        <div class="bubble">
          <div class="message-text">{{ msg.text }}</div>
          </div>
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
            @change="handleFileUpload"
            :disabled="!props.lm_name"
            hidden/>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, computed } from 'vue'
import LoadingAnimation from "./LoadingAnimation.vue";
import { marked } from 'marked';
const currentTab = ref('base')
const tabs = [
  {key: 'base', label: 'Base'},
  {key: 'rag', label: 'RAG'},
  {key: 'agentic_rag', label: 'Agentic RAG'}

]

// animations
const loading = ref(false)

const messages = ref([])
const inputValue = ref('')
const chatContainer = ref(null)
const props = defineProps({
  base_url: String,
  lm_name: String,
  enable_rag: Boolean,
  system_message: String
})

const shouldShowWelcome = computed(() => {
  return !props.lm_name && messages.value.length === 0
})

const filteredMessages = computed(() => {
  return messages.value.filter(msg => msg.tab === currentTab.value)
})

function scrollToBottom() {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

function normalizeText(text) {
  return text.replace(/\n{3,}/g, '\n\n').trim()
}

async function handleEnter() {
  const userMsg = inputValue.value.trim()
  if (!userMsg) return
  loading.value = true

  messages.value.push({ role: 'User', text: userMsg, tab: currentTab.value })
  inputValue.value = ""
  scrollToBottom()
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      base_url: props.base_url,
      lm_name: props.lm_name,
      enable_rag: props.enable_rag,
      system_message: props.system_message,
      query: userMsg
    })
  })
  const data = await res.json()
  loading.value = false
  messages.value.push({
    role: 'Bot',
    text: normalizeText(data.response || 'Error.'),
    tab: currentTab.value
  })
  scrollToBottom()
}

async function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  loading.value = true

  messages.value.push({ role: 'User', text: `[Sent DOCX: ${file.name}]`})
  scrollToBottom()
  const formData = new FormData()
  formData.append('file', file)
  formData.append('base_url', props.base_url)
  formData.append('lm_name', props.lm_name)
  formData.append('enable_rag', props.enable_rag)
  formData.append('system_message', props.system_message)
  const res = await fetch('/api/upload-docx', {
    method: 'POST',
    body: formData
  })
  const data = await res.json()
  loading.value = false
  messages.value.push({ role: 'Bot', text: normalizeText(data.response || 'Error processing document.')})
  scrollToBottom()
}
</script>

<style scoped>
.chat-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header h2 {
  margin: 0;
  font-size: 1.2rem;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  overflow-y: auto;
  margin: 1rem;
  border: 2px solid cyan;
  border-radius: 8px;
  background-color: #333;
}

.message {
  font-family: monospace;
  display: flex;
  margin-bottom: 0.5rem;
}

.message-text {
  white-space: pre-wrap;
  word-wrap: break-word;
}

.message.user {
  justify-content: flex-end;
}

.message.bot {
  justify-content: flex-start;
}

.bubble {
  max-width: 60%;
  padding: 0.75rem;
  border-radius: 8px;
  background-color: #444;
  color: white;
  word-wrap: break-word;
}

.message.user .bubble {
  background-color: #6312ff;
  color: white;
  border-bottom-right-radius: 0;
}

.message.bot .bubble {
  background-color: #696969;
  border-bottom-left-radius: 0;
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
.tab-bar {
  display: flex;
  gap: 1rem;
  margin: 1rem;
}

.tab-bar button {
  background: #444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.tab-bar button.active {
  background: cyan;
  color: black;
}
</style>
