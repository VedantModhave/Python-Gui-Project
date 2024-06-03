import tkinter as tk
from tkinter import messagebox

class SimplexTK(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Profit Optimizer for Production Company")
        self.configure(bg="#454545")  # Set dark background color

        # Creating input frame
        input_frame = tk.Frame(self, padx=20, pady=65, bg="#454545")
        input_frame.pack()

        # Objective Function Input
        tk.Label(input_frame, text="Price of Products: ", font=("Arial", 12, "bold"), bg="#454545", fg="white").grid(
            row=0, column=0, padx=10, pady=15)
        self.x1_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.x1_entry.grid(row=0, column=1, padx=10, pady=5)
        self.x2_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.x2_entry.grid(row=0, column=2, padx=10, pady=5)

        # Constraint 1 Input
        tk.Label(input_frame, text="Raw Material Quantity Required: ", font=("Arial", 12, "bold"), bg="#454545",
                 fg="white").grid(row=1, column=0, padx=10, pady=15)
        self.x11_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.x11_entry.grid(row=1, column=1, padx=10, pady=5)
        self.x22_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.x22_entry.grid(row=1, column=2, padx=10, pady=5)
        self.rhs1_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.rhs1_entry.grid(row=1, column=3, padx=10, pady=5)

        # Constraint 2 Input
        tk.Label(input_frame, text="Labour Hours Required: ", font=("Arial", 12, "bold"), bg="#454545",
                 fg="white").grid(row=2, column=0, padx=10, pady=15)
        self.x111_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.x111_entry.grid(row=2, column=1, padx=10, pady=5)
        self.x222_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.x222_entry.grid(row=2, column=2, padx=10, pady=5)
        self.rhs2_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.rhs2_entry.grid(row=2, column=3, padx=10, pady=5)

        # Create calculate button
        self.calculate_button = tk.Button(self, text="Calculate", font=("Arial", 12, "bold"), command=self.calculate,
                                          bg="#1E90FF", fg="white", bd=5)
        self.calculate_button.pack(pady=10, side="top", anchor="center")

        # Output labels
        self.conclusion_label = tk.Label(self, text="", font=("Arial", 14, "bold"), bg="#454545", fg="white")
        self.conclusion_label.pack(pady=(20, 10))
        self.pa_label = tk.Label(self, text="", font=("Arial", 14, "bold"), bg="#454545", fg="white")
        self.pa_label.pack()
        self.pb_label = tk.Label(self, text="", font=("Arial", 14, "bold"), bg="#454545", fg="white")
        self.pb_label.pack()

    def calculate(self):
        # Reset output labels
        self.conclusion_label.config(text="")
        self.pa_label.config(text="")
        self.pb_label.config(text="")

        # Get values from entry boxes
        try:
            x1 = float(self.x1_entry.get())
            x2 = float(self.x2_entry.get())
            x11 = float(self.x11_entry.get())
            x22 = float(self.x22_entry.get())
            x111 = float(self.x111_entry.get())
            x222 = float(self.x222_entry.get())
            rhs1 = float(self.rhs1_entry.get())
            rhs2 = float(self.rhs2_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values in all input fields")
            return

        # Check for negative values
        if x1 < 0 or x2 < 0 or x11 < 0 or x22 < 0 or x111 < 0 or x222 < 0 or rhs1 < 0 or rhs2 < 0:
            messagebox.showerror("Error", "Please enter positive values in all input fields")
            return

        # Create the tableau matrix
        tableau = [
            [x111, x222, 1, 0, 0, rhs2],
            [x11, x22, 0, 1, 0, rhs1],
            [-x1, -x2, 0, 0, 1, 0]
        ]

        num_variables = len(tableau[0]) - 1
        num_constraints = len(tableau)

        optimal = False

        while not optimal:
            pivot_column = self.find_pivot_column(tableau)
            if pivot_column == -1:
                optimal = True
                break

            pivot_row = self.find_pivot_row(tableau, pivot_column)
            if pivot_row == -1:
                raise ArithmeticError("Unbounded solution")

            pivot_element = tableau[pivot_row][pivot_column]
            self.divide_row(tableau, pivot_row, pivot_element)

            for i in range(num_constraints):
                if i != pivot_row:
                    ratio = tableau[i][pivot_column]
                    self.subtract_rows(tableau, i, pivot_row, ratio)

        solution = self.get_solution(tableau, num_variables, num_constraints)

        self.conclusion_label.config(
            text=f"Conclusion: The Maximum profit from both products: Rs. {solution[-1]:.2f}")
        self.pa_label.config(text=f"Product A units to be produced: {int(solution[0])}")
        self.pb_label.config(text=f"Product B units to be produced: {int(solution[1])}")

    @staticmethod
    def find_pivot_column(tableau):
        pivot_column = -1
        min_value = 0

        for j in range(len(tableau[0]) - 1):
            if tableau[-1][j] < min_value:
                min_value = tableau[-1][j]
                pivot_column = j

        return pivot_column

    @staticmethod
    def find_pivot_row(tableau, pivot_column):
        pivot_row = -1
        min_ratio = float('inf')

        for i in range(len(tableau) - 1):
            if tableau[i][pivot_column] > 0:
                ratio = tableau[i][-1] / tableau[i][pivot_column]
                if ratio < min_ratio:
                    min_ratio = ratio
                    pivot_row = i

        return pivot_row

    @staticmethod
    def divide_row(tableau, row, pivot_element):
        num_variables = len(tableau[0])

        for j in range(num_variables):
            tableau[row][j] /= pivot_element

    @staticmethod
    def subtract_rows(tableau, row1, row2, ratio):
        num_variables = len(tableau[0])

        for j in range(num_variables):
            tableau[row1][j] -= ratio * tableau[row2][j]

    @staticmethod
    def get_solution(tableau, num_variables, num_constraints):
        solution = [0] * (num_variables - 1)

        for j in range(num_variables - 1):
            basic_var = [row[j] for row in tableau[:-1]]
            if basic_var.count(1) == 1 and basic_var.count(0) == len(basic_var) - 1:
                row = basic_var.index(1)
                solution[j] = tableau[row][-1]

        solution.append(tableau[-1][-1])
        return solution


if __name__ == "__main__":
    app = SimplexTK()
    app.mainloop()
