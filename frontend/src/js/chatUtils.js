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
      tab: currentTab
    })

    const formData = new FormData()
    formData.append('file', file)
    formData.append('base_url', props.base_url)
    formData.append('lm_name', props.lm_name)
    formData.append('system_message', props.system_message)

    const endpoint = getEndpoint(currentTab, true)
    const res = await fetch(endpoint, {
      method: 'POST',
      body: formData
    })

    const data = await res.json()
    loading.value = false
    messages.value.push({
      role: 'Bot',
      text: data.response || 'Error processing document.',
      tab: currentTab
    })
}

export const tabs = [
  {key: 'base', label: 'Base'},
  {key: 'agentic_base', label: 'Agentic Base'},
  {key: 'rag', label: 'RAG'},
  {key: 'agentic_rag', label: 'Agentic RAG'}
]

export function getEndpoint(currentTab, isDoc=false) {
  let url
  if (currentTab === 'base') {
    url = '/api/baseline/base'
  } else if (currentTab === 'rag') {
    url = '/api/baseline/rag'
  } else if (currentTab === 'agentic') {
    url = '/api/agentic/base'
  } else if (currentTab === 'agentic_rag') {
    url =  '/api/agentic/rag'
  }
  if (isDoc) {
    return url + '-docx'
  } else {
    return url
  }
}
