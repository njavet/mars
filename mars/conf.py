DEFAULT_PORT = 8080

# llama models
regular_1b = 'llama3.2:1b'
regular_3b = 'llama3.2:3b'

instruct_3b = 'llama3.2:3b-instruct-q8_0'

cai_regular = 'llama3.3:70b'
cai_instruct = 'llama3.3:70b-instruct-q8-0'

# sentence transformer model
sentence_transformer_name = 'all-MiniLM-L6-v2'
MODEL_OPTIONS = {
    "ChatGPT": "openai/gpt-4o",
    "LLaMA 3.2:1B": "llama3.2:1b",
    "LLaMA 3.2:3B": "llama3.2:3b",
    "Gemma-2B": "gemma:2b",

    "LLaMA 3.1:8B": "llama3.1:8b", # Model 1
    "Mistral-7B": "mistral", # Model 2
    "DeepSeek-R1:7b": "deepseek-r1:7b", # Model 3
    "Meditron": "meditron", # Model 4

    "DeepSeek-R1:14b": "deepseek-r1:14b", # Model 5
    "Qwen2.5:14b": "qwen2.5:14b", # Model 6
    
    "QwQ:32b": "qwq", # Model 7
    "DeepSeek-R1:32b": "deepseek-r1:32b" # Model 8 
}
