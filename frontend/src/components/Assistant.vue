<template>
  <div class="assistant-container">
    <div class="response-area" ref="ResponseContainer">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        class="message"
        :class="msg.role === 'User' ? 'user' : 'bot'">
        <div class="bubble"><strong>{{ msg.role }}:</strong> {{ msg.text }}</div>
        </div>
      </div>
    <div>
    <AssistantInterface/>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import AssistantInterface from "./AssistantInterface.vue";

const messages = ref([])
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

async function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  messages.value.push({ role: 'User', text: `[Sent DOCX: ${file.name}]`})
  messages.value.push({ role: 'Bot', text: 'Thinking...' })
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
  messages.value.pop()
  scrollToBottom()
  messages.value.push({ role: 'Bot', text: data.response || 'Error processing document.'})
  scrollToBottom()
}
</script>

<style scoped>
.assistant-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header h2 {
  margin: 0;
  font-size: 1.2rem;
}

.response-area {
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

.message.bot .bubble {
  background-color: #696969;
  border-bottom-left-radius: 0;
}

.upload-area input[type="file"] {
  color: white;
}
</style>
