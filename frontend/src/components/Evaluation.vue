<template>
  <div class="evaluation-container">
    <ResponseBox
        ref="childRef"
        :lm_name="props.lm_name"
        :loading="false"
        :messages="messages" />
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import ResponseBox from "./ResponseBox.vue";

const childRef = ref(null)

onMounted(async () => {
  const promises = files.map(f => )
})
</script>

<style scoped>
.evaluation-container {
  flex: 1;
  display: flex;
  overflow: hidden;
}


</style>
