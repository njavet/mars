<template>
  <div class="chat-wrapper">

    <div class="chat-header">
      <div class="model-controls">
        <select v-model="selectedLM">
          <option disabled value="">Select a model</option>
          <option v-for="model in models" :key="model" :value="model">
            {{ model }}
          </option>
        </select>
      </div>
      <label class="rag-checkbox">
        <input type="checkbox" v-model="ragEnabled" />
        Enable RAG
      </label>
      <button @click="showPromptPopup = true">Select Preprompt</button>
    </div>

    <div v-if="showPromptPopup" class="prompt-popup">
      <h3>Select a Preprompt</h3>
      <ul>
        <li v-for="(prompt, index) in preprompts" :key="index">
          <button @click="selectPreprompt(prompt)">
            {{ prompt.name }}
          </button>
        </li>
      </ul>
      <button @click="showPromptPopup = false">Close</button>
    </div>

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
        :disabled="!selectedLM"
        :title="!selectedLM ? 'Select a model first' : ''"
        placeholder="Type your message..."
        autofocus/>
      <div class="upload-area">
        <label for="upload" class="upload-button">@</label>
        <input
            id="upload"
            type="file"
            accept=".docx"
            @change="handleFileUpload"
            :disabled="!selectedLM"
            hidden/>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'

const props = defineProps({
  base_url: String
})

const models = ref([])
const preprompts = ref([])
const ragEnabled = ref(false)
const showPromptPopup = ref(false)
const selectedPreprompt = ref(null)
const selectedLM = ref('')
const messages = ref([])
const inputValue = ref("")
const chatContainer = ref(null)

onMounted(async () => {
  const res = await fetch(`/api/lms?base_url=${props.base_url}`)
  models.value = await res.json()
})

function selectPreprompt(prompt) {
  selectedPreprompt.value = prompt
  showPromptPopup.value = false
}

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
      lm_name: selectedLM.value,
      base_url: props.base_url,
      enable_rag: ragEnabled.value
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

  const res = await fetch(`/api/upload-docx?enable_rag=${ragEnabled.value}&lm_name=${selectedLM.value}&base_url=${props.base_url}`, {
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

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #ccc;
}
.model-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.rag-checkbox {
  display: flex;
  align-items: center;
  gap: 0.3rem;
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
.prompt-popup {
  position: absolute;
  top: 3.5rem;
  right: 1rem;
  background: white;
  border: 1px solid #ccc;
  padding: 1rem;
  z-index: 100;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  max-width: 300px;
}
</style>
