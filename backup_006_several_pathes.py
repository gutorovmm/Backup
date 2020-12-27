import os
from pathlib import Path
import shutil
import hashlib
import re
from shutil import copy
import datetime

cwd = Path(__file__).parents[0]
os.chdir(cwd)

# В файле записан путь откуда копировать. Получаем его и помещаем в массив:
with open("..\\source_pathes.txt") as f: 
    src_value = list(f)

src_folder = []
for i in range(len(src_value)):
    a = re.sub('\n', '', src_value[i]) # Убирает символ переноса строки (\n) в конце каждого элемента списка
    src_folder.append(a)

# В файле записан путь куда копировать. Получаем его и помещаем в массив:
with open("..\\destination_pathes.txt") as f:
    dest_value = list(f)
    
dest_folder = []
for i in range(len(dest_value)):
    a = re.sub('\n', '', dest_value[i]) # Убирает символ переноса строки (\n) в конце каждого элемента списка
    dest_folder.append(a)

list_of_dest_folders = []
list_of_src_files = []

# Используем os.walk, чтобы обойти все папки по указанному пути и создают два списка:
# Список файлов и список папок.
def file_and_path(path):
    list_of_files = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            list_of_files.append(os.path.join(root, name))      
    return list_of_files

def create_folders(src_path, dest_path):
    list_of_folders = []
    for root, dirs, files in os.walk(src_path, topdown=False):
        for name in dirs:
            list_of_folders.append(os.path.join(root, name))      

    for i in range(len(list_of_folders)):
        os.makedirs(list_of_folders[i].replace(src_path, dest_path), exist_ok=True)
   

# Создаем дерево подпапок, которое содержится по указанному в файле пути. Если какая-то папка уже существует, то пропускаем её.
# Сделать это отдельно нужно потому что функция copy из библиотеки shutil сама все директории по пути файла не создаёт.
for i in range(len(src_folder)):
    create_folders(src_folder[i], dest_folder[i])


list_of_new_dest_files = []
for j in range(len(src_folder)):
    list_of_src_files = []
    list_of_new_dest_files = []
    list_of_src_files = file_and_path(src_folder[j])
    for i in range(len(list_of_src_files)):
        list_of_new_dest_files.append(list_of_src_files[i].replace(src_folder[j], dest_folder[j]))
        if os.path.isfile(list_of_new_dest_files[i]):  # Проверяем, существует ли в целевой директории соответствующий файл. Если нет, то копируем.
            name_src = re.split('\\\\', list_of_src_files[i])[-1]
            name_dest = re.split('\\\\', list_of_new_dest_files[i])[-1]
            if name_dest == name_src: # Проверяем, совпадают ли имена файлов. Если да, то  
                moddate_dest = os.stat(list_of_new_dest_files[i])
                moddate_src = os.stat(list_of_src_files[i])
                if not moddate_dest.st_mtime > moddate_src.st_mtime:    # Если совпадают, то сверяем даты последнего изменения файлов 
                    copy(list_of_src_files[i], list_of_new_dest_files[i])
                    print('duplicated ' + list_of_src_files[i] + ' at ' + str(datetime.datetime.now()))
        else: 
            copy(list_of_src_files[i], list_of_new_dest_files[i]) 
            print('duplicated ' + list_of_src_files[i] + ' at ' + str(datetime.datetime.now()))
        
# Получается единственное условие, при котором цикл ничего не делает - это если совпадают имена файлов и их хэш-суммы.

