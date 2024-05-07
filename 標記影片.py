# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 13:19:41 2024

@author: YoloV8
"""

import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
import cv2
import os

def select_video():
    video_path = filedialog.askopenfilename(title="選擇影片檔", 
                                            filetypes=[('影片檔', '*.mp4 *.avi *.mov *.mkv *.flv'),
                                                       ('所有類型', '*.*')
                                                       ],
                                            initialdir="/"
                                            )
    video_entry.delete(0, tk.END)
    video_entry.insert(0, video_path)

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

def mark_video():
    video_path = video_entry.get()
    model_path = model_entry.get()
    output_path = output_entry.get()
    video_name = video_name_entry.get()
    
    if video_path and model_path and output_path:
        yolo = YOLO(model_path)
        cap = cv2.VideoCapture(video_path)
        frame_num = 1
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            

            img_name = f"{video_name}_{frame_num}.jpg"
            img_path = os.path.join(output_path, img_name)
            
            pred = yolo.predict(frame)
            if pred and len(pred) > 0 and len(pred[0]) > 0:
                frame_num += 1
                cv2.imwrite(img_path, frame)
                
        cap.release()
        cv2.destroyAllWindows()
        
        result_label.config(text="影片標記完成，請查看輸出資料夾。")
    else:
        result_label.config(text="請選擇影片檔、模型檔和輸出資料夾")







root = tk.Tk()
root.title("影片標記工具")

# 標簽和按鈕
video_label = tk.Label(root, text="影片檔:")
video_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

video_entry = tk.Entry(root, width=50)
video_entry.grid(row=0, column=1, padx=5, pady=5)

video_button = tk.Button(root, text="瀏覽", command=select_video)
video_button.grid(row=0, column=2, padx=5, pady=5)

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

video_name_label = tk.Label(root, text="影片名稱:")
video_name_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

video_name_entry = tk.Entry(root, width=50)
video_name_entry.grid(row=3, column=1, padx=5, pady=5)


mark_button = tk.Button(root, text="標記影片", command=mark_video)
mark_button.grid(row=4, column=1, padx=5, pady=5)

result_label = tk.Label(root, text="", fg='#f00')
result_label.grid(row=5, column=1, padx=5, pady=5)



root.mainloop()