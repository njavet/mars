<template>
  <div class="chat-wrapper">
    <div class="chat-area" ref="chatContainer">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        class="message"
        :class="msg.role === 'User' ? 'user' : 'bot'">
        <div class="bubble"><strong>{{ msg.role }}:</strong> {{ msg.text }}</div>
        </div>
      </div>
    <div class="input-area horizontal">
      <input
        type="text"
        v-model="inputValue"
        @keydown.enter="handleEnter"
        placeholder="Type your message..."
        autofocus/>
      <div class="upload-area">
        <label for="upload" class="upload-button">@</label>
        <input id="upload" type="file" accept=".docx" @change="handleFileUpload" hidden/>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'

const props = defineProps({
  lm_name: String,
  base_url: String
})

const messages = ref([])
const inputValue = ref("")
const chatContainer = ref(null)

function scrollToBottom() {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

async function handleEnter() {
  const userMsg = inputValue.value.trim()
  if (!userMsg) return

  messages.value.push({ role: 'User', text: userMsg })
  inputValue.value = ""
  messages.value.push({ role: 'Bot', text: 'Thinking...' })
  scrollToBottom()

  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: userMsg,
      lm_name: props.lm_name,
      base_url: props.base_url
    })
  })

  const data = await res.json()
  messages.value.pop()
  messages.value.push({ role: 'Bot', text: data.response || 'Error' })
  scrollToBottom()
}

async function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  messages.value.push({ role: 'User', text: `[Sent DOCX: ${file.name}]`})
  messages.value.push({ role: 'Bot', text: 'Thinking...' })
  scrollToBottom()
  const formData = new FormData()
  formData.append('file', file)

  const res = await fetch(`/api/upload-docx?lm_name=${props.lm_name}&base_url=${props.base_url}`, {
    method: 'POST',
    body: formData
  })

  const data = await res.json()
  messages.value.pop()
  scrollToBottom()
  messages.value.push({ role: 'Bot', text: data.response || 'Error processing document.'})
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

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  overflow-y: auto;
  background-color: #333;
  max-height: 100%;
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
  background-color: #0084ff;
  color: white;
  border-bottom-right-radius: 0;
}

.message.bot .bubble {
  background-color: #333;
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

.input-area input {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: none;
  font-size: 1em;
  background-color: #333;
  color: white;
  outline: none;
}

.input-area.horizontal {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.input-area.horizontal input[type="text"] {
  flex: 1;
}

.upload-button {
  cursor: pointer;
  font-size: 1rem;
  padding: 0.5rem;
  background: #555;
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-button:hover {
  background: #666;
}
</style>
