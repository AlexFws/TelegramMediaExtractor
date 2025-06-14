
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
    b'PK\x03\x04': '.zip',
    b'Rar!': '.rar',
    b'7z\xBC\xAF\x27\x1C': '.7z',
    b'\xD0\xCF\x11\xE0': '.doc',
    b'\x50\x4B\x03\x04': '.docx',
    b'%!PS': '.ps',
    b'GIF87a': '.gif',
    b'GIF89a': '.gif'
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
    checked = 0

    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.isfile(filepath):
                checked += 1
                ext = get_extension(filepath)
                if ext:
                    new_filename = f"{filename}{ext}"
                    new_path = os.path.join(output_dir, new_filename)
                    shutil.copyfile(filepath, new_path)
                    count += 1

    return count, checked

def choose_source():
    path = filedialog.askdirectory(title="Выберите папку с файлами Telegram")
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

    count, checked = extract_media(source, output)
    if count == 0:
        messagebox.showwarning("Ничего не найдено", f"Проверено файлов: {checked}\nПодходящих медиафайлов не найдено.")
    else:
        messagebox.showinfo("Готово", f"Скопировано файлов: {count} из {checked}")

# GUI
root = tk.Tk()
root.title("Telegram Media Extractor")
root.geometry("500x220")

source_var = tk.StringVar()
output_var = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Папка с файлами Telegram:").pack(anchor="w")
tk.Entry(frame, textvariable=source_var, width=60).pack(anchor="w")
tk.Button(frame, text="Обзор...", command=choose_source).pack(anchor="w", pady=(0,10))

tk.Label(frame, text="Папка для сохранения:").pack(anchor="w")
tk.Entry(frame, textvariable=output_var, width=60).pack(anchor="w")
tk.Button(frame, text="Обзор...", command=choose_output).pack(anchor="w", pady=(0,10))

tk.Button(frame, text="Начать извлечение", command=run_extraction).pack(pady=10)

root.mainloop()
