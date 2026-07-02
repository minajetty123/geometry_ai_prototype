# Geometry RAG Agent

A local AI assistant for a C# geometry component library. It uses **RAG** (Retrieval-Augmented Generation) to answer questions about geometry source code, and an **intent-based agent** to actually create, resize, and erase shapes in pixels.

Powered by **Qwen2.5-Coder-1.5B** running fully locally — no cloud API, no Ollama required.

---

## Architecture

```
User input
    │
    ▼
Intent Detection (keyword-based)
    │
    ├─► create / resize / erase / list
    │       │
    │       ▼
    │   geometry.py (Python geometry engine)
    │   Returns real measurements in pixels
    │
    └─► explain / why / what / how
            │
            ▼
        ChromaDB (vector index of C# source)
            │
            ▼
        Qwen2.5-Coder-1.5B (explains code)
```

### File overview

| File | Purpose |
|---|---|
| `chat.py` | CLI entry point |
| `agent.py` | Intent dispatcher + LLM parameter extraction |
| `geometry.py` | Python geometry engine (circle, square, rectangle) |
| `tools.py` | LangChain tool wrappers (used for future ReAct upgrades) |
| `index_code.py` | Indexes C# source files into ChromaDB |
| `config.py` | Model names, paths, chunk settings |
| `geometry_src/` | Your C# geometry source files (indexed for RAG) |
| `chroma_db/` | Auto-generated vector index (gitignore this) |

### Why two geometry representations?

| `geometry_src/*.cs` | `geometry.py` |
|---|---|
| Real production C# code | Python mirror for agent execution |
| Indexed by RAG for Q&A | Used to run real shape creation |
| Explains *why* things work | Executes *what* the user asks |

In production, `geometry.py` would be replaced by a call to your actual C# component via API or CLI interop.

---

## Requirements

- Python 3.9+
- ~3GB disk space (model cache)
- No GPU required (runs on CPU)

---

## Setup

### 1. Install dependencies

```powershell
pip install -r requirements.txt
```

> **Corporate proxy / SSL issues?** The SSL bypass is already built into `agent.py`.
> If you see symlink warnings on Windows, enable Developer Mode or run as administrator.

### 2. Add your C# source files

Place your `.cs` geometry files in `geometry_src/`:

```
geometry_src/
├── Circle.cs
├── Square.cs
└── Rectangle.cs
```

Sample files are already provided for testing.

### 3. Index the source code

```powershell
python index_code.py
```

Re-run this whenever your C# source files change.

### 4. Start the agent

```powershell
python chat.py
```

The first run downloads the model (~3GB) and caches it locally. Subsequent runs load instantly.

---

## Usage

```
=======================================================
  Geometry Agent (Qwen2.5-Coder + Tools)
  Type 'exit' to quit.
=======================================================
```

### Shape operations (real execution)

| What you type | What happens |
|---|---|
| `Create a circle with radius 50px` | Creates circle, returns all measurements |
| `Make it bigger by 20px` | Increases radius by 20px |
| `Create a rectangle 100x60px` | Creates rectangle with width=100, height=60 |
| `Make the square smaller by 10px` | Decreases side length |
| `Erase circle_1` | Removes shape from canvas |
| `List all shapes` | Shows all shapes with measurements |

### Knowledge questions (RAG over C# source)

| What you type | What happens |
|---|---|
| `Why does Circle throw an error with radius -1?` | Retrieves C# validation code, explains it |
| `What is the formula for the diagonal of a square?` | Retrieves algorithm from source |
| `What parameters does Rectangle need?` | Retrieves constructor docs |

---

## Example session

```
You: Create a circle with radius 50px
Assistant: Created: [circle_1] Circle | radius=50.0px | diameter=100.0px | area=7854.0px² | circumference=314.2px

You: Make it bigger by 20px
Assistant: Resized: [circle_1] Circle | radius=70.0px | diameter=140.0px | area=15393.8px² | circumference=439.8px

You: Why does Circle throw an error with radius -1?
Assistant: The Circle constructor validates that radius must be greater than 0.
If you pass -1, it throws an ArgumentException with the message:
"radius must be greater than 0. You provided: -1px."

You: Erase circle_1
Assistant: Shape 'circle_1' erased.
```

---

## Configuration

Edit `config.py` to customise:

```python
SOURCE_CODE_DIR = "./geometry_src"               # path to your C# files
CHROMA_DB_DIR   = "./chroma_db"                  # vector index storage
EMBED_MODEL     = "all-MiniLM-L6-v2"             # embedding model
LLM_MODEL       = "Qwen/Qwen2.5-Coder-1.5B-Instruct"  # language model
CHUNK_SIZE      = 800                            # RAG chunk size
CHUNK_OVERLAP   = 100                            # RAG chunk overlap
```

---

## Extending with your own C# geometry files

1. Add your `.cs` files to `geometry_src/`
2. Re-run `python index_code.py`
3. Update `geometry.py` to mirror any new shapes for real execution

---

## Troubleshooting

| Error | Fix |
|---|---|
| `SSL certificate verify failed` | Already patched. If still failing, ask IT for your corporate CA cert. |
| `403 Forbidden (HuggingFace)` | Model uses offline cache. Run `index_code.py` first to confirm setup. |
| `No shapes to resize/erase` | Create a shape first. |
| Model repeats itself | Expected on CPU with small LLMs. The intent dispatcher avoids most cases. |
