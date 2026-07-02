# Configuration
SOURCE_CODE_DIR = "./geometry_src"         # Point this to your C# source folder
CHROMA_DB_DIR   = "./chroma_db"            # Where the vector index is stored
EMBED_MODEL     = "all-MiniLM-L6-v2"      # Local embedding model (no API key needed)
LLM_MODEL       = "Qwen/Qwen2.5-Coder-1.5B-Instruct"  # HuggingFace model ID
CHUNK_SIZE      = 800
CHUNK_OVERLAP   = 100
