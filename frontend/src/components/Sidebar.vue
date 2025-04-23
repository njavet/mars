<template>
  <div class="sidebar">
    <h2>Language Models</h2>
    <select v-model="selected" @change="onSelectChange">
      <option disabled value="">Select a Model</option>
      <option v-for="model in models" :key="model" :value="model">
        {{ model }}
      </option>
    </select>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
const emit = defineEmits(['model-selected'])
const selected = ref('')

function onSelectChange(event) {
  emit('model-selected', selected.value)
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