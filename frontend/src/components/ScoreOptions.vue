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
            :checked="local[item.key] === 'undefined'"
            @change="setScore(item.key, 'undefined')"
            value="option.value"
            v-model="local[item.key]"/>
          <span>{{ option.label }}</span>
        </label>
        </div>
    </div>
  </div>
</template>

<script setup>
import {ref, watch} from "vue";

const props = defineProps({
  scores: Object
})

const emit = defineEmits(['update:scores'])

const local = ref({})
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

watch(() => props.scores, newScores => {
  local.value = { ...(newScores || {})}
}, { immediate: true})

function setScore(key, val) {
  local.value = { ...local.value, [key]: val}
  console.log('emit update score')
  emit('update:scores', { ...local.value})
}

</script>

<style scoped>
.binary-matrix {
  display: flex;
  flex-direction: column;
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
</style>
