<template>
  <div class="app-container">
    <Sidebar
        :selectedView="selectedView"
        @view-selected="goToView"
        @file-upload="onFileUpload"
        v-model:servers="servers"
        v-model:selectedLib="selectedLib"
        v-model:selectedServer="selectedServer"
        v-model:selectedModel="selectedModel"
        v-model:selectedSystemMessage="selectedSystemMessage"
        v-model:agentic="agentic"
        v-model:selectedTools="selectedTools"
    />
    <div class="main-content">
      <RouterView v-slot="{ Component }">
        <component
            :is="Component"
            ref="childRef"
            v-bind="{
              ...(route.name === 'chatbot' || route.name === 'assistant'
              ? {
                lib: selectedLib,
                base_url: selectedServer,
                model_name: selectedModel,
                system_message: selectedSystemMessage,
                agentic: agentic,
                selected_tools: selectedTools
              } : {})
          }"
        />
      </RouterView>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Sidebar from './components/Sidebar.vue'

const router = useRouter()
const route = useRoute()

// state
const selectedView = computed(() => route.name)
const childRef = ref(null)
const selectedLib = ref('transformers')
const selectedServer = ref('http://localhost:11434')
const servers = ref(['http://localhost:11434'])
const selectedModel = ref('')
const selectedSystemMessage = ref('')
const agentic = ref(false)
const selectedTools = ref([])

function goToView(viewName) {
  router.push({ name: viewName})
}

function onFileUpload(event) {
  console.log('file upload event')
  childRef.value?.onFileUpload?.(event)
}

onMounted(async() => {
  const res = await fetch('/api/servers')
  const raw = await res.json()
  const fetched = raw.servers || []
  fetched.forEach(server => {
    servers.value.push(server)
  })
  if (!selectedServer.value && servers.value.length > 1) {
    selectedServer.value = servers.value[0]
  }
})
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