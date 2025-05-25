<template>
  <div class="output-container" ref="outputContainer">
    <div
        v-for="(msg, index) in messages"
        :key="index"
        class="message"
        :class="msg.role">
      <div class="bubble">
        <div class="message-text">{{ msg.text }}</div>
      </div>
    </div>
    <LoadingAnimation :loading="loading" baseText="Thinking"/>
  </div>
</template>

<script setup>
import { watch, ref, onMounted, nextTick } from 'vue'
import LoadingAnimation from './LoadingAnimation.vue'
import { useChatState } from "../composables/useState.js";
const outputContainer = ref(null)
const {
  messages,
  loading,
} = useChatState()

function scrollToBottom() {
  if (outputContainer.value) {
      outputContainer.value.scrollTop = outputContainer.value.scrollHeight
  }
}

onMounted(() => {
  scrollToBottom()
})

watch(() => messages, async() => {
  await nextTick()
  scrollToBottom()
}, { deep: true })

</script>

<style scoped>
.output-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
  padding: 1rem;
  overflow-y: auto;
  margin: 0.2rem;
  border: 1px solid #747bff;
  border-radius: 8px;
  background-color: #333;
}

.message {
  display: flex;
  margin-bottom: 0.5rem;
  justify-content: flex-end;
}

.bubble {
  max-width: 60%;
  padding: 0.75rem;
  border-radius: 8px;
  background-color: #444;
  color: white;
  word-wrap: break-word;
}

.message.assistant {
  text-align: left;
  justify-content: flex-start;
}

.message.user {
  text-align: left;
}

.message.assistant .bubble {
  background-color: #696969;
  border-bottom-left-radius: 0;
}

.message.user .bubble {
  background-color: #747bff;
  color: white;
  border-bottom-right-radius: 0;
}

.message-text {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
