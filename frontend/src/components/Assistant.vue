<template>
  <div class="assistant-container">
    <ResponseBox
        ref="childRef"
        :lm_name="props.lm_name"
        :loading="loading"
        :messages="messages" />
  </div>
</template>

<script setup>
import {ref} from 'vue'
import { useFileUpload } from '../js/chatUtils.js'
import ResponseBox from './ResponseBox.vue';

const childRef = ref(null)
const loading = ref(false)
const messages = ref([])
const props = defineProps({
  base_url: String,
  lm_name: String,
  system_message: String
})

const { onFileUpload } = useFileUpload({
  childRef,
  messages,
  props
})

defineExpose({ onFileUpload })
</script>

<style scoped>
.assistant-container {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.upload-area input[type="file"] {
  color: white;
}
</style>
