<template>
  <div class="sidebar">
    <h3>Ollama Server</h3>
    <select v-model="selectedServer" @change="onSelectServerChange">
      <option value="http://localhost:11434">Localhost</option>
    </select>
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
const emit = defineEmits(['model-selected', 'server-selected'])
const selectedServer = ref("http://localhost:11434")
const selectedLM = ref('')

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
  border: none;
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
  color: #ccc;
  text-decoration: none;
}

.sidebar a:hover {
  color: white;
}
</style>