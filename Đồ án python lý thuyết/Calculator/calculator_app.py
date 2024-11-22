import tkinter as tk
from tkinter import messagebox


root = tk.Tk()
root.title("Máy tính đơn giản")
root.geometry("300x200")

def calculate():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        operator = operator_var.get()
        
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                messagebox.showerror("Lỗi", "Không thể chia cho 0")
                return
            result = num1 / num2
        else:
            messagebox.showerror("Lỗi", "Phép toán không hợp lệ")
            return
        
        result_label.config(text="Kết quả: " + str(result))
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
        
entry1 = tk.Entry(root, width=10)
entry1.grid(row=0, column=1, padx=5, pady=5)

entry2 = tk.Entry(root, width=10)
entry2.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Số thứ nhất:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(root, text="Số thứ hai:").grid(row=1, column=0, padx=5, pady=5)

operator_var = tk.StringVar(value="+")
operator_menu = tk.OptionMenu(root, operator_var, "+", "-", "*", "/")
operator_menu.grid(row=2, column=1, padx=5, pady=5)

calc_button = tk.Button(root, text="Tính toán", command=calculate)
calc_button.grid(row=3, column=1, padx=5, pady=5)

result_label = tk.Label(root, text="Kết quả: ")
result_label.grid(row=4, column=1, padx=5, pady=5)

root.mainloop()
