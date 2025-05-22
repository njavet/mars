<template>
  <div class="binary-matrix">
    <div
        v-for="item in [
            {key: 'complete', label: 'Complete'},
            {key: 'irrelevant', label: 'Irrelevant'},
            {key: 'concise', label: 'Concise'}
             ]"
        :key="item.key"
        class="binary-row"
    >
      <span class="label">{{ item.label }}</span>

      <label>
        <input
          type="radio"
          :name="item.key"
          :checked="local[item.key] === 'undefined'"
          @change="setScore(item.key, 'undefined')"
          value="undefined"
          v-model="local[item.key]"
        />
        <span>Undefined</span>
      </label>

      <label>
        <input
          type="radio"
          :name="item.key"
          :checked="local[item.key] === 'yes'"
          @change="setScore(item.key, 'yes')"
          value="yes"
          v-model="local[item.key]"
        />
        <span>Yes</span>
      </label>

      <label>
        <input
            type="radio"
            :name="item.key"
            :checked="local[item.key] === 'no'"
            @change="setScore(item.key, 'no')"
            value="no"
            v-model="local[item.key]"
        />
        <span>No</span>
      </label>
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
  border: 2px solid #747bff;
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
