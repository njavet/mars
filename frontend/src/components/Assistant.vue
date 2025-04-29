<template>
  <div class="assistant-container">
    <div class="main-area">
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
          :system_message="system_message"
          @bot-response="handleBotResponse"/>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { marked } from 'marked'
import AssistantInterface from "./AssistantInterface.vue";

const messages = ref([])
const responseContainer = ref(null)
const props = defineProps({
  base_url: String,
  lm_name: String,
  system_message: String
})

function scrollToBottom() {
  nextTick(() => {
    if (responseContainer.value) {
      responseContainer.value.scrollTop = responseContainer.value.scrollHeight
    }
  })
}

function handleBotResponse(message) {
  messages.value.push({ role: message.role, text: message.text})
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

.upload-area input[type="file"] {
  color: white;
}
</style>
