import tkinter as tk
from tkinter import scrolledtext
import os
import argparse

class Emulator:
    def __init__(self, root_window, vfs_path, script_path):
        self.root = root_window
        self.root.title("VFS")
        self.root.geometry("800x600")
        main_frame = tk.Frame(self.root, bg="#2d2d2d")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.vfs_path = os.path.abspath(vfs_path)
        self.script_path = os.path.abspath(script_path)

        # Область вывода
        self.output_area = scrolledtext.ScrolledText(
            main_frame,
            bg="#1e1e1e", # Цвет фона
            fg="#d4d4d4", # Цвет текста
            font=("Consolas", 12),
        )
        self.output_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.output_area.configure(state='disabled')  # Поле только для чтения

        # Область ввода
        input_frame = tk.Frame(main_frame, bg="#2d2d2d")
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
        self.write_to_output(f"VFS path: {self.vfs_path}\n")
        self.write_to_output(f"Script path: {self.script_path}\n")

    # Вывод текста
    def write_to_output(self, text):
        self.output_area.configure(state='normal') # Разрешаем редактирование
        self.output_area.insert(tk.END, text) # Вставляем текст в конец
        self.output_area.configure(state='disabled') # Запрещаем редактирование

    # Обработчик нажатия Enter
    def handle_command(self, event):
        command_line = self.input_entry.get()
        if not command_line:
            return
        self.write_to_output(f"> {command_line}\n")
        self.input_entry.delete(0, tk.END)
        if not self.execute_command(command_line):
            self.write_to_output("Execution stopped due to error.\n")
            return "break"

    # Вынесено сюда
    def execute_command(self, command_line):
        if command_line.startswith('%'):
            var_name = command_line[1:]
            var_value = os.environ.get(var_name)
            if var_value is not None:
                self.write_to_output(var_value + "\n")
                return True
            else:
                self.write_to_output(f"Error: environment variable {var_name} not found\n")
                return False

        command_name, *args = command_line.split()
        match command_name:
            case "ls":
                self.write_to_output(f"ls {args}\n")
                return True
            case "cd":
                self.write_to_output(f"cd {args}\n")
                return True
            case "exit":
                self.root.destroy()
                return True
            case _:
                self.write_to_output(f"Error: command not found: {command_name}\n")
                return True

    def run_script(self):
        if os.path.exists(self.script_path): # Проверяем, существует ли файл скрипта
            with open(self.script_path, "r") as f: # Открываем файл скрипта для чтения
                for line in f:
                    line = line.strip() #  Убираем пробелы и переносы строки в начале и конце
                    if line:
                        self.write_to_output(f"> {line}\n")
                        if not self.execute_command(line):
                            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VFS Emulator")
    parser.add_argument("--vfs", help="Path to VFS", default="./vfs")
    parser.add_argument("--script", help="Path to start script", default="./start.txt")
    args = parser.parse_args()

    root = tk.Tk()
    app = Emulator(root, vfs_path=args.vfs, script_path=args.script)
    app.run_script()
    root.mainloop()
