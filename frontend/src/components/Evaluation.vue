<template>
  <div class="selector-container">
    <label>
      Select run:
      <select v-model="selectedRun">
        <option v-for="run in runs" :key="run" :value="run">
          {{ run }}
        </option>
      </select>

    </label>
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
      <div class="score-inputs">
        <div v-for="(value, key) in selectedEntry.scores" :key="key">
        <label>
          {{ key }}:
          <input
            type="number"
            v-model.number="selectedEntry.scores[key]"
            min="0"
            max="10"
            step="1"
          />
        </label>
      </div>

      </div>
      <ScoreChart v-if="selectedEntry.scores" :scores="selectedEntry.scores"/>
      <strong>Output:</strong>
      <pre>{{ selectedEntry.output}}</pre>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref, computed, watch} from 'vue'
import ScoreChart from "./ScoreChart.vue";

const runs = ref([])
const filesByRun = ref({})
const filenames = computed(() => filesByRun.value[selectedRun.value] || [])

const fileData = ref([])
const selectedFileIndex = ref(0)
const selectedLM = ref(null)
const selectedRun = ref(0)

onMounted(async () => {
  const res = await fetch('/api/runs')
  runs.value = await res.json()
  console.log('number of runs', runs.value)
  selectedRun.value = runs.value[0] ?? 0
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
watch(
  () => selectedEntry.value?.scores,
  async (scores) => {
    if (!scores) return

    await fetch('/api/save-scores', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        file: filenames.value[selectedFileIndex.value],
        lm_name: selectedEntry.value.lm_name,
        scores
      })
    })
  },
  { deep: true }
)

async function loadFileDataForRun(runIndex) {
  const files = filesByRun.value[runIndex] || []
  const results = await Promise.all(
    files.map(async name => {
      const result = await fetch(`/api/results/${run}`)
      if (!result.ok) return []
      return await result.json()
    })
  )
  fileData.value = results
  selectedFileIndex.value = 0
  selectedLM.value = results[0]?.[0]?.lm_name ?? null
}

</script>
<style scoped>
.selector-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 800px;
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