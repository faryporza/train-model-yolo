# YOLO Vehicle Detection Training

ระบบ Training YOLO สำหรับ Vehicle Detection พร้อม Roboflow Integration

## 📁 โครงสร้างโปรเจค

```
train-model-yolo/
├── main.py           # Entry point หลัก - เมนูเลือกโหมด
├── robo.py           # ดาวน์โหลด Dataset จาก Roboflow
├── resume.py         # Resume Training จาก Checkpoint
├── train.py          # Training Logic และ Configuration
├── setup.bat         # Setup script สำหรับ Windows
├── run.bat           # Run script สำหรับ Windows
├── requirements.txt  # Python dependencies
└── README.md         # ไฟล์นี้
```

## 🚀 วิธีใช้งาน

### การติดตั้ง (ครั้งแรก)

1. **ดับเบิลคลิก `setup.bat`** เพื่อติดตั้ง:
   - สร้าง Virtual Environment
   - ติดตั้ง PyTorch with CUDA
   - ติดตั้ง Ultralytics (YOLO)
   - ติดตั้ง Roboflow

### การใช้งาน

1. **ดับเบิลคลิก `run.bat`** หรือรัน:
   ```cmd
   venv\Scripts\activate
   python main.py
   ```

2. **เลือกโหมด:**
   - `[1] เริ่มใหม่หมด` - ดาวน์โหลด Dataset และเริ่ม Training ตั้งแต่ต้น
   - `[2] Resume Training` - ทำ Training ต่อจาก Checkpoint ล่าสุด
   - `[3] Download Dataset Only` - ดาวน์โหลด Dataset อย่างเดียว
   - `[4] Exit` - ออกจากโปรแกรม

## ⚙️ Configuration

### ปรับแต่ง Training Parameters

แก้ไขใน `train.py`:

```python
# Model Configuration
MODEL_NAME = "yolo11n.pt"  # n, s, m, l, x

# Training Hyperparameters
EPOCHS = 100              # จำนวน Epochs
BATCH_SIZE = 16           # ลดลงถ้า GPU หน่วยความจำไม่พอ
IMAGE_SIZE = 640          # ขนาดภาพ
```

### เปลี่ยน Dataset

แก้ไขใน `robo.py`:

```python
ROBOFLOW_API_KEY = "your-api-key"
WORKSPACE_NAME = "your-workspace"
PROJECT_NAME = "your-project"
VERSION_NUMBER = 1
```

## 📊 Output

หลังจาก Training เสร็จสิ้น จะได้:

```
runs/detect/train/
├── weights/
│   ├── best.pt      # Model ที่ดีที่สุด
│   └── last.pt      # Checkpoint ล่าสุด
├── results.png      # กราฟผลลัพธ์
├── confusion_matrix.png
└── ...
```

## 🔧 Requirements

- Windows 10/11
- Python 3.8+
- NVIDIA GPU with CUDA support (แนะนำ)
- อินเทอร์เน็ตสำหรับดาวน์โหลด Dataset

## 📝 Notes

- ถ้า Training หยุดกลางคัน สามารถใช้ Resume ได้
- Model จะ Save อัตโนมัติทุก 10 epochs
- ใช้ `Ctrl+C` เพื่อหยุด Training อย่างปลอดภัย
