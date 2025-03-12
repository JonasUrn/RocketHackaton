## Backend for RocketHackathon2025 

## Installation
### _Python_ dependencies
Install Python from https://python.org or other package delivery distributions.

`pip install flask flask_cors chromadb sentence_transformers ollama`


### _Ollama_ preparation
Download binary from https://ollama.com

`ollama serve`

`ollama pull llama3.2`

To test whether ollama installation is successful: `ollama run llama3.2`

## Run
`python app.py`
Should open a port on 5000.
