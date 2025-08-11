from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import messagebox
from comparator import start_comparison
from pathlib import Path

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
        full_path = Path(filepath).resolve()
        local_path = "/".join(full_path.parts[-2:])
        path_sef.config(text=".../"+local_path)
        small_box_left.config(bg="#a8d5a2")  # svetlozelena
    validate_button_state()

def handle_drop_right(event):
    filepath = event.data.strip('{}')
    if filepath.endswith(('.xlsx', '.xls')):
        valid_files["right"] = filepath
        full_path = Path(filepath).resolve()
        local_path = "/".join(full_path.parts[-2:])
        path_comp.config(text=".../"+local_path)
        small_box_right.config(bg="#a8d5a2")
    else:
        messagebox.showwarning("Неправилна Excel датотека", "Унесите Excel датотеку у правилном формату (.xlsx или .xls)")
        valid_files["right"] = None
    validate_button_state()

def fill_treeview(tree, data_dict):
    for i in tree.get_children():
        tree.delete(i)
    if not data_dict:
        tree.insert("", "end", values=("Нема података", ""))
        return
    for k, v in data_dict.items():
        tree.insert("", "end", values=(k, v))

def on_btn1_click():
    sef_path = valid_files["left"]
    compare_path = valid_files["right"]

    try:
        nepodudarni_osn_os, nepodudarni_pdv_os, nepodudarni_osn_ns, nepodudarni_pdv_ns, nepostojeci = start_comparison(sef_path, compare_path)

        fill_treeview(tree_nepostojeci, nepostojeci)
        fill_treeview(tree_osn_os, nepodudarni_osn_os)
        fill_treeview(tree_pdv_os, nepodudarni_pdv_os)
        fill_treeview(tree_osn_ns, nepodudarni_osn_ns)
        fill_treeview(tree_pdv_ns, nepodudarni_pdv_ns)

    except Exception as e:
        messagebox.showerror("Грешка", str(e))

root = TkinterDnD.Tk()
root.title("Excel Comparator")
root.geometry("900x650")
root.configure(bg="#f0f0f0")

style = ttk.Style(root)
style.theme_use("clam")

# Stil za Treeview header
style.configure("Treeview.Heading",
                font=("Arial", 11, "bold"),
                background="#34495e",
                foreground="white",
                relief="flat")

# Stil za Treeview redove
style.configure("Treeview",
                font=("Arial", 10),
                background="white",
                foreground="#333",
                fieldbackground="white",
                rowheight=24)
style.map("Treeview",
          background=[("selected", "#2980b9")],
          foreground=[("selected", "white")])

top_frame = tk.Frame(root, bg="#f0f0f0", height=400)
bottom_frame = tk.Frame(root, bg="#f0f0f0", height=250)

top_frame.pack(side="top", fill="both", expand=True)
bottom_frame.pack(side="bottom", fill="both", expand=True)

left_top = tk.Frame(top_frame, padx=10, pady=10, bg="#f0f0f0")
right_top = tk.Frame(top_frame, padx=10, pady=10, bg="#f0f0f0")

left_top.pack(side="left", fill="both", expand=True)
right_top.pack(side="right", fill="both", expand=True)

# Left drag-drop area
tk.Label(left_top, text="Овде превуци SEF Excel датотеку", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
small_box_left = tk.Label(left_top, width=40, height=15, bg="white", relief="solid", text="+", font=("Arial", 10), anchor="center")
small_box_left.pack(pady=10)
small_box_left.drop_target_register(DND_FILES)
small_box_left.dnd_bind('<<Drop>>', handle_drop_left)
path_sef = tk.Label(left_top, text="путanja до SEF датотеке", font=("Arial", 9), bg="#f0f0f0")
path_sef.pack()

# Right drag-drop area
tk.Label(right_top, text="Овде превуци Excel датотеку за проверу", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
small_box_right = tk.Label(right_top, width=40, height=15, bg="white", relief="solid", text="+", font=("Arial", 10), anchor="center")
small_box_right.pack(pady=10)
small_box_right.drop_target_register(DND_FILES)
small_box_right.dnd_bind('<<Drop>>', handle_drop_right)
path_comp = tk.Label(right_top, text="Путanja до датотеке за проверу", font=("Arial", 9), bg="#f0f0f0")
path_comp.pack()

# Bottom section: Button on top and centered
btn1 = tk.Button(bottom_frame, text="Провери", width=15, state="disabled", command=on_btn1_click,
                 font=("Arial", 11, "bold"), bg="#2980b9", fg="white", activebackground="#1c5980", relief="flat")
btn1.pack(pady=(15, 10))
btn1.pack_configure(anchor="center")

# Notebook (tabs) for results below the button, centered with padding
notebook = ttk.Notebook(bottom_frame)
notebook.pack(fill="both", expand=True, padx=30, pady=10)

# Create one tab per category
tabs_info = {
    "Непостојећи ID-eви": None,
    "Неподударни Oсновица OС": None,
    "Неподударни ПДВ OС": None,
    "Неподударни Oсновица НС": None,
    "Неподударни ПДВ НС": None,
}

trees = {}

for tab_name in tabs_info:
    frame = ttk.Frame(notebook, padding=10)
    notebook.add(frame, text=tab_name)

    tree = ttk.Treeview(frame, columns=("ID", "Разлика"), show="headings", selectmode="browse")
    tree.heading("ID", text="ID")
    tree.heading("Разлика", text="Разлика")
    tree.column("ID", anchor="center", width=200)
    tree.column("Разлика", anchor="center", width=500)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    trees[tab_name] = tree

tree_nepostojeci = trees["Непостојећи ID-ови"]
tree_osn_os = trees["Неподударни Oсновица OС"]
tree_pdv_os = trees["Неподударни ПДВ OС"]
tree_osn_ns = trees["Неподударни Oсновица НС"]
tree_pdv_ns = trees["Неподударни ПДВ НС"]

root.mainloop()
