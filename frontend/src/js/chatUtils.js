export function useFileUpload({ childRef, messages, loading, props }) {
  async function onFileUpload(event) {
    const tab = childRef.value?.currentTab
    if (!tab) return

    loading.value = true
    try {
      await handleFileUpload({
        event,
        props,
        messages,
      })
    } finally {
      loading.value = false
    }
  }

  return { onFileUpload }
}

async function handleFileUpload({
                                         event,
                                         props,
                                         messages,
}) {
  const file = event.target.files[0]
    if (!file) return

  const ext = file.name.split('.').pop().toLowerCase()
  const isDocx = ext === 'docx'
  const isTxt = ext === 'txt'
  let fileType = null
  if (isDocx) fileType = 'docx'
  else if (isTxt) fileType = 'txt'

  if (isTxt) {
  const reader = new FileReader()
  reader.onload = () => {
    const content = reader.result
    messages.value.push({
      role: 'User',
      text: content,
    })
  }
  reader.readAsText(file)
} else {
  messages.value.push({
    role: 'User',
    text: `[Sent ${isDocx ? 'DOCX' : 'Unknown'}: ${file.name}]`,
  })
}

  const formData = new FormData()
  formData.append('file', file)
  formData.append('base_url', props.base_url)
  formData.append('lm_name', props.lm_name)
  formData.append('system_message', props.system_message)

  const endpoint = getEndpoint(currentTab, fileType)
  const res = await fetch(endpoint, {
    method: 'POST',
    body: formData
  })

  const data = await res.json()
  messages.value.push({
    role: 'Bot',
    text: data.response || 'Error processing document.',
  })
}

export function getEndpoint(currentTab, fileType= null) {
  const map = {
    base: '/api/baseline/base',
    rag: '/api/baseline/rag',
    agentic: '/api/agentic/base',
    agentic_rag: '/api/agentic/rag',
  }
  const baseUrl = map[currentTab]
  if (!baseUrl) throw new Error(`Unknown tab: ${currentTab}`)
  if (fileType === 'docx') return `${baseUrl}-docx`
  if (fileType === 'txt') return `${baseUrl}-text`
  return baseUrl

}
