<template>
  <div class="app-container">
    <Sidebar
        :selectedView="selectedView"
        :servers="servers"
        @view-selected="goToView"
        @file-upload="onFileUpload"
        v-model:selectedServer="selectedServer"
        v-model:selectedLM="selectedLM"
        v-model:selectedSystemMessage="selectedSystemMessage"
    />
    <div class="main-content">
      <RouterView v-slot="{ Component }">
        <component
            :is="Component"
            ref="childRef"
            :base_url="selectedServer"
            :lm_name="selectedLM"
            :system_message="selectedSystemMessage"
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
const selectedServer = ref('http://localhost:11434')
const servers = ref(['http://localhost:11434'])
const selectedLM = ref('')
const selectedSystemMessage = ref('')

function goToView(viewName) {
  router.push({ name: viewName})
}

function onFileUpload(event) {
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