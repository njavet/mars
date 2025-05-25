import {endpoints} from "./endpoints.js";

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
