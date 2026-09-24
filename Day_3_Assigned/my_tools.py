"""Day 3: Tools for the Online Shopping Assistant."""

import ast
import operator
import os
import re


# ============================================================
# 1. SAFE CALCULATOR
# ============================================================

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right)
        )

    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](
            _evaluate(node.operand)
        )

    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    try:
        result = _evaluate(
            ast.parse(expression, mode="eval").body
        )
        return str(result)

    except Exception as error:
        return (
            f"Calculator error: {error}. "
            "Use only numbers and + - * / ** ( )."
        )


# ============================================================
# 2. HTML READER
# ============================================================

CURRENT_HTML = ""
CURRENT_FILENAME = ""


def read_html(filename: str, max_chars: int = 3000) -> str:
    """
    Read a local HTML file and return clean visible text.
    The contents are stored so other tools can use the
    currently loaded catalog.
    """

    global CURRENT_HTML
    global CURRENT_FILENAME

    try:
        if not os.path.exists(filename):
            return (
                f"Read error: '{filename}' was not found."
            )

        with open(
            filename,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:
            raw = file.read()

        # Remove script and style blocks
        raw = re.sub(
            r"<(script|style)[^>]*>.*?</\1>",
            " ",
            raw,
            flags=re.S | re.I
        )

        # Remove HTML tags
        text = re.sub(r"<[^>]+>", " ", raw)

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text).strip()

        if not text:
            return (
                f"Read error: '{filename}' "
                "contained no readable text."
            )

        # Store the loaded HTML for other tools
        CURRENT_HTML = text
        CURRENT_FILENAME = filename

        if len(text) > max_chars:
            text = (
                text[:max_chars]
                + f" ... [truncated, {len(CURRENT_HTML)} "
                  "characters total]"
            )

        return text

    except Exception as error:
        return (
            f"Read error: {type(error).__name__}: {error}"
        )


# ============================================================
# 3. PRODUCT SEARCH
# ============================================================

def search_product(query: str, max_price: float) -> str:
    """
    Search the HTML file that was most recently loaded
    using read_html().
    """

    if not CURRENT_HTML:
        return (
            "Search error: no HTML catalog is loaded. "
            "Call read_html first."
        )

    try:
        pattern = re.compile(
            r"([A-Za-z0-9]+(?:\s+[A-Za-z0-9]+)*)"
            r"\s+Product ID:\s*([A-Z0-9]+)"
            r"\s+Category:\s*([A-Za-z]+)"
            r"\s+Price:\s*Rs\.\s*([0-9]+)"
            r"\s+Stock:\s*(In Stock|Out of Stock)",
            re.I
        )

        matches = pattern.findall(CURRENT_HTML)

        results = []

        for match in matches:

            name = match[0].strip()
            product_id = match[1].strip()
            category = match[2].strip()
            price = float(match[3])
            stock = match[4].strip()

            if (
                query.lower() in category.lower()
                and price <= max_price
            ):
                results.append({
                    "name": name,
                    "product_id": product_id,
                    "price": price,
                    "stock": stock
                })

        if not results:
            return (
                f"No {query} products found under "
                f"Rs. {max_price} in {CURRENT_FILENAME}."
            )

        return str(results)

    except Exception as error:
        return (
            f"Search error: {type(error).__name__}: {error}"
        )


# ============================================================
# 4. STOCK CHECK
# ============================================================

def check_stock(product_id: str) -> str:
    """
    Check stock using the currently loaded HTML catalog.
    """

    if not CURRENT_HTML:
        return (
            "Stock error: no HTML catalog is loaded. "
            "Call read_html first."
        )

    try:
        pattern = re.compile(
            rf"Product ID:\s*{re.escape(product_id)}"
            rf".*?Stock:\s*(In Stock|Out of Stock)",
            re.I
        )

        match = pattern.search(CURRENT_HTML)

        if not match:
            return (
                f"Stock error: product "
                f"{product_id} not found in "
                f"{CURRENT_FILENAME}."
            )

        stock_status = match.group(1).strip()

        return (
            f"{product_id}: {stock_status}"
        )

    except Exception as error:
        return (
            f"Stock error: {type(error).__name__}: {error}"
        )


# ============================================================
# 5. TOOL REGISTRY
# ============================================================

TOOL_FUNCTIONS = {
    "read_html": read_html,
    "search_product": search_product,
    "check_stock": check_stock,
    "calculator": calculator,
}


# ============================================================
# 6. JSON TOOL SCHEMAS
# ============================================================

TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "read_html",
            "description": (
                "Read a local HTML file and return its visible text. "
                "Use this first when the user mentions a specific "
                "HTML file such as products.html."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": (
                            "Name of the HTML file to read, "
                            "for example products.html."
                        )
                    }
                },
                "required": ["filename"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_product",
            "description": (
                "Search the HTML catalog that was most recently "
                "loaded using read_html."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "Product category, such as laptop."
                        )
                    },
                    "max_price": {
                        "type": "number",
                        "description": (
                            "Maximum price in Indian rupees."
                        )
                    }
                },
                "required": ["query", "max_price"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "check_stock",
            "description": (
                "Check whether a product is in stock in "
                "the currently loaded HTML catalog."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Unique product ID."
                    }
                },
                "required": ["product_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "Safely perform arithmetic calculations."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "Arithmetic expression such as "
                            "54999 * 0.9."
                        )
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


# ============================================================
# 7. DIRECT TOOL TESTING
# ============================================================

if __name__ == "__main__":

    print("=== TOOL TESTING ===")

    print("\n1. Calculator:")
    print(calculator("54999 * 0.9"))

    print("\n2. Read HTML:")
    print(read_html("products.html"))

    print("\n3. Product Search:")
    print(search_product("laptop", 60000))

    print("\n4. Stock Check:")
    print(check_stock("HP15"))

    print("\n5. Invalid Product:")
    print(check_stock("UNKNOWN"))

    print("\n6. Missing HTML File:")
    print(read_html("missing_products.html"))