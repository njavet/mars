<template>
  <ResponseBox
      ref="childRef"
      :onFileUpload="props.onFileUpload"
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
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import ResponseBox from "./ResponseBox.vue"
import { getEndpoint, useFileUpload} from "../js/chatUtils.js"
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
  onFileUpload: Function,
  base_url: String,
  lm_name: String,
  system_message: String,
})

const currentLoading = computed(() => {
  const tab = childRef.value?.currentTab
  return tab ? loadingByTab.value[tab] : false
})

const { onFileUpload } = useFileUpload({
  childRef,
  messages,
  loadingByTab,
  props
})
defineExpose({ onFileUpload })

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
      base_url: props.base_url,
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
