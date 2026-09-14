# GuiltFreeAI

A fully browser-based, privacy-first AI chat interface. No datacenters, no data collection, no API costs, no guilt.

---

## What is GuiltFreeAI?

GuiltFreeAI is a single-page web application that downloads and runs Large Language Models (LLMs) directly inside your web browser using your own computer's hardware. Your messages, documents, and images never leave your machine.

It is equal parts useful tool and proof of concept: personal AI chat that works offline after a model is downloaded, with no dependency on cloud AI providers.

---

## Features

- **Private by design** — all inference happens locally in your browser.
- **Multiple model tiers** — Low, Medium, High, and High Multimodal (vision-capable).
- **WebGPU & CPU support** — automatically uses WebGPU when available, falls back to WASM CPU inference.
- **Document chat** — upload `.txt`, `.docx`, `.pdf`, `.xlsx`, `.pptx` files and ask questions using local vector search.
- **Image input** — attach images for multimodal models.
- **Web search** — optional DuckDuckGo search integration via the local Python server.
- **Tunable generation** — per-model control over temperature, top-k, top-p, min-p, repeat penalty, batch size, and system prompt.
- **No accounts, no telemetry** — everything is stored locally in `localStorage` and in-memory.

---

## Project Structure

| File | Purpose |
|------|---------|
| `index.html` | The entire frontend application (HTML, CSS, and JavaScript). |
| `server.py` | Local Python server for web search and serving the app with required cross-origin isolation headers. |
| `models.json` | Configuration for available GGUF models, including download URLs and multimodal projector links. Fell free to swap in different models, the UI will automatically adjust. |
| `config.json` | Local configuration / metadata for the embedding model (`sentence-transformers/all-MiniLM-L6-v2`). |
| `favicon.ico` | Site icon. |
| `.gitignore` | Excludes downloaded model files and ONNX embeddings from version control. I keep these on the main hosting server in the event of a huggingface outage. |

---

## Use GuiltFreeAI

GuiltFreeAI is hosted at GuiltFreeAI.net and GuiltFreeAI.com. To use, simply visit one of these hosted sites.

## Host GuiltFreeAI

Want to locally host GuiltFreeAI yourself? Make sure you have Python installed. Clone the repo, run "pip install -r requirements.txt", and then server.py. You will have access at localhost:8080.
