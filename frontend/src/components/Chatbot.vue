<template>
  <ResponseBox
      ref="childRef"
      :lm_name="props.lm_name"
      :loading="currentLoading"
      :messages="messages" />
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
import { getEndpoint, handleFileUpload } from "../js/chatUtils.js"

const childRef = ref(null)
const loadingByTab = ref({
  base: false,
  rag: false,
  agentic_base: false,
  agentic_rag: false
})

const messages = ref([])
const inputValue = ref('')
const props = defineProps({
  base_url: String,
  port: Number,
  lm_name: String,
  system_message: String,
})
console.log('port', props.port)
console.log('lm_name', props.lm_name)

const currentLoading = computed(() => {
  const tab = childRef.value?.currentTab
  return tab ? loadingByTab.value[tab] : false
})

async function onFileUpload(event) {
  if (!childRef.value || !childRef.value.currentTab) {
    console.warn('childRef or currentTab not available')
    return
  }
  const activeTab = childRef.value.currentTab
  loadingByTab.value[activeTab] = true
  await handleFileUpload({
    event,
    props,
    messages,
    currentTab: activeTab
  })
  loadingByTab.value[activeTab] = false
}

async function handleEnter() {
  const userMsg = inputValue.value.trim()
  if (!userMsg) return
  const activeTab = childRef.value.currentTab
  loadingByTab.value[activeTab] = true

  messages.value.push({
    role: 'User',
    text: userMsg,
    tab: activeTab
  })
  inputValue.value = ""
  const endpoint = getEndpoint(activeTab)
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      server: props.base_url + ':' + props.port,
      lm_name: props.lm_name,
      system_message: props.system_message,
      query: userMsg
    })
  })
  const data = await res.json()
  messages.value.push({
    role: 'Bot',
    text: data.response || 'Error.',
    tab: activeTab
  })
  loadingByTab.value[activeTab] = false
}
</script>

<style scoped>
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
