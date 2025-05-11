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

  <ScoreOptions
      :scores="currentScores"
      @update:scores="handleScoreUpdate"
  />
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
import {reactive, onMounted, ref, computed, watch, watchEffect} from 'vue'
import ScoreChart from "./ScoreChart.vue";
import ScoreOptions from "./ScoreOptions.vue";

const runs = ref([])
const selectedRun = ref(null)
const entries = ref([])
const selectedLM = ref(null)
const scoresByContext = reactive({})
const selectedFile = ref(null)

const selectedEntry = computed(() => {
  return entries.value.find(e => e?.filename === selectedFile.value) || null
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
  selectedRun.value = runs.value.length > 0 ? runs.value.length - 1 : null
  if (selectedRun.value != null) {
    await loadFileDataForRun(selectedRun.value)
    await loadScores(selectedRun.value)
    console.log('scores and files are loaded for', selectedRun.value)
  }
})

watch(selectedRun, loadFileDataForRun, { immediate: true})

function handleScoreUpdate (val) {
  console.log('handle update', val)
  const run = selectedRun.value
  const file = selectedFile.value
  const lm = selectedLM.value
  if (!scoresByContext[run]) scoresByContext[run] = {}
  if (!scoresByContext[run][file]) scoresByContext[run][file] = {}
  scoresByContext[run][file][lm] = { ...val }
}

async function loadFileDataForRun(run) {
  if (run == null) return
  console.log('loading files for', run)
  const res = await fetch(`/api/results/${run}`)
  const data = await res.json()
  entries.value = data
  selectedFile.value = data[0]?.filename ?? null
  selectedLM.value = Object.keys(data[0]?.lms ?? {})[0] ?? null
}

async function loadScores(run) {
  if (run == null) return
  const res = await fetch(`/api/fetch-scores/${run}`)
  const data = await res.json()

  scoresByContext[run] ??= {}
  for (const scoreEntry of data) {
    scoresByContext[run][scoreEntry.filename] ??= {}
    scoresByContext[run][scoreEntry.filename][scoreEntry.lm_name] ??= {}
    for (const [key, value] of Object.entries(scoreEntry.scores)) {
      scoresByContext[run][scoreEntry.filename][scoreEntry.lm_name][key] = value
    }
  }
}

const currentScores = computed(() => {
  if (
      selectedRun.value === null ||
      !selectedFile.value ||
      !selectedLM.value) return {}
  const s = scoresByContext[selectedRun.value]?.[selectedFile.value]?.[selectedLM.value]
  return s ? { ...s} : {}
})

function hasUnanswered(scores) {
  return Object.values(scores).some(
      v => v === 'undefined' || v === '' || v == null
  )
}

async function saveAllScores() {
  const run = selectedRun.value
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
    const res = await fetch(`/api/save-scores/${run}`, {
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