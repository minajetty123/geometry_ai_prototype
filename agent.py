"""
agent.py
Simple geometry agent — intent detection + direct tool dispatch.
More reliable than ReAct for small LLMs (1.5B).

Flow:
  1. Detect intent (create / resize / erase / list / explain) via keywords
  2. Use LLM to extract structured parameters from natural language
  3. Call the real tool directly
  4. Return the result
"""

import os, ssl, urllib3, requests as _req, json, re

ssl._create_default_https_context = ssl._create_unverified_context
os.environ["CURL_CA_BUNDLE"] = ""
os.environ["REQUESTS_CA_BUNDLE"] = ""
os.environ["HF_HUB_DISABLE_XET"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
_orig = _req.Session.send
def _patched(self, *a, **kw): kw["verify"] = False; return _orig(self, *a, **kw)
_req.Session.send = _patched

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline as hf_pipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from config import CHROMA_DB_DIR, EMBED_MODEL, LLM_MODEL
import geometry as geo


# ── Intent keywords ───────────────────────────────────────────────────────────

def detect_intent(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["create", "make a", "draw", "add", "new"]):
        return "create"
    if any(w in t for w in ["bigger", "larger", "increase", "grow", "expand",
                              "smaller", "decrease", "shrink", "reduce", "resize"]):
        return "resize"
    if any(w in t for w in ["erase", "delete", "remove", "clear"]):
        return "erase"
    if any(w in t for w in ["list", "show", "what shapes", "canvas"]):
        return "list"
    return "explain"


# ── LLM-based parameter extraction ───────────────────────────────────────────

def _call_llm(pipe, prompt: str) -> str:
    result = pipe(prompt)
    return result[0]["generated_text"].strip()


def extract_create_params(pipe, text: str) -> dict:
    prompt = f"""Extract geometry shape parameters from this request.
Return ONLY a JSON object. Nothing else.

Request: "{text}"

Rules:
- "type" must be one of: circle, square, rectangle
- circle needs "radius" (number in pixels)
- square needs "side" (number in pixels)
- rectangle needs "width" and "height" (numbers in pixels)
- If no unit mentioned, assume pixels

JSON:"""
    raw = _call_llm(pipe, prompt)
    match = re.search(r'\{[^}]+\}', raw)
    if not match:
        raise ValueError(f"Could not parse parameters from: {raw}")
    return json.loads(match.group())


def extract_resize_params(pipe, text: str, existing_ids: list) -> dict:
    prompt = f"""Extract resize parameters from this request.
Return ONLY a JSON object. Nothing else.

Existing shape IDs: {existing_ids}
Request: "{text}"

Rules:
- "shape_id": pick the most relevant shape from existing IDs (or the last one if unclear)
- "amount": positive number = bigger, negative number = smaller (in pixels)

JSON:"""
    raw = _call_llm(pipe, prompt)
    match = re.search(r'\{[^}]+\}', raw)
    if not match:
        raise ValueError(f"Could not parse parameters from: {raw}")
    return json.loads(match.group())


def extract_erase_params(pipe, text: str, existing_ids: list) -> dict:
    prompt = f"""Which shape ID should be erased?
Return ONLY a JSON object like: {{"shape_id": "circle_1"}}

Existing shape IDs: {existing_ids}
Request: "{text}"

JSON:"""
    raw = _call_llm(pipe, prompt)
    match = re.search(r'\{[^}]+\}', raw)
    if not match:
        raise ValueError(f"Could not parse parameters from: {raw}")
    return json.loads(match.group())


# ── Main agent class ─────────────────────────────────────────────────────────

class GeometryAgent:
    def __init__(self, pipe, retriever):
        self.pipe = pipe
        self.retriever = retriever

    def run(self, user_input: str) -> str:
        intent = detect_intent(user_input)

        if intent == "create":
            try:
                params = extract_create_params(self.pipe, user_input)
                shape_type = params.pop("type")
                result = geo.create_shape(shape_type, **params)
                return result
            except Exception as e:
                return f"Could not create shape: {e}"

        elif intent == "resize":
            existing = list(geo._registry.keys())
            if not existing:
                return "No shapes on the canvas to resize."
            try:
                params = extract_resize_params(self.pipe, user_input, existing)
                result = geo.resize_shape(params["shape_id"], float(params["amount"]))
                return result
            except Exception as e:
                return f"Could not resize shape: {e}"

        elif intent == "erase":
            existing = list(geo._registry.keys())
            if not existing:
                return "No shapes on the canvas to erase."
            try:
                params = extract_erase_params(self.pipe, user_input, existing)
                result = geo.erase_shape(params["shape_id"])
                return result
            except Exception as e:
                return f"Could not erase shape: {e}"

        elif intent == "list":
            return geo.list_shapes()

        else:  # explain — RAG
            docs = self.retriever.invoke(user_input)
            context = "\n\n".join(d.page_content for d in docs)
            prompt = f"""You are an expert on a C# geometry library. Use ONLY the source code below.
Answer concisely. Stop after your answer.

Source code:
{context}

Question: {user_input}
Answer:"""
            answer = _call_llm(self.pipe, prompt)
            # Trim at any "Question:" repetition
            answer = re.split(r'\nQuestion:', answer)[0].strip()
            return answer


# ── Builder ───────────────────────────────────────────────────────────────────

def build_agent() -> GeometryAgent:
    print("Loading vector index ...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    db = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings,
                collection_name="geometry_code")
    retriever = db.as_retriever(search_kwargs={"k": 3})

    print(f"Loading LLM '{LLM_MODEL}' ...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
    model = AutoModelForCausalLM.from_pretrained(
        LLM_MODEL,
        dtype=torch.float16 if device == "cuda" else torch.float32,
        device_map="auto",
    )
    pipe = hf_pipeline(
        "text-generation", model=model, tokenizer=tokenizer,
        max_new_tokens=256, temperature=0.1, do_sample=True,
        return_full_text=False,
    )
    return GeometryAgent(pipe, retriever)

