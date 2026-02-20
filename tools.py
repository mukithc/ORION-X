"""
ORION-X Agent Tools
Calculator, web search, and other utilities.
"""

import re
import ast
import operator

# Safe math operators for calculator
SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _eval_node(node):
    """Safely evaluate AST node - numbers and basic math only."""
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_node(node.operand)
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op = SAFE_OPS.get(type(node.op))
        if op is None:
            raise ValueError("Unsupported operation")
        return op(left, right)
    raise ValueError("Only numbers and basic math allowed")


def calculator(expr: str) -> str:
    """Safely evaluate a math expression. Returns result or error."""
    expr = expr.strip().replace(",", "")
    # Only allow numbers, spaces, + - * / ^ ( )
    if not re.match(r"^[\d\s+\-*/().^]+$", expr):
        return "Error: Only numbers and + - * / ^ ( ) allowed"
    expr = expr.replace("^", "**")
    try:
        tree = ast.parse(expr, mode="eval")
        result = _eval_node(tree.body)
        return str(round(result, 10) if isinstance(result, float) else result)
    except Exception as e:
        return f"Error: {e}"


def web_search(query: str, max_results: int = 5) -> str:
    """Search the web and return snippets. Requires duckduckgo-search."""
    try:
        from duckduckgo_search import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(f"- {r.get('title', '')}: {r.get('body', '')[:200]}...")
        return "\n".join(results) if results else "No results found."
    except ImportError:
        return "Web search requires: pip install duckduckgo-search"
    except Exception as e:
        return f"Search error: {e}"


def process_with_tools(message: str) -> str:
    """
    Detect tool use in message and prepend results.
    Returns enhanced message for the LLM.
    """
    enhanced = message
    lower = message.lower().strip()

    # Calculator
    if "calculate" in lower or "compute" in lower:
        m = re.search(r"(?:calculate|compute)\s+(.+)", lower, re.I)
        if m:
            result = calculator(m.group(1).strip())
            enhanced = f"[Calculator result: {result}]\n\n{message}"
    elif re.match(r"^[\d\s+\-*/().^,]+$", message.strip()):
        result = calculator(message.strip())
        enhanced = f"[Calculator result: {result}]\n\n{message}"
    elif re.match(r"^what is\s+[\d\s+\-*/().^,]+\s*\??$", lower):
        m = re.search(r"what is\s+(.+)", lower, re.I)
        if m:
            result = calculator(m.group(1).strip().rstrip("?"))
            enhanced = f"[Calculator result: {result}]\n\n{message}"

    # Web search
    elif "search for" in lower or "look up" in lower:
        for prefix in ["search for", "look up"]:
            if prefix in lower:
                idx = lower.find(prefix)
                query = message[idx + len(prefix):].strip()
                if query:
                    results = web_search(query)
                    enhanced = f"[Web search results for '{query}':\n{results}]\n\n{message}"
                break

    return enhanced
