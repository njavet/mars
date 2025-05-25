<template>
  <div class="eval-settings-container">
    <h3>Settings</h3>

    <label>Run</label>
    <select class="select" v-model="selectedRun">
      <option disabled value="">Select a Run</option>
      <option v-for="run in runs" :key="run" :value="run">
        {{ run }}
      </option>
    </select>

    <label>File</label>
    <select class="select" v-model="selectedFile">
      <option disabled value="">Select a File</option>
      <option v-for="entry in evalDocs"
              :key="entry.filename"
              :value="entry.filename">
        {{ entry.filename }}
      </option>
    </select>

    <label>Model</label>
    <select class="select" v-model="selectedEvalModel">
      <option disabled value="">Select a Model</option>
      <option v-for="lm in evalModels"
              :key="lm"
              :value="lm">
        {{ lm }}
      </option>
    </select>
  </div>
  <div class="eval-container">
    <h3>Evaluation</h3>
    <ScoreOptions
        :scores="currentScores"
        @update:scores="handleScoreUpdate"
    />
    <button class="save-button" @click="saveAllScores">Save</button>

  </div>
</template>

<script setup>
import {computed, onMounted, reactive, watch} from 'vue'
import { useEvalState} from '../composables/useState.js'
import {fetchRuns, loadFileDataForRun, loadScores} from '../js/utils.js'
import {endpoints} from "../js/endpoints.js";
import ScoreOptions from "./ScoreOptions.vue";
const scoresByContext = reactive({})
const {
  runs,
  selectedRun,
  evalDocs,
  evalModels,
  evalSystemMessage,
  selectedEvalDoc,
  selectedEvalModel,
  selectedFile,
  selectedOutput,
} = useEvalState()

const currentScores = computed(() => {
  if (
      selectedRun.value === null ||
      !selectedFile.value ||
      !selectedEvalModel.value) return {}
  const s = scoresByContext[selectedRun.value]?.[selectedFile.value]?.[selectedEvalModel.value]
  return s ? { ...s} : {}
})

onMounted(async () => {
  runs.value = await fetchRuns()
  selectedRun.value = runs.value.length > 0 ? runs.value.length - 1 : null
  if (selectedRun.value != null) {
    evalDocs.value = await loadFileDataForRun(selectedRun.value)
    selectedFile.value = evalDocs.value[0]?.filename ?? null
    selectedEvalModel.value = Object.keys(evalDocs.value[0]?.models ?? {})[0] ?? null
    const scores = await loadScores(selectedRun.value)
    scoresByContext[selectedRun.value] ??= {}
    for (const scoreEntry of scores) {
      scoresByContext[selectedRun.value][scoreEntry.filename] ??= {}
      scoresByContext[selectedRun.value][scoreEntry.filename][scoreEntry.model_name] ??= {}
      for (const [key, value] of Object.entries(scoreEntry.scores)) {
        scoresByContext[selectedRun.value][scoreEntry.filename][scoreEntry.model_name][key] = value
      }
    }
  }
})

watch(selectedRun, async(run) => {
  evalDocs.value = await loadFileDataForRun(run)
}, {immediate: true})

function handleScoreUpdate (val) {
  console.log('handle update', val)
  const run = selectedRun.value
  const file = selectedFile.value
  const lm = selectedEvalModel.value
  if (!scoresByContext[run]) scoresByContext[run] = {}
  if (!scoresByContext[run][file]) scoresByContext[run][file] = {}
  scoresByContext[run][file][lm] = { ...val }
}

async function saveAllScores(run) {
  const payload = []

  for (const file in scoresByContext[run]) {
    for (const lm in scoresByContext[run][file]) {
      const scores = scoresByContext[run][file][lm]
      payload.push({
        run: Number(run),
        filename: file,
        model_name: lm,
        scores: scores
      })
    }
  }
  try {
    const url = endpoints.saveSores + `/${run}`
    const res = await fetch(url, {
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
.eval-settings-container {
  display: flex;
  flex-direction: column;
  padding-bottom: 1rem;
  gap: 1rem;
}
.eval-container {
  display: flex;
  flex-direction: column;
  margin-top: 1rem;
  border-top: 1px solid gray;
}

.save-button {
  max-width: 128px;
  border: 1px solid grey;
  border-radius: 6px;
  background-color: #222;
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

.select {
  width: 100%;
}
</style>