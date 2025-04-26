<template>
  <div class="right-sidebar">
    <div class="upload-area">
        <label for="upload" class="sidebar-button">Upload Document</label>
        <input
            id="upload"
            type="file"
            accept=".docx"
            @change="handleFileUpload"
            :disabled="!props.lm_name"
            hidden/>
      </div>
    <button class="sidebar-button" @click="handleImprove">Improve</button>
    <button class="sidebar-button" @click="handleSave">Save</button>
  </div>
</template>

<script setup>
const emit = defineEmits(['bot-response'])

const props = defineProps({
  base_url: String,
  lm_name: String,
  enable_rag: Boolean,
  system_message: String
})

async function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  emit('bot-response', {role: 'info', text: 'Evaluating document...'})
  const formData = new FormData()
  formData.append('file', file)
  formData.append('base_url', props.base_url)
  formData.append('lm_name', props.lm_name)
  formData.append('enable_rag', props.enable_rag)
  formData.append('system_message', props.system_message)

  const res = await fetch('/api/upload-docx', {
    method: 'POST',
    body: formData
  })
  const data = await res.json()
  emit('bot-response', {role: 'res', text: data.response || 'Error processing document'})
}

async function handleImprove(event) {
  console.log("lm name", props.lm_name)
}
async function handleSave(event) {

}
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
