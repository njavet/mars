<template>
  <div class="assistant-container">
    <ResponseBox
        ref="childRef"
        :lm_name="props.lm_name"
        :loading="currentLoading"
        :messages="messages" />
  </div>
</template>

<script setup>
import {computed, ref} from 'vue'
import { useFileUpload } from "../js/chatUtils.js"
import ResponseBox from "./ResponseBox.vue";

const childRef = ref(null)
const loadingByTab = ref({
  base: false,
  rag: false,
  agentic_base: false,
  agentic_rag: false
})

const currentLoading = computed(() => {
  const tab = childRef.value?.currentTab
  return tab ? loadingByTab.value[tab] : false
})

const messages = ref([])
const props = defineProps({
  base_url: String,
  lm_name: String,
  system_message: String
})
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
