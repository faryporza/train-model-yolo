"""
Training Module
Handles YOLO model training with configurable parameters
"""
import os
from pathlib import Path

# =============================================================================
# TRAINING CONFIGURATION - ปรับแต่งค่าที่นี่
# =============================================================================

# Model Configuration
MODEL_NAME = "yolo11n.pt"  # Options: yolo11n.pt, yolo11s.pt, yolo11m.pt, yolo11l.pt, yolo11x.pt

# Training Hyperparameters
EPOCHS = 100              # จำนวน Epochs
BATCH_SIZE = 16           # Batch size (ลดลงถ้า GPU memory ไม่พอ)
IMAGE_SIZE = 640          # ขนาดภาพ (640 หรือ 1280)
PATIENCE = 50             # จำนวน epochs ที่จะหยุดถ้าไม่มีการปรับปรุง

# Device Configuration
DEVICE = 0                # GPU ID (0 = GPU แรก, 'cpu' = ใช้ CPU)

# Output Configuration
PROJECT_NAME = "runs/detect"
RUN_NAME = "train"        # ชื่อ run (จะถูกเพิ่มเลขอัตโนมัติ ถ้าซ้ำ)

# Advanced Settings
WORKERS = 8               # จำนวน workers สำหรับ data loading
CACHE = True              # Cache images สำหรับเร็วขึ้น
AMP = True                # Automatic Mixed Precision (ใช้ memory น้อยลง)

# =============================================================================

def get_data_yaml(dataset_path: str) -> str:
    """Find the data.yaml file in the dataset"""
    data_yaml = Path(dataset_path) / "data.yaml"
    
    if data_yaml.exists():
        return str(data_yaml)
    
    # Try alternative names
    for name in ["data.yaml", "dataset.yaml", "config.yaml"]:
        yaml_path = Path(dataset_path) / name
        if yaml_path.exists():
            return str(yaml_path)
    
    raise FileNotFoundError(f"ไม่พบ data.yaml ใน {dataset_path}")

def print_training_config(dataset_path: str):
    """Print the training configuration"""
    print("\n📋 Training Configuration:")
    print("=" * 60)
    print(f"   Model:      {MODEL_NAME}")
    print(f"   Dataset:    {dataset_path}")
    print(f"   Epochs:     {EPOCHS}")
    print(f"   Batch Size: {BATCH_SIZE}")
    print(f"   Image Size: {IMAGE_SIZE}")
    print(f"   Device:     {DEVICE}")
    print(f"   AMP:        {AMP}")
    print("=" * 60)

def start_training(dataset_path: str, resume: bool = False):
    """
    Start YOLO training
    
    Args:
        dataset_path: Path to the dataset directory
        resume: Whether to resume from last checkpoint
    """
    try:
        from ultralytics import YOLO
    except ImportError:
        print("❌ ไม่พบ ultralytics package")
        print("   กรุณารัน: pip install ultralytics")
        return False
    
    # Find data.yaml
    try:
        data_yaml = get_data_yaml(dataset_path)
        print(f"✅ พบ data.yaml: {data_yaml}")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return False
    
    # Print configuration
    print_training_config(dataset_path)
    
    # Confirm with user
    user_input = input("\n   ต้องการเริ่ม Training? (Y/n): ").strip().lower()
    if user_input == 'n':
        print("   ยกเลิกการ Training")
        return False
    
    try:
        # Load model
        print(f"\n📦 กำลังโหลด Model: {MODEL_NAME}")
        model = YOLO(MODEL_NAME)
        
        print("\n🚀 เริ่ม Training...")
        print("=" * 60)
        print("   กด Ctrl+C เพื่อหยุด (สามารถ Resume ได้ภายหลัง)")
        print("=" * 60)
        print()
        
        # Start training
        results = model.train(
            data=data_yaml,
            epochs=EPOCHS,
            batch=BATCH_SIZE,
            imgsz=IMAGE_SIZE,
            device=DEVICE,
            project=PROJECT_NAME,
            name=RUN_NAME,
            patience=PATIENCE,
            workers=WORKERS,
            cache=CACHE,
            amp=AMP,
            resume=resume,
            
            # Additional settings
            save=True,           # Save checkpoints
            save_period=10,      # Save every N epochs
            plots=True,          # Generate plots
            verbose=True,        # Verbose output
        )
        
        print("\n" + "=" * 60)
        print("✅ Training เสร็จสิ้น!")
        print("=" * 60)
        
        # Print results location
        print(f"\n📁 ผลลัพธ์อยู่ที่:")
        print(f"   Best Model: {results.save_dir}/weights/best.pt")
        print(f"   Last Model: {results.save_dir}/weights/last.pt")
        print(f"   Results:    {results.save_dir}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Training ถูกหยุด!")
        print("   สามารถ Resume ได้โดยเลือก 'Resume Training' จากเมนูหลัก")
        return False
        
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {str(e)}")
        return False

def validate_model(model_path: str, dataset_path: str):
    """
    Validate a trained model
    
    Args:
        model_path: Path to the trained model (.pt file)
        dataset_path: Path to the dataset
    """
    try:
        from ultralytics import YOLO
        
        print(f"\n🔍 กำลัง Validate Model: {model_path}")
        
        model = YOLO(model_path)
        data_yaml = get_data_yaml(dataset_path)
        
        results = model.val(data=data_yaml)
        
        print("\n📊 Validation Results:")
        print(f"   mAP50:     {results.box.map50:.4f}")
        print(f"   mAP50-95:  {results.box.map:.4f}")
        
        return results
        
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return None

if __name__ == "__main__":
    # Run standalone for testing
    print("=" * 60)
    print("       YOLO Training Module")
    print("=" * 60)
    
    # Check if dataset exists
    from robo import PROJECT_NAME as ROBO_PROJECT, VERSION_NUMBER
    
    dataset_path = f"{ROBO_PROJECT}-{VERSION_NUMBER}"
    
    if os.path.exists(dataset_path):
        start_training(dataset_path)
    else:
        print(f"\n❌ ไม่พบ Dataset: {dataset_path}")
        print("   กรุณาดาวน์โหลด Dataset ก่อน")
