<template>
  <details class="details">
    <strong>System Message:</strong>
    <pre>{{ evalSystemMessage }}</pre>
  </details>
  <div v-if="selectedEvalDoc" class="output-display">
      <ScoreChart v-if="selectedEvalDoc.scores" :scores="selectedEvalDoc.scores"/>
      <strong>Output:</strong>
      <pre>{{ selectedOutput }}</pre>
  </div>
</template>

<script setup>
import ScoreChart from './ScoreChart.vue'
import { useEvalState } from '../composables/useState.js'
const {
  runs,
  selectedRun,
  evalDocs,
  evalModels,
  evalSystemMessage,
  selectedEvalDoc,
  selectedEvalModel,
  selectedFile,
  selectedOutput
} = useEvalState()

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