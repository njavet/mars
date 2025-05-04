<template>
  <div class="assistant-container">
    <ResponseBox
        ref="childRef"
        :lm_name="props.lm_name"
        :loading="currentLoading"
        :messages="messages" />
    <div class="assistant-interface">
      <AssistantInterface
          :base_url="base_url"
          :lm_name="lm_name"
          :system_message="system_message"
          @file-upload="onFileUpload"/>
    </div>
  </div>
</template>

<script setup>
import {computed, ref} from 'vue'
import { handleFileUpload } from "../js/chatUtils.js"
import AssistantInterface from "./AssistantInterface.vue";
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

async function onFileUpload(event) {
  if (!childRef.value || !childRef.value.currentTab) {
    console.warn('childRef or currentTab not available')
    return
  }
  const activeTab = childRef.value.currentTab
  loadingByTab.value[activeTab] = true
  await handleFileUpload({
    event,
    props,
    messages,
    currentTab: activeTab
  })
  loadingByTab.value[activeTab] = false
}
</script>

<style scoped>
.assistant-container {
  flex: 1;
  display: flex;
  overflow: hidden;
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
