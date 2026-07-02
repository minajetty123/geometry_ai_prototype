"""
tools.py
LangChain tools that wrap the geometry engine and the RAG retriever.
The agent calls these tools to fulfil user requests.
"""

import json
from langchain.tools import tool
import geometry as geo


@tool
def create_shape(input: str) -> str:
    """
    Create a geometry shape (circle, square, or rectangle) in pixels.
    Input must be a JSON string with:
      - "type": "circle" | "square" | "rectangle"
      - For circle:    "radius": <number>
      - For square:    "side": <number>
      - For rectangle: "width": <number>, "height": <number>
    Example: {"type": "circle", "radius": 50}
    """
    try:
        params = json.loads(input)
        shape_type = params.pop("type")
        return geo.create_shape(shape_type, **params)
    except (ValueError, KeyError) as e:
        return f"Error: {e}"


@tool
def resize_shape(input: str) -> str:
    """
    Make an existing shape bigger or smaller.
    Input must be a JSON string with:
      - "shape_id": the ID returned when the shape was created (e.g. "circle_1")
      - "amount": pixels to add (positive = bigger, negative = smaller)
    Example: {"shape_id": "circle_1", "amount": 20}
    """
    try:
        params = json.loads(input)
        return geo.resize_shape(params["shape_id"], float(params["amount"]))
    except (ValueError, KeyError) as e:
        return f"Error: {e}"


@tool
def erase_shape(input: str) -> str:
    """
    Remove a shape from the canvas.
    Input must be a JSON string with:
      - "shape_id": the ID of the shape to erase (e.g. "square_1")
    Example: {"shape_id": "square_1"}
    """
    try:
        params = json.loads(input)
        return geo.erase_shape(params["shape_id"])
    except (ValueError, KeyError) as e:
        return f"Error: {e}"


@tool
def list_shapes(input: str = "") -> str:
    """
    List all shapes currently on the canvas with their measurements.
    No input required.
    """
    return geo.list_shapes()


def make_explain_tool(retriever):
    """Returns a RAG-backed tool for answering docs/code questions."""

    @tool
    def explain_geometry(question: str) -> str:
        """
        Answer questions about the geometry component: parameters, validation rules,
        algorithms, error explanations. Use this for 'why', 'what', 'how' questions.
        """
        docs = retriever.invoke(question)
        context = "\n\n".join(d.page_content for d in docs)
        return f"Relevant source code:\n{context}"

    return explain_geometry
