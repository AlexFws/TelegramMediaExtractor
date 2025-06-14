
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

MAGIC_BYTES = {
    b'\xFF\xD8\xFF': '.jpg',
    b'\x89PNG': '.png',
    b'\x47\x49\x46\x38': '.gif',
    b'\x25PDF': '.pdf',
    b'\x00\x00\x00': '.mp4',
    b'\x49\x44\x33': '.mp3',
    b'OggS': '.ogg',
    b'\x1A\x45\xDF\xA3': '.mkv',
    b'RIFF': '.avi',
}

def get_extension(file_path):
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)
            for magic, ext in MAGIC_BYTES.items():
                if header.startswith(magic):
                    return ext
    except Exception:
        return None
    return None

def extract_media(source_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    count = 0

    for filename in os.listdir(source_dir):
        filepath = os.path.join(source_dir, filename)
        if os.path.isfile(filepath):
            ext = get_extension(filepath)
            if ext:
                new_filename = f"{filename}{ext}"
                new_path = os.path.join(output_dir, new_filename)
                shutil.copyfile(filepath, new_path)
                count += 1

    return count

def choose_source():
    path = filedialog.askdirectory(title="Выберите папку D877F783D5D3EF8C")
    if path:
        source_var.set(path)

def choose_output():
    path = filedialog.askdirectory(title="Выберите папку для сохранения")
    if path:
        output_var.set(path)

def run_extraction():
    source = source_var.get()
    output = output_var.get()
    if not os.path.isdir(source) or not os.path.isdir(output):
        messagebox.showerror("Ошибка", "Указаны некорректные пути к папкам")
        return

    count = extract_media(source, output)
    messagebox.showinfo("Готово", f"Скопировано файлов: {count}")

# GUI
root = tk.Tk()
root.title("Telegram Media Extractor")
root.geometry("450x200")

source_var = tk.StringVar()
output_var = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Папка с файлами Telegram:").pack(anchor="w")
tk.Entry(frame, textvariable=source_var, width=50).pack(anchor="w")
tk.Button(frame, text="Обзор...", command=choose_source).pack(anchor="w", pady=(0,10))

tk.Label(frame, text="Папка для сохранения:").pack(anchor="w")
tk.Entry(frame, textvariable=output_var, width=50).pack(anchor="w")
tk.Button(frame, text="Обзор...", command=choose_output).pack(anchor="w", pady=(0,10))

btn = tk.Button(frame, text="Начать извлечение", command=run_extraction)
btn.pack(pady=10)

root.mainloop()
