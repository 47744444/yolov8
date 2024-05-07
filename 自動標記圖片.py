import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
import cv2
import os

def select_image_folder():
    image_folder_path = filedialog.askdirectory(title="選擇圖片資料夾", initialdir="/")
    image_entry.delete(0, tk.END)
    image_entry.insert(0, image_folder_path)

def select_model():
    model_path = filedialog.askopenfilename(title="選擇模型檔", 
                                            filetypes=[('模型檔', '*.pt *.onnx *.weights *.tflite'),
                                                       ('所有類型', '*.*')
                                                       ],
                                            initialdir="/"
                                            )
    model_entry.delete(0, tk.END)
    model_entry.insert(0, model_path)

def select_output():
    output_path = filedialog.askdirectory(title="選擇輸出資料夾", initialdir="/")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_path)

def mark_images():
    image_folder_path = image_entry.get()
    model_path = model_entry.get()
    output_path = output_entry.get()
    i=0
    if image_folder_path and model_path and output_path:
        yolo = YOLO(model_path)
        for filename in os.listdir(image_folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(image_folder_path, filename)
                image = cv2.imread(image_path)
                
                pred = yolo.predict(image)
                if pred and len(pred) > 0 and len(pred[0]) > 0:
                    for  bbox in enumerate(pred):
                        i=i+1
                        cv2.imwrite(os.path.join(output_path, f"frame10{i}.jpg"), image)
                        
        
        result_label.config(text="圖片標記完成，請查看輸出資料夾。")
    else:
        result_label.config(text="請選擇圖片資料夾、模型檔和輸出資料夾")


# 創建主窗口
root = tk.Tk()
root.title("圖片標記工具")

# 標簽和按鈕
image_label = tk.Label(root, text="圖片資料夾:")
image_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

image_entry = tk.Entry(root, width=50)
image_entry.grid(row=0, column=1, padx=5, pady=5)

image_button = tk.Button(root, text="瀏覽", command=select_image_folder)
image_button.grid(row=0, column=2, padx=5, pady=5)

model_label = tk.Label(root, text="模型檔:")
model_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

model_entry = tk.Entry(root, width=50)
model_entry.grid(row=1, column=1, padx=5, pady=5)

model_button = tk.Button(root, text="瀏覽", command=select_model)
model_button.grid(row=1, column=2, padx=5, pady=5)

output_label = tk.Label(root, text="輸出資料夾:")
output_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

output_entry = tk.Entry(root, width=50)
output_entry.grid(row=2, column=1, padx=5, pady=5)

output_button = tk.Button(root, text="瀏覽", command=select_output)
output_button.grid(row=2, column=2, padx=5, pady=5)

mark_button = tk.Button(root, text="標記圖片", command=mark_images)
mark_button.grid(row=3, column=1, padx=5, pady=5)

result_label = tk.Label(root, text="", fg='#f00')
result_label.grid(row=4, column=1, padx=5, pady=5)

root.mainloop()
