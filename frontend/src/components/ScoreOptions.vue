<template>
  <div class="binary-matrix">
<div v-for="(label, key) in ['complete', 'irrelevant', 'concise']" :key="key">
  <span>{{ label }}</span>
  <label>
    <input
      type="radio"
      :name="label"
      value="yes"
      v-model="scores[label]"
    /> Yes
  </label>
  <label>
    <input
      type="radio"
      :name="label"
      value="no"
      v-model="scores[label]"
    /> No
  </label>
</div>


  </div>
</template>

<script setup>
import { reactive } from 'vue'
const scores = defineModel('scores')
// TODO fetch from backend
const categories = ['complete', 'irrelevant', 'concise']
const selections = reactive({
  complete: null,
  irrelevant: null,
  concise: null
})
</script>

<style scoped>
.binary-matrix {
  display: flex;
  border: 2px solid #6312ff;
  flex-direction: column;
  padding: 1rem;
  gap: 0.5rem;
}
.binary-row {
  display: flex;
  align-items: center;
  text-align: left;
  gap: 1rem;
}
.label {
  width: 100px;
  font-weight: bold;
}
</style>
