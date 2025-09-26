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
        # Растягивается по всей ширине и высоте окна
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
        # Делаем поле только для чтения
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
            borderwidth=0,  # Без рамки
            insertbackground="#d4d4d4"
        )
        self.input_entry.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.input_entry.bind("<Return>", self.handle_command)
        self.write_to_output("Welcome to the VFS Emulator!\n")
        self.write_to_output(f"VFS path: {self.vfs_path}\n")
        self.write_to_output(f"Script path: {self.script_path}\n")

    # Вывод текста
    def write_to_output(self, text):
        # Разрешаем редактирование
        self.output_area.configure(state='normal')
        # Вставляем текст в конец
        self.output_area.insert(tk.END, text)
        # Запрещаем редактирование
        self.output_area.configure(state='disabled')

    # Обработчик нажатия Enter
    def handle_command(self, event):
        # Получаем текст из поля ввода
        command_line = self.input_entry.get()
        if not command_line:
            return
        self.write_to_output(f"> {command_line}\n")
        # Очищаем поле ввода
        self.input_entry.delete(0, tk.END)
        if not self.execute_command(command_line):
            self.write_to_output("Error\n")
            return "break"

    # Вынесено сюда
    def execute_command(self, command_line):
        if command_line.startswith('%'):
            var_name = command_line[1:]
             # os.environ словарь переменных окружения операционной системы
            var_value = os.environ.get(var_name)
            if var_value is not None:
                self.write_to_output(var_value + "\n")
                return True
            else:
                self.write_to_output(f"Error: command not found: {var_name}\n")
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
        # Проверяем существует ли файл скрипта
        if os.path.exists(self.script_path):
            # Открываем файл скрипта для чтения
            with open(self.script_path, "r") as f:
                for line in f:
                    # Убираем пробелы и переносы строки в начале и конце
                    line = line.strip()
                    if line:
                        self.write_to_output(f"> {line}\n")
                        if not self.execute_command(line):
                            break


parser = argparse.ArgumentParser()
# Добавляем аргумент --vfs для указания пути к виртуальной файловой системе
parser.add_argument("--vfs", default="./vfs")
# Добавляем аргумент --script для указания пути к стартовому скрипту
parser.add_argument("--script", default="./Skript.txt")
args = parser.parse_args()

root = tk.Tk()
app = Emulator(root, vfs_path=args.vfs, script_path=args.script)
app.run_script()
root.mainloop()
