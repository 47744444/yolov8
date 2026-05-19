🎯 YOLOv8 影像辨識專案 (YOLOv8 Vision Project)

本專案基於 Ultralytics YOLOv8 模型，架設完整的電腦視覺工作流，包含資料庫準備、模型訓練、評估以及預測推論。

---

## 🛠️ 功能特點 (Features)

* **多任務支援**：支援目標檢測 (Detection)、實例分割 (Segmentation) 與姿勢估計 (Pose)。
* **即時推論**：支援圖片、影片以及 WebCam 即時串流偵測。
* **導出多格式**：可將模型導出為 ONNX、TensorRT、TFLite 等格式以利部署。

---

## 📦 環境需求 (Prerequisites)

* Python 3.8+
* CUDA 11.x / 12.x (建議使用 GPU 以加速訓練)
* PyTorch (已安裝對應的 CUDA 版本)

---

## ⚙️ 快速開始 (Quick Start)

### 1. 複製專案庫與安裝依賴
```bash
git clone https://github.com
cd yolov8-project
pip install -r requirements.txt
```

### 2. 安裝 Ultralytics 套件
```bash
pip install ultralytics
```

---

## 📂 資料集準備 (Dataset Setup)

請將您的資料集（YOLO 格式）放置於專案根目錄下，結構如下：

```text
dataset/
├── data.yaml              # 資料集設定檔 (必填)
├── train/
│   ├── images/            # 訓練集圖片
│   └── labels/            # 訓練集標籤 (.txt)
└── val/
    ├── images/            # 驗證集圖片
    └── labels/            # 驗證集標籤 (.txt)
```

### `data.yaml` 範例內容：
```yaml
path: ../dataset            # 資料集根目錄絕對或相對路徑
train: train/images
val: val/images

names:
  0: person
  1: car
  2: dog
```

---

## 🏋️ 模型訓練 (Training)

### 使用命令列 (CLI)
```bash
yolo task=detect mode=train model=yolov8n.pt data=dataset/data.yaml epochs=100 imgsz=640 device=0
```

### 使用 Python 腳本
```python
from ultralytics import YOLO

# 載入預訓練模型
model = YOLO('yolov8n.pt')

# 開始訓練
results = model.train(
    data='dataset/data.yaml',
    epochs=100,
    imgsz=640,
    device=0  # 使用第一個 GPU
)
```

---

## 🔮 模型推論與預測 (Inference)

訓練完成後，權重檔案會儲存在 `runs/detect/train/weights/best.pt`。

### 預測單張圖片
```bash
yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source=path/to/image.jpg show=True
```

### 預測影片或即時鏡頭 (Webcam)
```bash
yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source=0 show=True
```

---

## 📊 模型評估 (Evaluation)

驗證模型在驗證集上的效能表現 (mAP50, mAP50-95)：

```bash
yolo task=detect mode=val model=runs/detect/train/weights/best.pt data=dataset/data.yaml
```

---
