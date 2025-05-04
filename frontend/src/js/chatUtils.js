export async function handleFileUpload({
                                         event,
                                         props,
                                         messages,
                                         currentTab,
                                         loading,
}) {
  const file = event.target.files[0]
    if (!file) return
    loading.value = true
    messages.value.push({
      role: 'User',
      text: `[Sent DOCX: ${file.name}]`,
      tab: currentTab.value
    })

    const formData = new FormData()
    formData.append('file', file)
    formData.append('base_url', props.base_url)
    formData.append('lm_name', props.lm_name)
    formData.append('enable_rag', enableRag(currentTab.value))
    formData.append('system_message', props.system_message)

    const endpoint = fetch_endpoint(currentTab.value) + '/upload-docx'
    const res = await fetch(endpoint, {
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
}

export const tabs = [
  {key: 'base', label: 'Base'},
  {key: 'agentic_base', label: 'Agentic Base'},
  {key: 'rag', label: 'RAG'},
  {key: 'agentic_rag', label: 'Agentic RAG'}
]

export function enableRag(currentTab) {
  return currentTab === 'rag' || currentTab === 'agentic_rag'
}

export function fetch_endpoint(currentTab) {
  if (currentTab === 'agentic' || currentTab === 'agentic_rag') {
    return '/api/agentic'
  } else {
    return '/api/baseline'
  }
}
