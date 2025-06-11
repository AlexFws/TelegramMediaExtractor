
import os
import shutil

def print_ru(text):
    print(text.encode('cp1251', errors='ignore').decode('cp1251'))

print_ru("=== Telegram Media Extractor ===")
SOURCE_DIR = input("Введите путь к папке D877F783D5D3EF8C: ").strip('"')
OUTPUT_DIR = input("Введите путь, куда сохранить файлы с расширениями: ").strip('"')

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
    with open(file_path, 'rb') as f:
        header = f.read(8)
        for magic, ext in MAGIC_BYTES.items():
            if header.startswith(magic):
                return ext
    return None

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    count = 0

    for filename in os.listdir(SOURCE_DIR):
        filepath = os.path.join(SOURCE_DIR, filename)
        if os.path.isfile(filepath):
            ext = get_extension(filepath)
            if ext:
                new_filename = f"{filename}{ext}"
                new_path = os.path.join(OUTPUT_DIR, new_filename)
                shutil.copyfile(filepath, new_path)
                print_ru(f"✓ {filename} → {new_filename}")
                count += 1
            else:
                print_ru(f"✗ Неизвестный формат: {filename}")

    print_ru(f"Готово! Скопировано файлов: {count}")

if __name__ == '__main__':
    main()
