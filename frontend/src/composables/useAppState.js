import { ref } from 'vue';

const libs = ref([])
const selectedLib = ref('')
const servers = ref(['http://localhost:11434'])
const selectedServer = ref('http://localhost:11434')
const models = ref([])
const selectedModel = ref('')
const systemMessages = ref([])
const selectedSystemMessage = ref('')
const agentic = ref(false)

export function useAppState() {
    return {
        libs,
        selectedLib,
        servers,
        selectedServer,
        models,
        selectedModel,
        systemMessages,
        selectedSystemMessage,
        agentic,
    }
}
