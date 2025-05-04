<template>
  <div class="response-container">
    <div class="tab-bar">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        :class="{ active: currentTab === tab.key }"
        @click="currentTab = tab.key"
        >
        {{ tab.label }}
      </button>
    </div>
    <div class="response-area" ref="responseContainer">
      <LoadingAnimation :loading="props.loading" baseText="Thinking"/>
      <div v-if="shouldShowWelcome" class="message bot">
        <div class="bubble">
          <div class="message-text">Hi! Please select a model to start chatting.</div>
        </div>
      </div>
      <div
          v-for="(msg, index) in filteredMessages"
          :key="index"
          class="message"
          :class="msg.role === 'User' ? 'user' : 'bot'"
      >
        <div class="bubble">
          <div class="message-text">{{ msg.text }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted, nextTick} from "vue"
import LoadingAnimation from "./LoadingAnimation.vue"
import { tabs } from "../js/chatUtils.js"

const currentTab = ref('base')
const responseContainer = ref(null)
defineExpose({ responseContainer, currentTab })

const props = defineProps({
  lm_name: String,
  loading: Boolean,
  messages: Array
})

onMounted(() => {
  scrollToBottom()
})

function scrollToBottom() {
  if (responseContainer.value) {
      responseContainer.value.scrollTop = responseContainer.value.scrollHeight
  }
}

const filteredMessages = computed(() => {
  return props.messages.filter(msg => msg.tab === currentTab.value)
})

const shouldShowWelcome = computed(() => {
  return !props.lm_name && props.messages.length === 0
})
</script>

<style scoped>
.response-container {
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

.message {
  display: flex;
  margin-bottom: 0.5rem;
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

.message-text {
  white-space: pre-wrap;
  word-wrap: break-word;
}

.message.user {
  justify-content: flex-end;
}

.message.user .bubble {
  background-color: #6312ff;
  color: white;
  border-bottom-right-radius: 0;
}

.tab-bar {
  display: flex;
  gap: 1rem;
  margin: 1rem;
}

.tab-bar button {
  background: #444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.tab-bar button.active {
  background: cyan;
  color: black;
}
</style>
