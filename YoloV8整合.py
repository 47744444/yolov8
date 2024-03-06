import os
import shutil
import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
import cv2
import time
import multiprocessing
multiprocessing.freeze_support()

# model測試
def ModelTest_and_SaveVideo(model,video_path):
    current_time = time.strftime("%m%d%H%M", time.localtime())
    model(video_path, conf=0.5, imgsz=640, save=True, project='模型測試結果', name=current_time)#

# 自動標記
def AutoLabel_to_WillyDone(model,video_path):
    # if int(class_id_entry.get())<0 or int(class_id_entry.get())>1000:
    #     result_label.config(text="請填入合理的類別數")
    #     return
    cap = cv2.VideoCapture(video_path)
    while True:
        seed=int(time.time())
        ret, frame = cap.read()
        if not ret:
            break
        model.predict(source=frame, conf=0.65, project='Willy_temp', name=seed, imgsz=640, save_txt=True, save=True, boxes=False)#, save_crop=True, stream=True
        
    # 設置原始目錄和目標目錄
    source_dir = 'Willy_temp'
    desktop_path = os.path.expanduser("~/Desktop")
    current_time = time.strftime("%m%d%H%M", time.localtime())
    target_dir = os.path.join(desktop_path, f"Label_{current_time}")
    os.makedirs(target_dir,exist_ok=True)
    # 遍歷原始目錄
    for subdir in os.listdir(source_dir):
        subdir_path = os.path.join(source_dir, subdir)
        
        # 檢查是否存在'image0.txt'文件
        txt_file = os.path.join(subdir_path, 'labels', 'image0.txt')
        if os.path.exists(txt_file):
            # 重命名'image0.txt'為子目錄名
            new_txt_file = os.path.join(subdir_path, 'labels', f'{subdir}.txt')
            os.rename(txt_file, new_txt_file)
            
            # # 修改YOLO座標文件中的class id
            # with open(new_txt_file, 'r') as f:
            #     lines = f.readlines()
            # with open(new_txt_file, 'w') as f:
            #     for line in lines:
            #         if line.startswith('0'):
            #             line = f'{new_class_id}' + line[1:]
            #         f.write(line)
            
            # 檢查是否存在'image0.jpg'文件
            jpg_file = os.path.join(subdir_path, 'image0.jpg')
            if os.path.exists(jpg_file):
                # 重命名'image0.jpg'為子目錄名
                new_jpg_file = os.path.join(subdir_path, f'{subdir}.jpg')
                os.rename(jpg_file, new_jpg_file)
                # 移動重命名後的文件到目標目錄
                shutil.move(new_txt_file, os.path.join(target_dir, f'{subdir}.txt'))
                shutil.move(new_jpg_file, os.path.join(target_dir, f'{subdir}.jpg'))
    # 刪除原始目錄
    shutil.rmtree(source_dir)
    print('操作完成')

# 函數：選擇模型文件
def select_model():
    model_path = filedialog.askopenfilename(title="選擇模型文件", 
                                            filetypes=[('模型檔', '*.pt *.onnx *.weight *.torchscript *.pb *.tflite'),('所有類型', '*.*')],
                                            initialdir=os.getcwd()
                                            )
    model_entry.delete(0, tk.END)
    model_entry.insert(0, model_path)

# 函數：選擇視頻文件
def select_video():
    video_path = filedialog.askopenfilename(title="選擇影片檔", 
                                            filetypes=[('影片檔', '*.mp4 *.asf *.avi *.gif *.m4v *.mkv *.mov *.mpeg *.mpg *.ts *.wmv *.webm'),
                                                       ('所有類型', '*.*')
                                                       ],
                                            initialdir=os.getcwd()
                                            )
    video_entry.delete(0, tk.END)
    video_entry.insert(0, video_path)

# 函數：執行自動標記 by mp4
def auto_label():
    result_label.config(text="圖像運算中...")
    # if class_id_entry.get()== "":
    #     result_label.config(text="請指定類別~")
    #     return
    model_path = model_entry.get()
    video_path = video_entry.get()
    # new_class_id = int(class_id_entry.get())  # 獲取用戶輸入的新的class id
    
    if model_path and video_path:
        model = YOLO(model_path)
        AutoLabel_to_WillyDone(model, video_path)
        result_label.config(text="自動標記完成，檔案位於桌面")

# 函數：執行自動標記 by dir
def auto_label_dir():
    result_label.config(text="圖像處理中...")
    # if class_id_entry.get() == "":
    #     result_label.config(text="請指定類別~")
    #     return
    model_path = model_entry.get()
    # new_class_id = int(class_id_entry.get())  # 獲取用戶輸入的新的class id
    directory_path = directory_entry.get()
    
    if model_path and directory_path:
        model = YOLO(model_path)
        
        # 遍歷目錄下的圖片文件
        for root_dir, _, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    image_path = os.path.join(root_dir, file)
                    AutoLabel_to_WillyDone(model, image_path)
                    
        result_label.config(text="自動標記完成")

# 函數：執行模型測試
def model_test():
    result_label.config(text="圖像運算中...")
    model_path = model_entry.get()
    video_path = video_entry.get()
    if model_path and video_path:
        model = YOLO(model_path)
        ModelTest_and_SaveVideo(model, video_path)
        result_label.config(text="模型測試完成")

def select_directory():
    directory_path = filedialog.askdirectory(title="選擇目錄", initialdir=os.getcwd())
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, directory_path)


# 設定python程式路徑，掛載至程式所在的上級目錄
os.chdir(os.path.abspath(os.path.join(os.getcwd(), "..")))

# 建立主視窗
root = tk.Tk()
root.title("自動標記和模型測試工具")

# 標簽和按鈕
# model_label = tk.Label(root, text="選擇模型:")
# model_label.pack()

model_entry = tk.Entry(root, width=50)
model_entry.pack()

browse_model_button = tk.Button(root, text="選擇.pt模型檔", command=select_model)
browse_model_button.pack()

# 註解掉上面的輸入框
# video_entry = tk.Entry(root, width=50)
# video_entry.pack()

browse_video_button = tk.Button(root, text="a.選擇單一影片檔", command=select_video)
browse_video_button.pack(side=tk.LEFT)

auto_label_button = tk.Button(root, text="a. 開始標記", command=auto_label)
auto_label_button.pack(side=tk.LEFT)

model_test_button = tk.Button(root, text="a. 影片辨識效果測試", command=model_test)
model_test_button.pack(side=tk.LEFT)

tk.Label(root, text="").pack()  # 添加一個空的標籤來分隔兩排按鈕

directory_entry = tk.Entry(root, width=50)
directory_entry.pack()

browse_directory_button = tk.Button(root, text="b.選擇圖片檔(請選整個目錄)", command=select_directory)
browse_directory_button.pack(side=tk.LEFT)

auto_label_directory_button = tk.Button(root, text="b. 開始標記", command=auto_label_dir)
auto_label_directory_button.pack(side=tk.LEFT)

result_label = tk.Label(root, text="", fg='#f00')
result_label.pack()

root.mainloop()
