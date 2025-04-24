<template>
  <div class="sidebar">

    <h3>Ollama Server</h3>
    <select v-model="selectedServer" @change="onSelectServerChange">
      <option value="http://localhost:11434">Localhost</option>
    </select>

    <h3>Navigation</h3>
    <label v-for="option in options" :key="option.value" class="nav-option">
      <input
        type="radio"
        name="nav"
        :value="option.value"
        v-model="selectedView"
        @change="emit('view-selected', selectedView)"/>
      {{ option.lavel }}
    </label>

    <h3>Language Models</h3>
    <select v-model="selectedLM" @change="onSelectLMChange">
      <option disabled value="">Select a Model</option>
      <option v-for="model in models" :key="model" :value="model">
        {{ model }}
      </option>
    </select>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
const emit = defineEmits([
    'model-selected', 'server-selected', 'view-selected'
])
const selectedServer = ref("http://localhost:11434")
const selectedView = ref('chat')
const selectedLM = ref('')

const options = [
  { value: 'chat', label: 'Chatbot'},
  { value: 'evaluation', label: 'Evaluation'}
]

function onSelectServerChange(event) {
  emit('server-selected', selectedServer.value)
}

function onSelectLMChange(event) {
  emit('model-selected', selectedLM.value)
}

const models = ref([])

onMounted(async () => {
  const res = await fetch('/api/lms')
  models.value = await res.json()
})

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

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin: 1rem 0;
}

.sidebar a {
  color: #6312ff;
  text-decoration: none;
}

.sidebar a:hover {
  color: #6312ff;
}
</style>