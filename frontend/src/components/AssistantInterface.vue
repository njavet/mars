<template>
  <div class="right-sidebar">
    <div class="upload-area">
        <label for="upload" class="sidebar-button">Upload Document</label>
        <input
            id="upload"
            type="file"
            accept=".docx"
            @change="emit('file-upload', $event)"
            :disabled="!props.lm_name"
            hidden/>
      </div>
    <button class="sidebar-button" @click="emit('improve')">Improve</button>
    <button class="sidebar-button" @click="emit('save')">Save</button>
  </div>
</template>

<script setup>
const emit = defineEmits([
        'file-upload',
        'improve',
        'save'])

const props = defineProps({lm_name: String})
</script>

<style scoped>
.right-sidebar {
  position: fixed;
  top: 0;
  right: 0;
  width: 200px;
  height: 100vh;
  background-color: #222;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 2rem;
  gap: 1rem;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.3);
}

.sidebar-button {
  cursor: pointer;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border: 2px solid gray;
  background: #555;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
  width: 80%;
}

.sidebar-button:hover {
  background: #666;
}
</style>
