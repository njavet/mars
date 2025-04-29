import { nextTick } from 'vue'

export function scrollToBottom(chatContainer) {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

export async function handleFileUpload({
                                         event,
                                         props,
                                         messages,
                                         currentTab,
                                         loading,
                                         chatContainer
}) {
  const file = event.target.files[0]
    if (!file) return
    loading.value = true

    messages.value.push({ role: 'User', text: `[Sent DOCX: ${file.name}]`, tab: currentTab.value })
    scrollToBottom(chatContainer)

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
    scrollToBottom(chatContainer)
}

export const tabs = [
  {key: 'base', label: 'Base'},
  {key: 'agentic_base', label: 'Agentic Base'},
  {key: 'rag', label: 'RAG'},
  {key: 'agentic_rag', label: 'Agentic RAG'}
]
