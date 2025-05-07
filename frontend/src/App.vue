<template>
  <div class="app-container">
    <Sidebar
        :selectedView="selectedView"
        :servers="servers"
        @view-selected="goToView"
        @file-upload="handleFileUpload"
        v-model:selectedServer="selectedServer"
        v-model:selectedLM="selectedLM"
        v-model:selectedSystemMessage="selectedSystemMessage"
    />
    <div class="main-content">
      <RouterView v-slot="{ Component }">
        <component
            :is="Component"
            :base_url="selectedServer"
            :lm_name="selectedLM"
            :system_message="selectedSystemMessage"
            :onFileUpload="handleFileUpload"
        />
      </RouterView>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import {handleFileUpload} from "./js/chatUtils.js";

const router = useRouter()
const route = useRoute()
// state
const selectedView = computed(() => route.name)
const selectedServer = ref('http://localhost:11434')
const servers = ref(['http://localhost:11434'])
const selectedLM = ref('')
const selectedSystemMessage = ref('')

function goToView(viewName) {
  router.push({ name: viewName})
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