<template>
  <ResponseBox
      ref="childRef"
      :model_name="props.model_name"
      :loading="loading"
      :messages="messages" />
  <div class="input-area horizontal">
    <input
      type="text"
      v-model="inputValue"
      @keydown.enter="handleEnter"
      :disabled="!props.model_name"
      :title="!props.model_name ? 'Select a model first' : ''"
      placeholder="Type your message..."
      autofocus/>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ResponseBox from './ResponseBox.vue'
import { useFileUpload} from '../js/chatUtils.js'
const childRef = ref(null)
const loading = ref(false)
const messages = ref([])
const inputValue = ref('')
const props = defineProps({
  onFileUpload: Function,
  base_url: String,
  model_name: String,
  system_message: String,
  agentic: Boolean,
  selected_tools: Array
})

const { onFileUpload } = useFileUpload({
  messages,
  loading,
  props
})
defineExpose({ onFileUpload })

async function handleEnter() {
  const userMsg = inputValue.value
  if (!userMsg) return
  loading.value = true
  messages.value.push({
    role: 'user',
    text: userMsg,
  })
  inputValue.value = ''
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      base_url: props.base_url,
      model_name: props.model_name,
      system_message: props.system_message,
      user_message: userMsg,
      agentic: props.agentic,
      tools: props.selected_tools
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
</style>
