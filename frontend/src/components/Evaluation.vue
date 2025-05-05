<template>
  <div class="tabs-container">
    <div class="tab-bar">
      <button
        v-for="(file, i) in filenames"
        :key="file"
        :class="{ active: currentTab === i}"
        @click="currentTab = i">
        {{ file }}
      </button>
    </div>
    <div class="tab-content" v-if="dataList[currentTab]">
      <div><strong>lm_name:</strong>{{ dataList[currentTab].lm_name}}</div>
      <div><strong>output:</strong></div>
      <pre>{{ dataList[currentTab].output }}</pre>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'

const dataList = ref([])
const currentTab = ref(0)
const filenames = ref([])

onMounted(async () => {
  const res = await fetch('/api/results/file-list')
  filenames.value = await res.json()
  const promises = filenames.value.map(name =>
      fetch (`/results/${name}`).then(res => res.json())
  )
  dataList.value = await Promise.all(promises)
})
</script>
<style scoped>
.tab-bar {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.tab-bar button {
  padding: 0.5rem 1rem;
  border: none;
  background: #444;
  color: white;
  cursor: pointer;
  border-radius: 4px;
}
.tab-bar button.active {
  background: cyan;
  color: black;
}
.tab-content {
  background: #222;
  color: white;
  padding: 1rem;
  border: 1px solid cyan;
  border-radius: 6px;
}
pre {
  white-space: pre-wrap;
  background: #333;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 0.5rem;
}
</style>
