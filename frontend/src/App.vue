<template>
  <div class="app-container">
    <div class="sidebar">
      <h2>LLMs</h2>
      <select v-model="selectedModel">
        <option v-for="model in models" :key="model" :value="model">
          {{ model }}
        </option>
      </select>
    </div>
    <div class="main-content" v-if="selectedModel">
      <Chat :model="selectedModel" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chat from './components/Chat.vue'

const models = ref([])
const selectedModel = ref("")

onMounted(async () => {
  const res = await fetch('/api/lms')
  models.value = await res.json()
  selectedModel.value = models.value[0] || ""
})

</script>

<style scoped>

.app-container {
  height: 100vh;
  width: 100vw;
  display: flex;
  overflow: hidden;
}

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

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>