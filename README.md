# MARS
Multi Agent RAG system 

# setup
poetry for project / dependencies management

### FastAPI backend
```
cd mars
poetry install
poetry run mars
```

For pip / venv
```
poetry export -f requirements.txt --without-hashes > requirements.txt
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Vue frontend
```
cd mars/frontend
npm install
npm run dev
```

### pdf embeddings
fresh setup:
```angular2html
rm -rf mars/data/pdfs
rm mars/sentence.db
rm mars/index.faiss
```
Now you can copy a new set of pdfs to `mars/data/pdfs`
and restart fastAPI. 


## Activate Virtual Environment

```
source /raid/persistent_scratch/<zhaw-user>/venvs/bafs25_env/bin/activate
```

## ZHAW cluster
* setup zhaw vpn

log into server:

`ssh <user_name>@dallas.zhaw.ch`

request GPU node:

`srun --gres=gpu:1 --partition=gpu_ia --pty --account=<user_group> bash`

* launch tmux and split terminal into two:
 
`tmux`

`<Ctrl-b><%>`

* temporary / manually set ollama host env variable:
 
`export OLLAMA_HOST="$(hostname).zhaw.ch:$(showcustomports | grep -oE '[0-9]+' | head -n1)"`

check the true host name / port (`showcustomports`)

start ollama server:

`ollama/bin/ollama serve`

Now connect the client:
```
from langchain_ollama import ChatOllama
a = ChatOllama(base_url='sandiego.zhaw.ch:8800', model='llama3.3:70b)
```

