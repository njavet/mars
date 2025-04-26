<template>
  <div class="assistant-container">
    <div class="main-area">
      <LoadingAnimation :loading="loading" baseText="Evaluating Document" />
      <div class="response-area" ref="responseContainer">
        <div
            v-for="(msg, index) in messages"
            :key="index"
            class="message">
          <div class="bubble">
            <strong>{{ msg.role }}:</strong>
              <div v-html="marked(msg.text)" class="message-text"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="assistant-interface">
      <AssistantInterface
          :base_url="base_url"
          :lm_name="lm_name"
          :enable_rag="enable_rag"
          :preprompt="preprompt"
          @bot-response="handleBotResponse"/>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { marked } from 'marked'
import AssistantInterface from "./AssistantInterface.vue";
import LoadingAnimation from "./LoadingAnimation.vue";

const loading = ref(false)
const messages = ref([])
const responseContainer = ref(null)
const props = defineProps({
  base_url: String,
  lm_name: String,
  enable_rag: Boolean,
  preprompt: String
})

function scrollToBottom() {
  nextTick(() => {
    if (responseContainer.value) {
      responseContainer.value.scrollTop = responseContainer.value.scrollHeight
    }
  })
}

function normalizeText(text) {
  return text.replace(/\n{3,}/g, '\n\n').trim()
}

function handleBotResponse(message) {
  loading.value = true
  messages.value.push({ role: message.role, text: normalizeText(message.text)})
  loading.value = false
  scrollToBottom()
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

.message {
  display: flex;
  margin-bottom: 0.5rem;
}

.message-text {
  white-space: pre-wrap;
  word-wrap: break-word;
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
