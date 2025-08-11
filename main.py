from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import messagebox
from comparator import start_comparison as start_comparison

valid_files = {"left": None, "right": None}

def validate_button_state():
    if valid_files["left"] and valid_files["right"]:
        btn1.config(state="normal")
    else:
        btn1.config(state="disabled")

def handle_drop_left(event):
    filepath = event.data.strip('{}')
    filename = filepath.split('/')[-1]

    if not filepath.endswith(('.xlsx', '.xls')):
        messagebox.showwarning("Неправилна Excel датотека", "Унесите Excel датотеку у правилном формату (.xlsx или .xls)")
        valid_files["left"] = None
    elif "SEF" not in filename and "sef" not in filename:
        messagebox.showwarning("Неправилна Excel датотека", "Потребно је унети SEF Excel датотеку.\nПровери да ли је датотека исправна.")
        valid_files["left"] = None
    else:
        valid_files["left"] = filepath
        path_sef.config(text=filepath)
        small_box_left.config(bg="lightgreen")
    validate_button_state()

def handle_drop_right(event):
    filepath = event.data.strip('{}')
    if filepath.endswith(('.xlsx', '.xls')):
        valid_files["right"] = filepath
        path_comp.config(text=filepath)
        small_box_right.config(bg="lightgreen")
    else:
        messagebox.showwarning("Неправилна Excel датотека", "Унесите Excel датотеку у правилном формату (.xlsx или .xls)")
        valid_files["right"] = None
    validate_button_state()

def on_btn1_click():
    sef_path = valid_files["left"]
    compare_path = valid_files["right"]

    try:
        nepostojeci, nepodudarni = start_comparison(sef_path, compare_path)
        if nepodudarni:
            result = ", ".join(map(str,nepodudarni.items()))
        else:
            result = "Све је у реду."
            
        input_field.config(state="normal")
        input_field.delete("1.0", tk.END)
        input_field.insert("1.0", result)
        input_field.config(state="disabled")
        
        if nepostojeci:
            result2 = ", ".join(map(str, nepostojeci))
        else:
            result2 = "Све је у реду."

        input_field2.config(state="normal")
        input_field2.delete("1.0", tk.END)
        input_field2.insert("1.0", result2)
        input_field2.config(state="disabled")

    except Exception as e:
        
        messagebox.showerror("Грешка", str(e))

root = TkinterDnD.Tk()
root.title("Excel Comparator")
root.geometry("800x600")

top_frame = tk.Frame(root, height=400)
bottom_frame = tk.Frame(root, height=200)

top_frame.pack(side="top", fill="both", expand=True)
bottom_frame.pack(side="bottom", fill="both", expand=True)

left_top = tk.Frame(top_frame, padx=10, pady=10)
right_top = tk.Frame(top_frame, padx=10, pady=10)

left_top.pack(side="left", fill="both", expand=True)
right_top.pack(side="right", fill="both", expand=True)

tk.Label(left_top, text="Овде превуци SEF Excel датотеку").pack()
small_box_left = tk.Label(left_top, width=40, height=15, bg="white", relief="solid", text="+", font=("Arial", 10), anchor="center")
small_box_left.pack(pady=10)
small_box_left.drop_target_register(DND_FILES)
small_box_left.dnd_bind('<<Drop>>', handle_drop_left)
path_sef=tk.Label(left_top,text="Putanja do file-a")
path_sef.pack()

tk.Label(right_top, text="Овде превуци Excel датотеку за проверу").pack()
small_box_right = tk.Label(right_top, width=40, height=15, bg="white", relief="solid", text="+", font=("Arial", 10), anchor="center")
small_box_right.pack(pady=10)
small_box_right.drop_target_register(DND_FILES)
small_box_right.dnd_bind('<<Drop>>', handle_drop_right)

path_comp=tk.Label(right_top,text="Putanja do file-a")
path_comp.pack()

left_btm = tk.Frame(bottom_frame, padx=10, pady=10)
right_btm = tk.Frame(bottom_frame, padx=10, pady=10)

left_btm.pack(side="left", fill="both", expand=True)
right_btm.pack(side="right", fill="both", expand=True)

tk.Label(left_btm, text="Неподударни ID-jevi").pack(pady=(10, 5))

scrollbar = tk.Scrollbar(left_btm)
scrollbar.pack(side="right", fill="y")

input_field = tk.Text(
    left_btm,
    width=40,    
    height=8,     
    wrap="word",
    yscrollcommand=scrollbar.set,
    state="disabled",
    font=("Arial", 10)
)
input_field.pack(side="left")

scrollbar.config(command=input_field.yview)

tk.Label(right_btm, text="Непостојећи ID-jevi").pack(pady=(10, 5))
scrollbar2 = tk.Scrollbar(right_btm)
scrollbar2.pack(side="right", fill="y")
input_field2 = tk.Text(
    right_btm,
    width=40,    
    height=8,     
    wrap="word",
    yscrollcommand=scrollbar2.set,
    state="disabled",
    font=("Arial", 10)
)
input_field2.pack(side="right")
scrollbar2.config(command=input_field2.yview)

button_frame = tk.Frame(bottom_frame)
button_frame.pack()

btn1 = tk.Button(button_frame, text="Провери", width=12, state="disabled", command=on_btn1_click)

btn1.pack()
tk.Frame(button_frame, width=20).pack()


root.mainloop()