<template>
  <ScoreOptions
      :scores="currentScores"
      @update:scores="handleScoreUpdate"
  />
  <button class="save-button" @click="saveAllScores">Save</button>
  <details class="details">
    <strong>System Message:</strong>
    <pre>{{ systemMessage }}</pre>
  </details>
  <div v-if="selectedEntry" class="output-display">
      <ScoreChart v-if="selectedEntry.scores" :scores="selectedEntry.scores"/>
      <strong>Output:</strong>
      <pre>{{ selectedOutput }}</pre>
  </div>
</template>

<script setup>
import {reactive, onMounted, ref, computed, watch} from 'vue'
import ScoreChart from "./ScoreChart.vue";
import ScoreOptions from "./ScoreOptions.vue";
import {useEvalState} from "../composables/useState.js";
const {
  runs,
  selectedRun,
  evalDocs,
  selectedEvalModel,
  selectedFile,
} = useEvalState()


const selectedOutput = computed(() => {
  return selectedEva.value?.lms?.[selectedModel.value] ?? ''
})

watch(selectedRun, loadFileDataForRun, { immediate: true})

function handleScoreUpdate (val) {
  console.log('handle update', val)
  const run = selectedRun.value
  const file = selectedFile.value
  const lm = selectedModel.value
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
  selectedModel.value = Object.keys(data[0]?.lms ?? {})[0] ?? null
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
      !selectedModel.value) return {}
  const s = scoresByContext[selectedRun.value]?.[selectedFile.value]?.[selectedModel.value]
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
.output-display {
  background: #222;
  padding: 1rem;
  border: 1px solid #747bff;
  border-radius: 6px;
  color: white;
  max-height: 80%;
  max-width: 80%;
  overflow: auto;
  margin: 8px;
  text-align: left;
}

.save-button {
  max-width: 128px;
  border: 1px solid grey;
  border-radius: 6px;
  background-color: #222;
  margin: 8px;
}

.details {
  border: 1px solid grey;
  border-radius: 6px;
  max-width: 80%;
  padding: 1rem;
  margin: 8px;
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