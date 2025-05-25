<template>
  <div class="app-container">
    <Sidebar :selectedView="selectedView" @view-selected="goToView"/>
    <div class="main-content">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import { useAppState } from './composables/useState.js'
import {
  fetchServers,
  fetchSystemMessages,
  fetchLibs,
  fetchModels,
} from './js/utils.js'

const router = useRouter()
const route = useRoute()
const selectedView = computed(() => route.name)
const {
  libs,
  servers,
  models,
  systemMessages,
} = useAppState()

onMounted(async() => {
  const fetched = await fetchServers()
  fetched.forEach(server => {
    servers.value.push(server)
  })
  libs.value = await fetchLibs()
  models.value = await fetchModels(servers.value[0])
  systemMessages.value = await fetchSystemMessages()
})

function goToView(viewName) {
  router.push({ name: viewName})
}
</script>

<style scoped>
.app-container {
  flex: 1;
  display: flex;
  overflow: hidden;
}
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>