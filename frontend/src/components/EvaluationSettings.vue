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
      <option v-for="entry in entries"
              :key="entry.filename"
              :value="entry.filename">
        {{ entry.filename }}
      </option>
    </select>

    <label>Model</label>
    <select class="select" v-model="selectedEvalModel">
      <option disabled value="">Select a Model</option>
      <option v-for="lm in lmOptions"
              :key="lm"
              :value="lm">
        {{ lm }}
      </option>
    </select>
  </div>
  <div class="eval-container">
    <h3>Evaluation</h3>

  </div>
</template>

<script setup>
import { onMounted, reactive } from 'vue'
import { useEvalState} from '../composables/useState.js'
import {fetchRuns, loadFileDataForRun, loadScores} from '../js/utils.js'
const scoresByContext = reactive({})
const {
  runs,
  selectedRun,
  evalDocs,
  evalSystemMessage,
  selectedEvalModel,
  selectedFile,
  selectedOutput,
} = useEvalState()


onMounted(async () => {
  runs.value = await fetchRuns()
  selectedRun.value = runs.value.length > 0 ? runs.value.length - 1 : null
  if (selectedRun.value != null) {
    evalDocs.value = await loadFileDataForRun(selectedRun.value)
    const scores = await loadScores(selectedRun.value)
    scoresByContext[run] ??= {}
    for (const scoreEntry of data) {
      scoresByContext[run][scoreEntry.filename] ??= {}
      scoresByContext[run][scoreEntry.filename][scoreEntry.lm_name] ??= {}
      for (const [key, value] of Object.entries(scoreEntry.scores)) {
        scoresByContext[run][scoreEntry.filename][scoreEntry.lm_name][key] = value
      }
    }
  }

})
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
  padding-top: 0.5rem;
  gap: 1rem;
  border-top: 1px solid gray;
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

.select {
  width: 100%;
}

</style>