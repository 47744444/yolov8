import tkinter as tk
from tkinter import filedialog
import os

def split_lines_into_txt(input_file, output_dir, video_name):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        
        for i, line in enumerate(lines):
            filename = f"{video_name}_{i+1}.txt"
            with open(os.path.join(output_dir, filename), 'w') as txt_file:
                txt_file.write(line.strip())
    result_label.config(text="檔案已分割完成")

def select_input_file():
    input_file_path = filedialog.askopenfilename(title="選擇輸入檔案", filetypes=[("Text files", "*.txt")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, input_file_path)

def select_output_dir():
    output_dir_path = filedialog.askdirectory(title="選擇輸出目錄")
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(0, output_dir_path)

# 創建主窗口
root = tk.Tk()
root.title("分割資料到txt檔案")

# 標簽和按鈕
input_file_label = tk.Label(root, text="輸入檔案:")
input_file_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

input_file_entry = tk.Entry(root, width=50)
input_file_entry.grid(row=0, column=1, padx=5, pady=5)

input_file_button = tk.Button(root, text="瀏覽", command=select_input_file)
input_file_button.grid(row=0, column=2, padx=5, pady=5)

output_dir_label = tk.Label(root, text="輸出目錄:")
output_dir_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.grid(row=1, column=1, padx=5, pady=5)

output_dir_button = tk.Button(root, text="瀏覽", command=select_output_dir)
output_dir_button.grid(row=1, column=2, padx=5, pady=5)

video_name_label = tk.Label(root, text="影片名稱:")
video_name_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

video_name_entry = tk.Entry(root, width=50)
video_name_entry.grid(row=2, column=1, padx=5, pady=5)

split_button = tk.Button(root, text="分割檔案", command=lambda: split_lines_into_txt(input_file_entry.get(), output_dir_entry.get(), video_name_entry.get()))
split_button.grid(row=3, column=1, padx=5, pady=5)

result_label = tk.Label(root, text="", fg='#f00')
result_label.grid(row=4, column=1, padx=5, pady=5)





root.mainloop()
