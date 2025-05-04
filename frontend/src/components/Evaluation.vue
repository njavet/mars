<template>
  <div class="evaluation-container">
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
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { marked } from 'marked'

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
</script>

<style scoped>
.evaluation-container {
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



.upload-area input[type="file"] {
  color: white;
}
</style>
