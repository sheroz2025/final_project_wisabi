import os

def get_folder_size(path):
    total_size = 0
    file_sizes = []
    
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                size = os.path.getsize(fp)
                total_size += size
                file_sizes.append((fp, size / (1024 * 1024)))  # в MB

    return total_size / (1024 * 1024), sorted(file_sizes, key=lambda x: x[1], reverse=True)

# Путь к папке проекта
project_path = "C:/Users/Lenovo/Desktop/course_project"
total_mb, files_sorted = get_folder_size(project_path)

print(f"\n📁 Общий размер папки course_project: {total_mb:.2f} MB\n")

print("📦 Самые тяжёлые файлы:")
for path, size in files_sorted:
    print(f"{path:<80} {size:.2f} MB")
