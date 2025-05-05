<template>
  <div class="evaluation-container">
    <ResponseBox
        ref="childRef"
        :lm_name="props.lm_name"
        :loading="currentLoading"
        :messages="messages" />
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import ResponseBox from "./ResponseBox.vue";

const messages = ref([])
const responseContainer = ref(null)
const props = defineProps({
  base_url: String,
  lm_name: String,
  system_message: String
})

</script>

<style scoped>
.evaluation-container {
  flex: 1;
  display: flex;
  overflow: hidden;
}


</style>
