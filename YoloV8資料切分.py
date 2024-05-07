import tkinter as tk
from tkinter import filedialog
import os
import random
import shutil

# 函數來選擇資料夾
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        feedback_label.config(text="處理中...")
        process_dataset(folder_path)

# 函數來處理資料集
def process_dataset(folder_path):
    image_files = []
    txt_files = []

    # 找到所有圖片和txt座標檔
    for file in os.listdir(folder_path):
        if file.endswith(".jpg") or file.endswith(".png"):
            image_files.append(file)
        elif file.endswith(".txt"):
            txt_files.append(file)

    # 隨機劃分資料集
    random.shuffle(image_files)
    num_samples = len(image_files)
    train_split = int(0.7 * num_samples)
    valid_split = int(0.2 * num_samples)

    train_set = image_files[:train_split]
    valid_set = image_files[train_split:train_split + valid_split]
    test_set = image_files[train_split + valid_split:]

    # 創建子目錄結構
    os.makedirs(os.path.join(folder_path, "train", "images"), exist_ok=True)
    os.makedirs(os.path.join(folder_path, "train", "labels"), exist_ok=True)
    os.makedirs(os.path.join(folder_path, "vaild", "images"), exist_ok=True)
    os.makedirs(os.path.join(folder_path, "vaild", "labels"), exist_ok=True)
    os.makedirs(os.path.join(folder_path, "test", "images"), exist_ok=True)
    os.makedirs(os.path.join(folder_path, "test", "labels"), exist_ok=True)

    # 將檔案複製到子目錄
    for file in train_set:
        shutil.move(os.path.join(folder_path, file), os.path.join(folder_path, "train", "images", file))
        txt_file = file.replace(".jpg", ".txt")
        if txt_file in txt_files:
            shutil.move(os.path.join(folder_path, txt_file), os.path.join(folder_path, "train", "labels", txt_file))

    for file in valid_set:
        shutil.move(os.path.join(folder_path, file), os.path.join(folder_path, "vaild", "images", file))
        txt_file = file.replace(".jpg", ".txt")
        if txt_file in txt_files:
            shutil.move(os.path.join(folder_path, txt_file), os.path.join(folder_path, "vaild", "labels", txt_file))

    for file in test_set:
        shutil.move(os.path.join(folder_path, file), os.path.join(folder_path, "test", "images", file))
        txt_file = file.replace(".jpg", ".txt")
        if txt_file in txt_files:
            shutil.move(os.path.join(folder_path, txt_file), os.path.join(folder_path, "test", "labels", txt_file))

    feedback_label.config(text="資料集劃分完成！")

# 建立主視窗
root = tk.Tk()
root.geometry("300x100")
root.title("Yolo資料集劃分工具")

# 建立按鈕
select_button = tk.Button(root, text="選擇資料夾", command=select_folder)
select_button.pack(pady=20)

# 添加反饋標籤
feedback_label = tk.Label(root, text="")
feedback_label.pack()

# 啟動主迴圈
root.mainloop()
