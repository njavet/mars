<template>
  <div class="selector-container">
    <label>
      <span>Select run:</span>
      <select v-model="selectedRun">
        <option v-for="run in runs" :key="run" :value="run">
          {{ run }}
        </option>
      </select>
    </label>

    <label v-if="entries.length > 0">
      <span>Select file:</span>
      <select v-model="selectedFile">
        <option v-for="entry in entries"
                :key="entry.filename"
                :value="entry.filename">
          {{ entry.filename }}
        </option>
      </select>
    </label>

    <label v-if="lmOptions.length > 0">
      <span>Select model:</span>
      <select v-model="selectedLM">
        <option v-for="lm in lmOptions"
                :key="lm"
                :value="lm">
          {{ lm }}
        </option>
      </select>
    </label>
  </div>

  <ScoreOptions v-model:scores="currentScores"/>
  <button @click="saveAllScores">Save</button>
  <div v-if="selectedEntry" class="output-display">
      <ScoreChart v-if="selectedEntry.scores" :scores="selectedEntry.scores"/>
      <strong>System Message:</strong>
      <pre>{{ systemMessage }}</pre>
      <strong>Output:</strong>
      <pre>{{ selectedOutput }}</pre>
  </div>
</template>

<script setup>
import {reactive, onMounted, ref, computed, watch} from 'vue'
import ScoreChart from "./ScoreChart.vue";
import ScoreOptions from "./ScoreOptions.vue";

const runs = ref([])
const selectedRun = ref(0)
const entries = ref([])
const selectedFile = ref(null)
const selectedLM = ref(null)
const scoresByContext = reactive({})

const selectedEntry = computed(() => {
  if (selectedFile.value== null) return null
  return entries.value.find(e => e.filename === selectedFile.value) || null
})

const lmOptions = computed(() => {
  if (!selectedEntry.value) return []
  return Object.keys(selectedEntry.value?.lms) || []
})

const systemMessage = computed(() => {
  return selectedEntry.value?.system_message || ''
})

const selectedOutput = computed(() => {
  return selectedEntry.value?.lms?.[selectedLM.value] ?? ''
})

onMounted(async () => {
  const res = await fetch('/api/runs')
  runs.value = await res.json()
  selectedRun.value = runs.value.length - 1 ?? 0
})

watch(selectedRun, loadFileDataForRun, { immediate: true})
watch([selectedRun, selectedFile, selectedLM], ([run, file, lm]) => {
  if (run == null || !file || !lm) return

  scoresByContext[run] ??= {}
  scoresByContext[run][file] ??= {}
  scoresByContext[run][file][lm] ??= {
    complete: 'undefined',
    irrelevant: 'undefined',
    concise: 'undefined'
  }
}, { immediate: true })

async function loadFileDataForRun(run) {
  console.log('loading files for', run)
  const res = await fetch(`/api/results/${run}`)
  const data = await res.json()
  entries.value = data
  selectedFile.value = data[0]?.filename ?? null
}

const currentScores = computed(() => {
  if (
      selectedRun.value === null ||
      !selectedFile.value ||
      !selectedLM.value) return {}
  console.log('current scores')
  return scoresByContext[selectedRun.value]?.[selectedFile.value]?.[selectedLM.value] || {}
})

function hasUnanswered(scores) {
  return Object.values(scores).some(
      v => v === 'undefined' || v === '' || v == null
  )
}

async function saveAllScores() {
  const run = selectedRun.value
  console.log('run', run)
  console.log(scoresByContext[run])
  const payload = []
  const missing = []

  for (const file in scoresByContext[run]) {
    for (const lm in scoresByContext[run][file]) {
      const scores = scoresByContext[run][file][lm]
      console.log('file', file, 'lm', lm)
      if (hasUnanswered(scores)) {
        missing.push({ run, file, lm})
        console.log('run', 'file', run, file, 'lm', lm)
        continue
      }
      payload.push({
        run: Number(run),
        filename: file,
        lm_name: lm,
        scores: scores
      })
    }
  }
  if (missing.length > 0) {
    alert(`Please answer all questions before saving.\nMissing: ${missing.length} entries.`)
    console.warn('Unanswered entries:', missing)
    return
  }
  try {
    const res = await fetch('/api/save-scores', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!res.ok) throw new Error('Failed to save')
    alert('Scores saved!')
  } catch (err) {
    console.error(err)
    alert('Error saving scores')
  }
}
</script>

<style scoped>
.selector-container {
  display: flex;
  flex-direction: column;
  text-align: left;
  gap: 1rem;
  max-width: 600px;
  margin: 1rem;
}

.selector-container label {
  display: flex;
}

.selector-container label span {
  display: inline-block;
  width: 120px;
  font-weight: bold;
}

.selector-container select {
  flex: 1;
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
  max-width: 80%;
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