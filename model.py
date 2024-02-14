from tkinter import messagebox


class Model:
    def __init__(self):
        self.expression = ""
        self.history = []

    def evaluate_expression(self):
        try:
            result = eval(self.expression)
            self.history.append((self.expression, result))
            return result
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_expression(self):
        self.expression = ""

    def delete_last(self):
        self.expression = self.expression[:-1]

    def add_to_expression(self, char):
        self.expression += char

    # def clear_history(self):
    #     self.history = []
