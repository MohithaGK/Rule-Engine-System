from flask import Flask, request, jsonify, render_template
import sqlite3
import json
import logging
import re

app = Flask(__name__, static_url_path='/static')

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    return render_template('index.html')


class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" for AND/OR, "operand" for conditions
        self.left = left  # Left child (Node)
        self.right = right  # Right child (Node)
        self.value = value

    def to_dict(self):
        """Convert Node to a dictionary for JSON serialization."""
        return {
            'type': self.type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None,
        }

def create_ast(rule_string):
    # Split the rule string by AND/OR and handle parentheses for complex expressions
    tokens = re.split(r'\s(AND|OR)\s', rule_string)
    stack = []
    current_node = None

    for token in tokens:
        token = token.strip()
        if token in ('AND', 'OR'):
            if current_node:
                stack.append(current_node)
            current_node = Node('operator', value=token)
        else:
            operand_node = Node('operand', value=token)
            if current_node:
                current_node.right = operand_node
            else:
                current_node = operand_node

    # If there's remaining nodes in the stack, we build the tree
    while len(stack) > 0:
        operator_node = stack.pop()
        operator_node.left = current_node
        current_node = operator_node

    return current_node

def print_ast(node, indent=0):
    """Print the AST in a line-by-line format."""
    if node is not None:
        print(' ' * indent + f"{node.type}: {node.value}")
        print_ast(node.left, indent + 4)  # Indent for the left child
        print_ast(node.right, indent + 4)  # Indent for the right child


@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json.get('rule_string')

    if not isinstance(rule_string, str):
        return jsonify({"message": "Invalid rule string format"}), 400

    ast_root = create_ast(rule_string)
    logger.debug(f"Rule created: {rule_string}, AST: {ast_root.value}")  # Log AST representation

    # Save to the database logic here
    with sqlite3.connect('rules.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rules (rule_string, ast_json) VALUES (?, ?)",
                       (rule_string, json.dumps(ast_root.to_dict())))  # Use to_dict() for JSON serialization
        conn.commit()

    return jsonify({"message": "Rule created", "ast": ast_root.to_dict()})


@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    # Extract rules and combination type from the request
    rules = request.json.get('rules')
    combination_type = request.json.get('combination_type', 'AND')  # Default to 'AND' if not specified

    # Validate input
    if not rules or len(rules) < 1:
        return jsonify({"message": "At least one rule is required."}), 400

    # Create ASTs for each rule
    asts = []
    for rule in rules:
        ast_root = create_ast(rule)
        asts.append(ast_root)

    # Handle single rule case
    if len(asts) == 1:
        return jsonify({"message": "Combined", "ast": asts[0].to_dict()})

    # Combine multiple ASTs into one
    root = Node("operator", value=combination_type)
    current_node = root
    for ast in asts:
        current_node.right = ast  # Link the next AST
        current_node = ast  # Move current_node to the next one for chaining

    logger.debug(f"Combined AST: {root.to_dict()}")  # Log combined AST for debugging

    # Return the combined AST as a JSON response
    return jsonify({"message": "Rules combined", "ast": root.to_dict()})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    data = request.json.get('data')
    rule_id = request.json.get('rule_id')

    if not data or not rule_id:
        return jsonify({"message": "Missing rule_id or data"}), 400

    with sqlite3.connect('rules.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ast_json FROM rules WHERE id = ?", (rule_id,))
        row = cursor.fetchone()

    if not row:
        return jsonify({"message": "Rule not found"}), 404

    try:
        ast_root = json.loads(row[0])
    except json.JSONDecodeError:
        return jsonify({"message": "Invalid AST format"}), 400

    # Evaluate the rule
    result = evaluate_ast(ast_root, data)

    logger.debug(f"Evaluating rule ID {rule_id} against data {data}: Result: {result}")

    return jsonify({"result": result, "message": "Evaluation successful"})


def evaluate_ast(ast, data):
    """Recursively evaluate the AST based on input data."""
    if ast['type'] == 'operand':
        condition = ast['value']
        try:
            # Convert the condition to a format Python can understand for eval()
            condition = re.sub(r"([a-zA-Z_][a-zA-Z_0-9]*)", r"data['\1']", condition)
            return eval(condition)  # Consider using a safer alternative to eval()
        except Exception as e:
            logger.error(f"Error evaluating condition '{condition}': {e}")
            return False

    elif ast['type'] == 'operator':
        left_result = evaluate_ast(ast['left'], data) if ast.get('left') else None
        right_result = evaluate_ast(ast['right'], data) if ast.get('right') else None

        if ast['value'] == 'AND':
            return left_result and right_result
        elif ast['value'] == 'OR':
            return left_result or right_result

    return False


if __name__ == '__main__':
    with sqlite3.connect('rules.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS rules (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          rule_string TEXT NOT NULL,
                          ast_json TEXT NOT NULL)''')
        conn.commit()

    app.run(debug=True)
