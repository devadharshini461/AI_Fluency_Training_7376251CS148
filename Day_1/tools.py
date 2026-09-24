import ast
import operator
from config import COURSES

def get_course_fee(course_code: str):
    """Retrieve the fee for a given course code."""
    course_code = course_code.strip().upper()
    if course_code in COURSES:
        return COURSES[course_code]
    return f"Course '{course_code}' not found."

def calculator(expression: str):
    """Safely evaluate a mathematical expression using AST parsing (no eval)."""
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv
    }

    def evaluate(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            op = allowed_operators[type(node.op)]
            return op(evaluate(node.left), evaluate(node.right))
        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -evaluate(node.operand)
            if isinstance(node.op, ast.UAdd):
                return evaluate(node.operand)
        raise ValueError("Invalid mathematical expression")

    try:
        clean_expr = expression.replace("₹", "").replace(",", "").strip()
        parsed = ast.parse(clean_expr, mode="eval")
        result = evaluate(parsed.body)
        return result
    except Exception as e:
        return f"Error evaluating expression '{expression}': {e}"

# Alias for compatibility
calculate = calculator

if __name__ == "__main__":
    print("Testing get_course_fee:")
    print(get_course_fee("AI202"))

    print("\nTesting calculator:")
    print(calculator("(12000 + 18000) * 0.9"))

    print("\nTesting calculator:")
    print(calculator("15000 - 12000"))