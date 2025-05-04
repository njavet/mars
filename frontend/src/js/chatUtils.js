export async function handleFileUpload({
                                         event,
                                         props,
                                         messages,
                                         currentTab,
}) {
  const file = event.target.files[0]
    if (!file) return
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

export function getEndpoint(currentTab, isDoc= false) {
  const map = {
    base: '/api/baseline/base',
    rag: '/api/baseline/rag',
    agentic: '/api/agentic/base',
    agentic_rag: '/api/agentic/rag',
  }
  const baseUrl = map[currentTab]
  if (!baseUrl) throw new Error(`Unknown tab: ${currentTab}`)
  return isDoc ? `${baseUrl}-docx` : baseUrl
}
