export function useFileUpload({ props, messages, loading }) {
  async function onFileUpload(event) {
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

async function handleFileUpload({event, props, messages}) {
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

  const res = await fetch('/api/chat/doc', {
    method: 'POST',
    body: formData
  })

  const data = await res.json()
  messages.value.push({
    role: 'Bot',
    text: data || 'Error processing document.',
  })
}
