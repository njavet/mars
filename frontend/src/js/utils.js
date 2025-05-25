import { endpoints } from './endpoints.js'

export async function fetchServers() {
  const res = await fetch(endpoints.servers)
  const raw = await res.json()
  return raw.servers || []
}

export async function fetchModels(server) {
  try {
      const url = endpoints.models + `?base_url=${server}`
      const res = await fetch(url)
      return await res.json()
  } catch (err) {
    console.warn('Failed to fetch models', err)
    return []
  }
}

export async function fetchSystemMessages() {
  const res = await fetch(endpoints.systemMessages)
  const raw = await res.json()
  return raw || []
}

export async function fetchLibs() {
  const res = await fetch(endpoints.libs)
  const raw = await res.json()
  return raw || []
}

export async function fetchRuns() {
  const res = await fetch(endpoints.runs)
  return await res.json()
}

export async function loadFileDataForRun(run) {
  if (run == null) return
  const url = endpoints.resultFiles + `/${run}`
  const res = await fetch(url)
  return await res.json()
}

export async function loadScores(run) {
  if (run == null) return
  const url = endpoints.scores + `/${run}`
  try {
    const res = await fetch(url)
    if (!res.ok) {
      console.warn('Failed to fetch scores', res.ok)
      return []
    }
    const data = await res.json()
    if (!Array.isArray(data)) {
      console.warn('Failed to fetch data', data)
      return []
    }
    return data
  } catch (err) {
    console.err('Failed to fetch data', err)
    return []
  }
}

