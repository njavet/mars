<template>
  <div class="sidebar">
    <h3>Navigation</h3>
    <label v-for="option in options" :key="option.value" class="nav-option">
      <input
        type="radio"
        name="nav"
        :value="option.value"
        v-model="selectedView"
        @change="onSelectView"
      />
        {{ option.label }}
    </label>

    <div v-if="selectedView === 'chatbot' || selectedView === 'assistant'">
      <LMConfig
          :tools="tools"
          v-model:servers="servers"
          v-model:lms="lms"
          v-model:selectedLib="selectedLib"
          v-model:selectedServer="selectedServer"
          v-model:selectedModel="selectedModel"
          v-model:selectedSystemMessage="selectedSystemMessage"
          v-model:agentic="agentic"
          v-model:selectedTools="selectedTools"
          @file-upload="e => emit('file-upload', e)"
      />
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref, watch} from "vue";
import LMConfig from "./LMConfig.vue";
const emit = defineEmits(['view-selected', 'file-upload'])

const selectedView = ref('home')
const selectedLib = defineModel('selectedLib')
const selectedServer = defineModel('selectedServer')
const selectedModel = defineModel('selectedModel')
const selectedSystemMessage = defineModel('selectedSystemMessage')
const agentic = defineModel('agentic')
const selectedTools = defineModel('selectedTools')
const lms = defineModel('llms')
const servers = defineModel('servers')
const tools = ref([])

const options = [
  { value: 'home', label: 'Home'},
  { value: 'about', label: 'About'},
  { value: 'chatbot', label: 'Chatbot'},
  { value: 'assistant', label: 'Assistant'},
  { value: 'evaluation', label: 'Evaluation'}
]

onMounted(async() => {
  try {
    const res1 = await fetch('/api/tools')
    tools.value = await res1.json()
    selectedTools.value = []
  } catch(err) {
    console.warn('Failed to tools config', err)
    tools.value = []
  }
})

function onSelectView(event) {
  emit('view-selected', selectedView.value)
}

</script>

<style scoped>
.sidebar {
  width: 220px;
  flex-shrink: 0;
  background-color: #1f1f1f;
  color: white;
  padding: 1rem;
  box-sizing: border-box;
  border-right: 1px solid #444;
  text-align: left;
  overflow: auto;
}

.nav-option {
  display: block;
  margin-bottom: 0.5rem;
  color: white;
}

input[type="radio"] {
  margin-right: 0.5rem;
}
</style>
