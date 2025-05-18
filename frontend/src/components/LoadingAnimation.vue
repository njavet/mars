<template>
  <div class="loader-container">
    <Transition name="fade">
      <div v-if="loading">
        <div class="loader"></div>
        <div class="loader-text">{{props.baseText}}{{ loaderText }}</div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'

const props = defineProps({
  loading: Boolean,
  baseText: {
    type: String,
    default: ''
  }
})

const loaderText = ref('   ')
let loadingInterval = null

watch(() => props.loading, (isLoading) => {
  if (isLoading) {
    startLoadingDots()
  } else {
    stopLoadingDots()
  }
})

function startLoadingDots() {
  let dots = 0
  loadingInterval = setInterval(() => {
    if (dots >= 3) {
      loaderText.value = '   '
      dots = 0
    } else {
      dots += 1
      loaderText.value = '.'.repeat(dots) + ' '.repeat(3 - dots)
    }
  }, 500)
}

function stopLoadingDots() {
  clearInterval(loadingInterval)
  loaderText.value = '   '
}

onUnmounted(() => {
  clearInterval(loadingInterval)
})
</script>

<style scoped>

.loader {
  width: 200px;
  height: 6px;
  background: linear-gradient(
    to right,
    transparent 0%,
    #646cff 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: knightRide 1.5s infinite linear;
  border-radius: 5px;
}

@keyframes knightRide {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.loader-text {
  color: #535bf2;
  font-size: 1.2rem;
  font-family: monospace;
  white-space: pre;
  font-weight: bold;
  text-shadow: 0 0 5px #535bf2;
}
.loader-container {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
