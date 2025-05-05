<template>
  <div class="selector-container">
    <label>
      Select file:
      <select v-model="selectedFileIndex">
        <option v-for="(file, index) in filenames" :key="file" :value="index">
          {{ file }}
        </option>
      </select>
    </label>

    <label v-if="lmEntries.length > 0">
      Select model:
      <select v-model="selectedLM">
        <option v-for="entry in lmEntries" :key="entry.lm" :value="entry.lm">
          {{ entry.lm}}
        </option>
      </select>
    </label>

    <div v-if="selectedOutput" class="output-display">
      <strong>Output:</strong>
      <pre>{{ selectedOutput }}</pre>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref, computed, watch} from 'vue'

const filenames = ref([])
const fileData = ref([])
const selectedFileIndex = ref(0)
const selectedLM = ref(null)

onMounted(async () => {
  const res = await fetch('/api/results/file-list')
  filenames.value = await res.json()
  const results = await Promise.all(
    filenames.value.map(name =>
      fetch (`/results/${name}`).then(res => res.json())
    )
  )
  fileData.value = results
  selectedLM.value = results[0]?.[0]?.lm_ ?? null
})
const lmEntries = computed(() => {
  return fileData.value[selectedFileIndex.value] || []
})

const selectedOutput = computed(() => {
  return lmEntries.value.find(e => e.lm === selectedLM.value)?.output || ''
})

watch(selectedFileIndex, () => {
  selectedLM.value = lmEntries.value[0]?.lm || null
})
</script>
<style scoped>
.selector-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 600px;
}

select {
  padding: 0.4rem;
  font-size: 1rem;
}

.output-display {
  background: #222;
  padding: 1rem;
  border: 1px solid cyan;
  border-radius: 6px;
  color: white;
  max-height: 300px;
  overflow: auto;
}
pre {
  white-space: pre-wrap;
  background: #333;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 0.5rem;
}
</style>