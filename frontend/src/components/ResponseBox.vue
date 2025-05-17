<template>
  <div class="response-container">
    <div class="response-area" ref="responseContainer">

      <div v-if="shouldShowWelcome" class="message bot">
        <div class="bubble">
          <div class="message-text">Hi! Please select a model to start chatting.</div>
        </div>
      </div>

      <div
          v-for="(msg, index) in props.messages"
          :key="index"
          class="message"
          :class="msg.role === 'User' ? 'user' : 'bot'"
      >
        <div class="bubble">
          <div class="message-text">{{ msg.text }}</div>
        </div>
      </div>
        <LoadingAnimation
            :loading="props.loading"
            baseText="Thinking"/>
    </div>
  </div>
</template>

<script setup>
import {watch, ref, computed, onMounted, nextTick} from "vue"
import LoadingAnimation from "./LoadingAnimation.vue"
const responseContainer = ref(null)
defineExpose({ responseContainer  })

const props = defineProps({
  model: String,
  loading: Boolean,
  messages: Array
})

function scrollToBottom() {
  if (responseContainer.value) {
      responseContainer.value.scrollTop = responseContainer.value.scrollHeight
  }
}

const shouldShowWelcome = computed(() => {
  return !props.model && props.messages.length === 0
})

onMounted(() => {
  scrollToBottom()
})

watch(() => props.messages, async() => {
  await nextTick()
  scrollToBottom()
}, { deep: true })

</script>

<style scoped>
.response-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.response-area {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  overflow-y: auto;
  margin: 1rem;
  border: 2px solid #747bff;
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

.message.bot {
  text-align: left;
  justify-content: flex-start;
}

.message.bot .bubble {
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
