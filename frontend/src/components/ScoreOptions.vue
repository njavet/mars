<template>
  <div class="binary-matrix">
    <div
        v-for="item in items"
        :key="item.key"
        class="binary-row">
      <label class="label">{{ item.label }}</label>
      <div class="radio-group">
        <input
          type="number"
          :name="item.key"
          :value="getScore(item.key)"
          @input="updateScore(item.key, $event.target.value)"/>
      </div>
    </div>
    <button class="save-button" @click="saveAllScores">Save</button>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { useEvalSettingState } from '../composables/useState.js'
import {endpoints} from '../js/endpoints.js'
import {loadScores} from '../js/utils.js'
const {
  runs,
  selectedRun,
  evalDocs,
  evalModels,
  selectedEvalModel,
  selectedFile,
} = useEvalSettingState()

const scoresByContext = reactive({})
const currentScores = ref({})

const items = [
  { key: 'true_positives', label: 'True Positives' },
  { key: 'false_positives', label: 'False Positives' },
  { key: 'true_negatives', label: 'True Negatives' },
  { key: 'false_negatives', label: 'False Negatives' },
  { key: 'irrelevant', label: 'Irrelevant' },
  { key: 'concise', label: 'Concise' },
  { key: 'missing', label: 'Missing' },
]

function getScore(key) {
  const run = selectedRun.value
  const file = selectedFile.value
  const model = selectedEvalModel.value
  return scoresByContext?.[run]?.[file]?.[model]?.[key] ?? ''
}

function updateScore(key, value) {
  const run = selectedRun.value
  const file = selectedFile.value
  const model = selectedEvalModel.value
  if (!scoresByContext[run]) scoresByContext[run] = {}
  if (!scoresByContext[run][file]) scoresByContext[run][file] = {}
  if (!scoresByContext[run][file][model]) scoresByContext[run][file][model] = {}
  scoresByContext[run][file][model][key] = Number(value)
}

async function saveAllScores() {
  const run = selectedRun.value
  console.log('run', run)
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
    console.log('payload', payload)
    console.log('payload', JSON.stringify(payload, null, 2))
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

watch(selectedRun, async (run) => {
  if (run == null) return
  const scores = await loadScores(run)
  scoresByContext[run] ??= {}

  for (const scoreEntry of scores) {
    scoresByContext[run][scoreEntry.filename] ??= {}
    scoresByContext[run][scoreEntry.filename][scoreEntry.model_name] ??= {}

    for (const [key, value] of Object.entries(scoreEntry.scores)) {
      scoresByContext[run][scoreEntry.filename][scoreEntry.model_name][key] = value
    }
  }
  const s = scoresByContext[run]?.[selectedFile.value]?.[selectedEvalModel.value]
  currentScores.value = s || {}
}, { immediate: true })
</script>

<style scoped>
.binary-matrix {
  display: flex;
  flex-direction: column;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid grey;
}
.binary-row {
  margin-bottom: 0.5rem;
}
.radio-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.25rem;
}
.label {
  width: 100px;
  font-weight: bold;
}
.save-button {
  border: 1px solid grey;
  border-radius: 6px;
  background-color: #222;
  margin: 8px;
}
</style>
