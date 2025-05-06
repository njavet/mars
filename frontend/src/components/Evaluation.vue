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
        <option v-for="entry in lmEntries" :key="entry.lm_name" :value="entry.lm_name">
          {{ entry.lm_name}}
        </option>
      </select>
    </label>

    <div v-if="selectedEntry" class="output-display">
      <ScoreChart v-if="selectedEntry.scores" :scores="selectedEntry.scores"/>
      <strong>Output (generate):</strong>
      <pre>{{ selectedEntry.output_generate }}</pre>

      <strong>Output (chat):</strong>
      <pre>{{ selectedEntry.output_chat }}</pre>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref, computed, watch} from 'vue'
import ScoreChart from "./ScoreChart.vue";

const filenames = ref([])
const fileData = ref([])
const selectedFileIndex = ref(0)
const selectedLM = ref(null)

onMounted(async () => {
  const res = await fetch('/api/results/file-list')
  filenames.value = await res.json()
  console.log(filenames)

  const results = await Promise.all(
    filenames.value.map(async name => {
      const result = await fetch(`/results/${name}`)
      if (!result.ok) return []
      return await result.json()
    })
  )
  fileData.value = results
  selectedLM.value = results[0]?.[0]?.lm_name ?? null
})
const lmEntries = computed(() => {
  return fileData.value[selectedFileIndex.value] || []
})

const selectedEntry = computed(() => {
  return lmEntries.value.find(e => e.lm_name === selectedLM.value) || null
})

watch(selectedFileIndex, () => {
  selectedLM.value = lmEntries.value[0]?.lm_name || null
})
</script>
<style scoped>
.selector-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 600px;
  overflow: auto;
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
  max-height: 80%;
  overflow: auto;
}
pre {
  white-space: pre-wrap;
  background: #333;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 0.5rem;
}
canvas {
  max-width: 500px;
  margin-top: 1rem;
}
</style>