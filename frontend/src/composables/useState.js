import { ref } from 'vue';

// app state
const libs = ref([])
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
const selectedRun = ref(null)
const entries = ref([])
const selectedEvalModel = ref('')
const selectedFile = ref(null)

export function useAppState() {
    return {
        libs,
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

export function useEvalState() {
    return {
        runs,
        selectedRun,
        entries,
        selectedEvalModel,
        selectedFile,
    }
}

export const views = [
    { value: 'home', label: 'Home'},
    { value: 'about', label: 'About'},
    { value: 'chatbot', label: 'Chatbot'},
    { value: 'evaluation', label: 'Evaluation'}
]

export const users = [
    { value: 'abdk',  label: 'Ahmed' },
    { value: 'noe', label: 'Noe' },
]
