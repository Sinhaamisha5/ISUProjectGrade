import requests
import tkinter as tk
from tkinter import messagebox

def get_grade_conversion():
    university = university_entry.get().strip()
    grade = grade_entry.get().strip()

    if not university:
        messagebox.showerror("Error", "Please enter a university name.")
        return

    # Construct API URL
    url = f"http://127.0.0.1:5000/convert_grade?university={university}"
    if grade:
        url += f"&grade={grade}"

    try:
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            result_label.config(text=f"Error: {data['error']}", fg="red")
        else:
            result_label.config(text=f"Result: {data}", fg="green")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to connect to API.\n{e}")

# Create UI window
root = tk.Tk()
root.title("Grade Converter")

tk.Label(root, text="University:").grid(row=0, column=0, padx=10, pady=5)
university_entry = tk.Entry(root, width=30)
university_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Grade (optional):").grid(row=1, column=0, padx=10, pady=5)
grade_entry = tk.Entry(root, width=30)
grade_entry.grid(row=1, column=1, padx=10, pady=5)

convert_button = tk.Button(root, text="Convert", command=get_grade_conversion)
convert_button.grid(row=2, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
