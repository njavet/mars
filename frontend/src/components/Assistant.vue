<template>
  <div class="assistant-container">
    <ResponseBox
        ref="childRef"
        :lm_name="props.lm_name"
        :loading="loading"
        :messages="messages" />
      <div class="main-area">
    </div>
    <div class="assistant-interface">
      <AssistantInterface
          :base_url="base_url"
          :lm_name="lm_name"
          :system_message="system_message"
          @bot-response="handleBotResponse"/>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { handleFileUpload } from "../js/chatUtils.js"
import AssistantInterface from "./AssistantInterface.vue";
import ResponseBox from "./ResponseBox.vue";

const childRef = ref(null)
const loading = ref(false)
const messages = ref([])
const props = defineProps({
  base_url: String,
  lm_name: String,
  system_message: String
})

function onFileUpload(event) {
  if (!childRef.value) return
  handleFileUpload({
    event,
    props,
    messages,
    tab: childRef.value.currentTab,
    loading,
  })
}
function handleBotResponse(message) {
  messages.value.push({ role: message.role, text: message.text})
}

</script>

<style scoped>
.assistant-container {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
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

.assistant-interface {
  width: 200px;
  background-color: #222;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 2rem;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.3);
}

.upload-area input[type="file"] {
  color: white;
}
</style>
