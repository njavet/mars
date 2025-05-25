<template>
  <div class="binary-matrix">
    <div
        v-for="item in items"
        :key="item.key"
        class="binary-row">
      <label class="label">{{ item.label }}</label>
      <div class="radio-group">
        <label v-for="option in options" :key="option.value">
          <input
            type="radio"
            :name="item.key"
            :checked="currentScores[item.key] === option.value"
            :value="option.value"
            @change="handleScoreUpdate(option.key, option.value)"/>
          <span>{{ option.label }}</span>
        </label>
        </div>
    </div>
    <button class="save-button" @click="saveAllScores">Save</button>
  </div>
</template>

<script setup>
import {computed, onMounted, reactive, ref, watch} from 'vue'
import { useEvalSettingState } from '../composables/useState.js'
import {endpoints} from '../js/endpoints.js'
import {loadScores} from "../js/utils.js";
const {
  runs,
  selectedRun,
  evalDocs,
  evalModels,
  selectedEvalModel,
  selectedFile,
} = useEvalSettingState()

const scoresByContext = reactive({})
const items = [
  { key: 'complete', label: 'Complete' },
  { key: 'irrelevant', label: 'Irrelevant' },
  { key: 'concise', label: 'Concise' },
]

const options = [
  { value: 'undefined', label: 'Undefined' },
  { value: 'yes', label: 'Yes' },
  { value: 'no', label: 'No' },
]
const currentScores = computed(() => {
  if (
      selectedRun.value === null ||
      !selectedFile.value ||
      !selectedEvalModel.value) return {}
  const s = scoresByContext[selectedRun.value]?.[selectedFile.value]?.[selectedEvalModel.value]
  return s || {}
})

function handleScoreUpdate (key, val) {
  const run = selectedRun.value
  const file = selectedFile.value
  const lm = selectedEvalModel.value
  if (!scoresByContext[run]) scoresByContext[run] = {}
  if (!scoresByContext[run][file]) scoresByContext[run][file] = {}
  if (!scoresByContext[run][file][lm]) scoresByContext[run][file][lm] = {}
  scoresByContext[run][file][lm][key] = val
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
}, { immediate: true })
</script>

<style scoped>
.binary-matrix {
  display: flex;
  flex-direction: column;
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
