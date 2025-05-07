<template>
  <div class="binary-matrix">
    <div
        v-for="(label, key) in ['complete', 'irrelevant', 'concise']"
        :key="key"
        class="binary-row"
    >
      <span class="label">{{ label }}</span>

      <label>
        <input
          type="radio"
          :name="key"
          value="undefined"
          v-model="scores[key]"
        />
        <span>Undefined</span>
      </label>

      <label>
        <input
          type="radio"
          :name="key"
          value="yes"
          v-model="scores[key]"
        />
        <span>Yes</span>
      </label>

      <label>
        <input
            type="radio"
            :name="key"
            value="no"
            v-model="scores[key]"
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
