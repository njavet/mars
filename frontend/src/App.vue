<template>
  <div class="app-container">
    <Sidebar
        :selectedView="selectedView"
        @view-selected="goToView"
        v-model:selectedServer="selectedServer"
        v-model:servers="servers"
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
const selectedServer = ref('http://localhost:11434')
const servers = ref([])
const selectedLM = ref('')
const selectedSystemMessage = ref('')

function goToView(viewName) {
  router.push({ name: viewName})
}

onMounted(async() => {
  const res = await fetch('/api/servers')
  const raw = await res.json()
  servers.value = raw.servers
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