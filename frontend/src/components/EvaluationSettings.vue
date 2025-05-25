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
        v-if="selectedRun !== null && selectedFile && selectedEvalModel"
    />
  </div>
</template>

<script setup>
import {onMounted, watch} from 'vue'
import {useEvalSettingState } from '../composables/useState.js'
import {fetchRuns, loadFileDataForRun, loadScores} from '../js/utils.js'
import ScoreOptions from "./ScoreOptions.vue";
const {
  runs,
  selectedRun,
  evalDocs,
  evalModels,
  selectedEvalModel,
  selectedFile,
} = useEvalSettingState()

onMounted(async () => {
  runs.value = await fetchRuns()
  if (runs.value.length > 0) {
    selectedRun.value = runs.value.length - 1
    evalDocs.value = await loadFileDataForRun(selectedRun.value)
    selectedFile.value = evalDocs.value[0]?.filename ?? null
    selectedEvalModel.value = Object.keys(evalDocs.value[0]?.models ?? {})[0] ?? null
  }
})

watch(selectedRun, async(run) => {
  evalDocs.value = await loadFileDataForRun(run)
}, {immediate: true})
</script>

<style scoped>
.eval-settings-container {
  display: flex;
  flex-direction: column;
  padding-bottom: 0.5rem;
  gap: 0.5rem;
}
.eval-container {
  display: flex;
  flex-direction: column;
  margin-top: 1rem;
  border-top: 1px solid gray;
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