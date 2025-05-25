<template>
  <div class="app-container">
    <Sidebar :selectedView="selectedView" @view-selected="goToView"/>

    <div class="main-content">
      <RouterView v-slot="{ Component }">
        <component
            :is="Component"
            ref="childRef"
            v-bind="{
              ...(route.name === 'chatbot'
              ? {
                lib: selectedLib,
                base_url: selectedServer,
                model_name: selectedModel,
                system_message: selectedSystemMessage,
                agentic: agentic,
              } : {})
          }"
        />
      </RouterView>
    </div>
  </div>
</template>

<script setup>
import {computed, onMounted, watch} from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import { useAppState } from './composables/useAppState.js'

const router = useRouter()
const route = useRoute()
const selectedView = computed(() => route.name)
const {
  libs,
  selectedLib,
  servers,
  selectedServer,
  models,
  selectedModel,
  systemMessages,
  selectedSystemMessage,
  agentic
} = useAppState()

function goToView(viewName) {
  router.push({ name: viewName})
}

async function fetchServers() {
  const res = await fetch('/api/servers')
  const raw = await res.json()
  return raw.servers || []
}

async function fetchModels() {
  const server = selectedServer.value
  console.log('fetch models from', server)
  try {
    const res = await fetch(`/api/lms?base_url=${server}`)
    models.value = await res.json()
    if (models.value.length > 0 && !selectedModel.value) {
      selectedModel.value = models.value[0]
    }
  } catch(err) {
    console.warn('Failed to fetch config', err)
    models.value = []
  }
}

async function fetchSystemMessages() {
  const res = await fetch('/api/system-messages')
  const raw = await res.json()
  systemMessages.value = raw
  if (systemMessages.value.length > 0 && !selectedSystemMessage.value) {
    selectedSystemMessage.value = raw[0].text
  }
}

onMounted(async() => {
  const fetched = await fetchServers()
  fetched.forEach(server => {
    servers.value.push(server)
  })
  if (!selectedServer.value && servers.value.length > 1) {
    selectedServer.value = servers.value[0]
  }
  await fetchModels()
  await fetchSystemMessages()
})

watch(selectedServer, fetchModels, {immediate: true})


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