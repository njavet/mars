<template>
  <div class="sidebar">
    <div class="nav-container">
      <h3>Navigation</h3>
      <label v-for="option in views" :key="option.value" class="nav-option">
        <input
          type="radio"
          name="nav"
          :value="option.value"
          v-model="selectedView"
          @change="onSelectView"
        />
        {{ option.label }}
      </label>
    </div>

    <div v-if="selectedView === 'chatbot'">
      <BotSettings/>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { views } from '../composables/useAppState.js'
import BotSettings from './BotSettings.vue'
const emit = defineEmits(['view-selected'])

const selectedView = ref('home')

function onSelectView(event) {
  emit('view-selected', selectedView.value)
}

</script>

<style scoped>
.sidebar {
  width: 220px;
  flex-shrink: 0;
  background-color: #1f1f1f;
  color: white;
  padding: 1rem;
  box-sizing: border-box;
  border-right: 1px solid gray;
  text-align: left;
  overflow: auto;
}

.nav-container {
  padding: 0.5rem 0;
  border-top: 1px solid gray;
  border-bottom: 1px solid gray;
}

.nav-option {
  display: block;
  margin-bottom: 1rem;
  color: white;
}

input[type="radio"] {
  margin-right: 0.5rem;
}
</style>
