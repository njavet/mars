<template>
  <Transition name="fade">
    <div v-if="loading" class="loading-overlay">
      <div class="loading-content">
        <div class="loader"></div>
        <div class="loader-wrapper">
          <div class="loader-text">Thinking{{ loaderText }}</div>
        </div>
      </div>
    </div>
  </Transition>
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

const loaderText = ref('')
let loadingInterval = null

watch(() => props.loading, (isLoading) => {
  if (isLoading) {
    startLoadingDots()
  } else {
    stopLoadingDots()
  }
})

function startLoadingDots() {
  let dots = ''
  loadingInterval = setInterval(() => {
    dots = dots.length >= 3 ? '' : dots + '.'
    loaderText.value = `${dots}`
  }, 500)
}

function stopLoadingDots() {
  clearInterval(loadingInterval)
  loaderText.value = ''
}

onUnmounted(() => {
  clearInterval(loadingInterval)
})
</script>

<style scoped>
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: calc(100% + 220px);
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.4);
  z-index: 10;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loader {
  width: 200px;
  height: 6px;
  background: linear-gradient(
    to right,
    transparent 0%,
    cyan 50%,
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

.loader-wrapper {
  width: 8ch;
  text-align: left;
}

.loader-text {
  color: cyan;
  font-size: 1.2rem;
  font-weight: bold;
  text-shadow: 0 0 5px cyan;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0.2;
}
</style>
