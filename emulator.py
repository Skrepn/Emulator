import tkinter as tk
from tkinter import scrolledtext
import os

class Emulator:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("VFS")
        self.root.geometry("800x600")
        main_frame = tk.Frame(self.root, bg="#2d2d2d")
        # Растягивается по всей ширине и высоте окна
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Область вывода
        self.output_area = scrolledtext.ScrolledText(
            main_frame,
            bg="#1e1e1e",  # Цвет фона
            fg="#d4d4d4",  # Цвет текста
            font=("Consolas", 12),
        )
        self.output_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        # Поле только для чтения
        self.output_area.configure(state='disabled')

        # Область ввода
        input_frame = tk.Frame(main_frame, bg="#2d2d2d")
        # Фрейм растягивается по горизонтали
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Метка-приглашение
        prompt_label = tk.Label(
            input_frame,
            text=">",
            bg="#2d2d2d",
            fg="#d4d4d4",
            font=("Consolas", 12)
        )
        prompt_label.pack(side=tk.LEFT, padx=(0, 5))

        # Поле для ввода команд
        self.input_entry = tk.Entry(
            input_frame,
            bg="#1e1e1e",
            fg="#d4d4d4",
            font=("Consolas", 12),
            borderwidth=0,
            insertbackground="#d4d4d4"
        )
        self.input_entry.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.input_entry.bind("<Return>", self.handle_command)
        self.write_to_output("Welcome to the VFS Emulator!\n")

    def write_to_output(self, text):
        # Разрешаем редактирование
        self.output_area.configure(state='normal')
        # Вставляем текст в конец
        self.output_area.insert(tk.END, text)
        # Запрещаем редактирование
        self.output_area.configure(state='disabled')

    def handle_command(self, event):
        # Получаем текст из поля ввода
        command_line = self.input_entry.get()
        if not command_line:
            return

        self.write_to_output(f"> {command_line}\n")
        self.input_entry.delete(0, tk.END)

        if command_line.startswith('$'):
            var_name = command_line[1:]
             # os.environ словарь переменных окружения операционной системы
            var_value = os.environ.get(var_name, command_line)
            self.write_to_output(var_value + "\n")
            return

        command_name, *args = command_line.split()

        match command_name:
            case "ls":
                self.write_to_output(f"ls {args}\n")
            case "cd":
                self.write_to_output(f"cd {args}\n")
            case "exit":
                self.root.destroy()
            case _:
                self.write_to_output(f"Error: command not found: {command_name}\n")

# Создаём главное окно
root = tk.Tk()
app = Emulator(root)
root.mainloop()
