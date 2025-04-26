<template>
  <div class="chat-wrapper">
    <div class="chat-area" ref="chatContainer">
      <Transition name="fade">
        <div v-if="loading" class="loading-overlay">
          <div class="loading-content">
            <div class="loader"></div>
            <div class="loader-text">Thinking...</div>
          </div>
        </div>
      </Transition>
      <div
        v-for="(msg, index) in messages"
        :key="index"
        class="message"
        :class="msg.role === 'User' ? 'user' : 'bot'">
        <div class="bubble"><strong>{{ msg.role }}:</strong>
        <div v-html="marked(msg.text)" class="message-text"></div>
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
import { ref, nextTick } from 'vue'
import { marked } from 'marked';

const loading = ref(false)

const messages = ref([])
const inputValue = ref('')
const chatContainer = ref(null)
const props = defineProps({
  base_url: String,
  lm_name: String,
  enable_rag: Boolean,
  preprompt: String
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

  messages.value.push({ role: 'User', text: userMsg })
  inputValue.value = ""
  scrollToBottom()
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      base_url: props.base_url,
      lm_name: props.lm_name,
      enable_rag: props.enable_rag,
      preprompt: props.preprompt,
      query: userMsg
    })
  })
  const data = await res.json()
  loading.value = false
  messages.value.push({ role: 'Bot', text: normalizeText(data.response || 'Error.')})
  scrollToBottom()
}

async function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  messages.value.push({ role: 'User', text: `[Sent DOCX: ${file.name}]`})
  scrollToBottom()
  const formData = new FormData()
  formData.append('file', file)
  formData.append('base_url', props.base_url)
  formData.append('lm_name', props.lm_name)
  formData.append('enable_rag', props.enable_rag)
  formData.append('preprompt', props.preprompt)
  const res = await fetch('/api/upload-docx', {
    method: 'POST',
    body: formData
  })
  const data = await res.json()
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
  display: flex;
  margin-bottom: 0.5rem;
}

.message.user {
  justify-content: flex-end;
}

.message.bot {
  justify-content: flex-start;
  white-space: pre-wrap;
  word-wrap: break-word;
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

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: calc(100% + 220px);
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.4);
  z-index: 10;
}
.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loader {
  width: 200px;
  height: 6px;
  background: linear-gradient(
    to right,
    transparent 0%,
    cyan 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: knightRide 1.5s infinite linear;
  border-radius: 5px;
}

@keyframes knightRide {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.loader-text {
  color: cyan;
  font-size: 1.2rem;
  font-weight: bold;
  text-shadow: 0 0 5px cyan;
}

@keyframes knightRide {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 1s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

</style>
