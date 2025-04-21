<template>
  <div class="chat-wrapper">

    <div class="chat-area" ref="chatContainer">
      <div v-for="(msg, index) in messages" :key="index" class="message">
        <strong>{{ msg.role }}:</strong> {{ msg.text }}
      </div>
    </div>

    <div class="upload-area">
      <input type="file" accept=".docx" @change="handleFileUpload"/>
    </div>

    <div class="input-area">
      <input
        type="text"
        v-model="inputValue"
        @keydown.enter="handleEnter"
        placeholder="Type your message..."
        autofocus/>
    </div>

  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

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
  scrollToBottom()

  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: userMsg })
  })

  const data = await res.json()
  messages.value.push({ role: 'Bot', text: data.response || 'Error' })
  scrollToBottom()
}

async function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  const res = await fetch('/api/upload-docx', {
    method: 'POST',
    body: formData
  })

  const data = await res.json()
  messages.value.push({ role: 'User', text: `[Sent DOCX: ${file.name}`})
  messages.value.push({ role: 'Bot', text: data.response || 'Error processing document.'})
  scrollToBottom()
}

</script>

<style scoped>
.chat-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.chat-area {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  background-color: #333;
}

.message {
  margin-bottom: 0.5rem;
}

.upload-area {
  background: #111;
  padding: 1rem;
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
</style>
