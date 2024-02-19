import ast
import math
from tkinter import messagebox


class Model:
    def __init__(self):
        self.expression = ""
        self.history = []

    def get_expression(self):
        """ Get the current expression. """
        return self.expression

    def evaluate_expression(self):
        try:
            # Parse the expression and replace math functions
            parsed_expression = ast.parse(self.expression, mode='eval')
            for node in ast.walk(parsed_expression):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id == 'exp':
                            node.func = ast.Name(id='math.exp', ctx=ast.Load())
                        elif node.func.id == 'ln':
                            node.func = ast.Name(id='math.log', ctx=ast.Load())
                        elif node.func.id == 'log':
                            node.func = ast.Name(id='math.log10', ctx=ast.Load())
                        elif node.func.id == 'sqrt':
                            node.func = ast.Name(id='math.sqrt', ctx=ast.Load())

            # Evaluate the modified expression
            result = eval(compile(parsed_expression, filename='', mode='eval'))
            self.history.append((self.expression, result))
            return result
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_last(self):
        """ Delete the last character from the expression. """
        if self.expression:
            self.expression = self.expression[:-1]
        return self.expression

    def clear_expression(self):
        """ Clear the expression. """
        self.expression = ""
        return self.expression

    def add_to_expression(self, char):
        self.expression += char

    def clear_history(self):
        self.history = []
