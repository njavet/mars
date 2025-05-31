import {computed, ref} from 'vue';

// app state
const servers = ref(['http://localhost:11434'])
const models = ref([])
const systemMessages = ref([])

// bot state
const selectedLib = ref('')
const selectedServer = ref('http://localhost:11434')
const selectedModel = ref('')
const selectedSystemMessage = ref('')
const agentic = ref(false)

// chat state
const messages = ref([])
const loading = ref(false)

// eval state
const runs = ref([])
const selectedRun = ref('')
const evalDocs = ref([])
const selectedEvalModel = ref('')
const selectedFile = ref('')

const selectedEvalDoc = computed(() => {
    if (!selectedFile.value) return null
    if (evalDocs.value) {
        return evalDocs.value.find(e => e?.filename === selectedFile.value) || null
    } else {
        return null
    }
})

const evalModels = computed(() => {
  if (!selectedEvalDoc.value) return []
  return Object.keys(selectedEvalDoc.value?.models) || []
})

const evalSystemMessage = computed(() => {
  return selectedEvalDoc.value?.system_message || ''
})

const selectedOutput = computed(() => {
  return selectedEvalDoc.value?.models?.[selectedEvalModel.value] ?? ''
})

export function useAppState() {
    return {
        servers,
        models,
        systemMessages,
    }
}

export function useBotState() {
    return {
        selectedLib,
        selectedServer,
        selectedModel,
        selectedSystemMessage,
        agentic,
    }
}

export function useChatState() {
    return {
        messages,
        loading,
    }
}

export function useEvalSettingState() {
    return {
        runs,
        selectedRun,
        evalDocs,
        evalModels,
        selectedEvalModel,
        selectedFile,
    }
}

export function useEvalState() {
    return {
        evalSystemMessage,
        selectedEvalDoc,
        selectedOutput,
    }
}

export function useScoreState() {

}

export const views = [
    { value: 'home', label: 'Home'},
    { value: 'about', label: 'About'},
    { value: 'chatbot', label: 'Chatbot'},
    { value: 'evaluation', label: 'Evaluation'}
]

