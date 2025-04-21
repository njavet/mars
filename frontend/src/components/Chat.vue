<template>
  <div class="chat-wrapper">
    <div class="chat-area" ref="chatContainer">
      <div v-for="(msg, index) in messages" :key="index" class="message">
        <strong>{{ msg.role }}:</strong> {{ msg.text }}
      </div>
    </div>

    <div class="input-area">
      <input
        type="text"
        v-model="inputValue"
        @keydown.enter="handleEnter"
        placeholder="Type your message..."
        autofocus
      />
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
    body: JSON.stringify({ text: userMsg })
  })

  const data = await res.json()
  messages.value.push({ role: 'Bot', text: data.response || 'Error' })
  scrollToBottom()
}
</script>

<style scoped>
.chat-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-area {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  background-color: #747bff;
}

.message {
  margin-bottom: 0.5rem;
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
