<template>
  <ChatOutput :loading="loading" :messages="messages" />

  <div class="input-container">
    <input
      type="text"
      v-model="inputValue"
      @keydown.enter="handleEnter"
      class="chat-input"
      placeholder="Type your message..."
      autofocus/>
    <div class="dropdown-container" @click="toggleMenu">
      <div v-if="menuOpen" class="dropdown-menu">
        <button @click="uploadDoc">Send Document</button>
        <button @click="deleteChat">Delete Chat</button>
      </div>
      <button class="menu-button">:</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ChatOutput from './ChatOutput.vue'
import { useBotState } from '../composables/useState.js'
import { endpoints } from '../js/endpoints.js'

const inputValue = ref('')
const menuOpen = ref(false)
const loading = ref(false)
const messages = ref([])
const toggleMenu = () => menuOpen.value = !menuOpen.value
const {
  selectedLib,
  selectedServer,
  selectedModel,
  selectedSystemMessage,
  agentic
} = useBotState()

async function handleEnter() {
  const userMsg = inputValue.value
  if (!userMsg) return
  loading.value = true
  messages.value.push({
    role: 'user',
    text: userMsg,
  })
  inputValue.value = ''
  let base_url
  if (selectedLib === 'transformers') {
    base_url = ''
  } else {
    base_url = selectedServer.value
  }
  const res = await fetch(endpoints.chat, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      base_url: base_url,
      model_name: selectedModel.value,
      system_message: selectedSystemMessage.value,
      user_message: userMsg,
      agentic: agentic.value,
    })
  })
  const data = await res.json()
  messages.value.push({
    role: 'assistant',
    text: data || 'Error.',
  })
  loading.value = false
}
</script>

<style scoped>
.input-container {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  background: #222;
  border: 1px solid gray;
}

.chat-input {
  flex: 1;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid gray;
  border-radius: 8px;
  background-color: #333;
  outline: none;
}

.dropdown-container {
  position: relative;
}

.menu-button {
  padding: 0.5rem;
  cursor: pointer;
  margin-left: 0.5rem;
  height: 2.5rem;
  width: 2.5rem;
  border: 1px solid gray;
}

.dropdown-menu {
  position: absolute;
  bottom: 3.5rem;
  right: 0.5rem;
  background: #333;
  border: 1px solid #ccc;
  display: flex;
  flex-direction: column;
  min-width: 140px;
  z-index: 10;
}

.dropdown-menu button {
  padding: 0.5rem;
  text-align: left;
  background: none;
  border: none;
  cursor: pointer;
}

.dropdown-menu button:hover {
  background: #eee;
}
</style>
