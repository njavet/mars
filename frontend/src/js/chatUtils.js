import { nextTick } from 'vue'

export function chatUtils({ props, messages, currentTab, chatContainer, loading }) {
  function scrollToBottom() {
      nextTick(() => {
      if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight
      }
    })
  }

  async function handleFileUpload(event) {
    const file = event.target.files[0]
    if (!file) return
    loading.value = true

    messages.value.push({ role: 'User', text: `[Sent DOCX: ${file.name}]`, tab: currentTab.value })
    scrollToBottom()

    const formData = new FormData()
    formData.append('file', file)
    formData.append('base_url', props.base_url)
    formData.append('lm_name', props.lm_name)
    formData.append('agent_type', currentTab.value)
    formData.append('system_message', props.system_message)

    const res = await fetch('/api/upload-docx', {
      method: 'POST',
      body: formData
    })

    const data = await res.json()
    loading.value = false
    messages.value.push({
      role: 'Bot',
      text: data.response || 'Error processing document.',
      tab: currentTab.value
    })
    scrollToBottom()
  }

  return { scrollToBottom, handleFileUpload }
}