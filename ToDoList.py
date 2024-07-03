import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json

# Functions for To-Do List functionality
def load_tasks(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks, file_path):
    with open(file_path, 'w') as file:
        json.dump(tasks, file)

def add_task(tasks, task_description):
    task = {
        'description': task_description,
        'completed': False
    }
    tasks.append(task)
    save_tasks(tasks, 'tasks.json')
    refresh_tasks()
    task_entry.delete(0, tk.END)

def mark_task_completed(tasks, index):
    tasks[index]['completed'] = not tasks[index]['completed']
    save_tasks(tasks, 'tasks.json')
    refresh_tasks()

def delete_task(tasks, index):
    tasks.pop(index)
    save_tasks(tasks, 'tasks.json')
    refresh_tasks()

def refresh_tasks():
    task_listbox.delete(*task_listbox.get_children())
    for i, task in enumerate(tasks):
        status = "Done" if task['completed'] else "Not Done"
        task_listbox.insert('', 'end', iid=i, values=(task['description'], status))

# GUI Setup
def setup_gui():
    root = tk.Tk()
    root.title("To-Do List")
    root.geometry("400x400")
    root.configure(bg="#f0f0f0")

    style = ttk.Style()
    style.configure("Treeview", background="#f0f0f0", foreground="black", rowheight=25, fieldbackground="#f0f0f0")
    style.map('Treeview', background=[('selected', '#347083')])

    title_label = tk.Label(root, text="My To-Do List", font=("Helvetica", 18), bg="#f0f0f0")
    title_label.pack(pady=10)

    global task_listbox
    task_listbox = ttk.Treeview(root, columns=("Task", "Status"), show="headings")
    task_listbox.heading("Task", text="Task")
    task_listbox.heading("Status", text="Status")
    task_listbox.column("Task", width=250)
    task_listbox.column("Status", width=100)
    task_listbox.pack(pady=10)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=task_listbox.yview)
    task_listbox.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    global task_entry
    task_entry = tk.Entry(root, width=30)
    task_entry.pack(pady=10)

    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=10)

    add_button = tk.Button(button_frame, text="Add Task", command=lambda: add_task(tasks, task_entry.get()), bg="#4CAF50", fg="white", padx=10, pady=5)
    add_button.grid(row=0, column=0, padx=5)

    complete_button = tk.Button(button_frame, text="Mark Completed", command=lambda: mark_task_completed(tasks, int(task_listbox.selection()[0])), bg="#2196F3", fg="white", padx=10, pady=5)
    complete_button.grid(row=0, column=1, padx=5)

    delete_button = tk.Button(button_frame, text="Delete Task", command=lambda: delete_task(tasks, int(task_listbox.selection()[0])), bg="#f44336", fg="white", padx=10, pady=5)
    delete_button.grid(row=0, column=2, padx=5)

    return root

# Load tasks and initialize GUI
file_path = 'tasks.json'
tasks = load_tasks(file_path)
root = setup_gui()
refresh_tasks()

root.mainloop()
