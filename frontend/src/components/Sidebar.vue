<template>
  <div class="sidebar">
    <h3>Ollama Server</h3>
    <select v-model="selectedServer">
      <option disabled value="">Select a Server</option>
      <option
        v-for="(server, index) in props.servers"
        :key="index"
        :value="server"
        :title="server"
      >
        {{ server }}
      </option>
    </select>

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
          :lms="lms"
          v-model:selectedLM="selectedLM"
          v-model:selectedSystemMessage="selectedSystemMessage"
          v-model:selectedMode="selectedMode"
          v-model:enableRag="enableRag"
          @file-upload="e => emit('file-upload', e)"
      />
    </div>
  </div>
</template>

<script setup>
import {ref, watch} from "vue";
import LMConfig from "./LMConfig.vue";
const emit = defineEmits(['view-selected', 'file-upload'])

const props = defineProps({
  servers: Array
})

const selectedView = ref('home')
const selectedServer = defineModel('selectedServer')
const selectedLM = defineModel('selectedLM')
const selectedSystemMessage = defineModel('selectedSystemMessage')
const selectedMode = defineModel('selectedMode')
const enableRag = defineModel(false)
const lms = ref([])

const options = [
  { value: 'home', label: 'Home'},
  { value: 'about', label: 'About'},
  { value: 'chatbot', label: 'Chatbot'},
  { value: 'assistant', label: 'Assistant'},
  { value: 'evaluation', label: 'Evaluation'}
]

watch(selectedServer, fetchModels, {immediate: true})

async function fetchModels() {
  const server = selectedServer.value
  console.log('fetch models from', server)
  try {
    const res0 = await fetch(`/api/lms?base_url=${server}`)
    lms.value = await res0.json()
    if (lms.value.length > 0 && !selectedLM.value) {
      selectedLM.value = lms.value[0]
    }
  } catch(err) {
    console.warn('Failed to fetch config', err)
    lms.value = []
  }
}

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

.sidebar select {
  width: 100%;
  padding: 0.5rem;
  margin-top: 1rem;
  background: #222;
  color: white;
  border: 2px solid gray;
  border-radius: 4px;
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
