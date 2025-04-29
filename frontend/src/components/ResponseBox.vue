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
      <LoadingAnimation :loading="loading" baseText="Thinking"/>
      <div v-if="shouldShowWelcome" class="message bot">
        <div class="bubble">
          <div class="message-text">Hi! Please select a model to start chatting.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import LoadingAnimation from "./LoadingAnimation.vue"
import { tabs } from "../js/chatUtils.js"

const currentTab = ref('base')
const responseContainer = ref(null)
defineExpose({ responseContainer, currentTab })

const props = defineProps({
  lm_name: String,
  messages: Object
})

const shouldShowWelcome = computed(() => {
  return !props.lm_name && props.messages.value.length === 0
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
