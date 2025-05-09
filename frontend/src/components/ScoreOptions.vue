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
          value="undefined"
          v-model="scores[item.key]"
        />
        <span>Undefined</span>
      </label>

      <label>
        <input
          type="radio"
          :name="item.key"
          value="yes"
          v-model="scores[item.key]"
        />
        <span>Yes</span>
      </label>

      <label>
        <input
            type="radio"
            :name="item.key"
            value="no"
            v-model="scores[item.key]"
        />
        <span>No</span>
      </label>
    </div>
  </div>
</template>

<script setup>
const scores = defineModel('scores')
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
