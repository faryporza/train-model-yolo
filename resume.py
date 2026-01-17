"""
Resume Training Module
Handles resuming training from the last checkpoint
"""
import os
import glob
from pathlib import Path

# Training configuration
RUNS_DIR = "runs/detect"
WEIGHTS_DIR = "weights"

def find_latest_checkpoint() -> tuple[str | None, str | None]:
    """
    Find the latest training checkpoint
    
    Returns:
        Tuple of (checkpoint_path, run_name) or (None, None) if not found
    """
    runs_path = Path(RUNS_DIR)
    
    if not runs_path.exists():
        print(f"❌ ไม่พบโฟลเดอร์ {RUNS_DIR}")
        return None, None
    
    # Find all training runs
    train_runs = list(runs_path.glob("train*"))
    
    if not train_runs:
        print("❌ ไม่พบประวัติการ Training")
        return None, None
    
    # Sort by modification time (newest first)
    train_runs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    print(f"🔍 พบการ Training {len(train_runs)} ครั้ง:")
    print()
    
    for i, run in enumerate(train_runs[:5], 1):  # Show latest 5
        weights_path = run / WEIGHTS_DIR
        last_pt = weights_path / "last.pt"
        best_pt = weights_path / "best.pt"
        
        status = []
        if last_pt.exists():
            status.append("last.pt ✅")
        if best_pt.exists():
            status.append("best.pt ✅")
        
        status_str = ", ".join(status) if status else "ไม่มี checkpoint"
        print(f"   [{i}] {run.name} - {status_str}")
    
    # Use the latest run
    latest_run = train_runs[0]
    last_checkpoint = latest_run / WEIGHTS_DIR / "last.pt"
    
    if last_checkpoint.exists():
        print(f"\n✅ พบ Checkpoint ล่าสุด: {last_checkpoint}")
        return str(last_checkpoint), latest_run.name
    else:
        print(f"\n⚠️  ไม่พบ last.pt ใน {latest_run.name}")
        return None, None

def resume_training(checkpoint_path: str | None = None):
    """
    Resume training from a checkpoint
    
    Args:
        checkpoint_path: Optional path to specific checkpoint. 
                        If None, uses the latest checkpoint.
    """
    print("\n🔍 กำลังค้นหา Checkpoint...")
    
    if checkpoint_path is None:
        checkpoint_path, run_name = find_latest_checkpoint()
    else:
        run_name = Path(checkpoint_path).parent.parent.name
    
    if checkpoint_path is None:
        print("\n❌ ไม่พบ Checkpoint สำหรับ Resume")
        print("   กรุณาเลือก 'เริ่มใหม่หมด' แทน")
        return False
    
    # Confirm with user
    print(f"\n📋 ข้อมูล Checkpoint:")
    print(f"   Run Name: {run_name}")
    print(f"   Path: {checkpoint_path}")
    
    user_input = input("\n   ต้องการ Resume จาก Checkpoint นี้? (Y/n): ").strip().lower()
    if user_input == 'n':
        print("   ยกเลิกการ Resume")
        return False
    
    # Start resume training
    try:
        from ultralytics import YOLO
        
        print("\n🏋️ กำลังโหลด Model จาก Checkpoint...")
        model = YOLO(checkpoint_path)
        
        print("🚀 เริ่ม Resume Training...")
        print("=" * 60)
        
        # Resume training
        results = model.train(resume=True)
        
        print("\n" + "=" * 60)
        print("✅ Training เสร็จสิ้น!")
        
        return True
        
    except ImportError:
        print("\n❌ ไม่พบ ultralytics package")
        print("   กรุณารัน: pip install ultralytics")
        return False
        
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {str(e)}")
        return False

def list_checkpoints():
    """List all available checkpoints"""
    runs_path = Path(RUNS_DIR)
    
    if not runs_path.exists():
        print("❌ ไม่พบประวัติการ Training")
        return []
    
    checkpoints = []
    
    for run in runs_path.glob("train*"):
        weights_path = run / WEIGHTS_DIR
        
        for weight_file in weights_path.glob("*.pt"):
            checkpoints.append({
                "run": run.name,
                "file": weight_file.name,
                "path": str(weight_file),
                "size_mb": weight_file.stat().st_size / (1024 * 1024),
                "modified": weight_file.stat().st_mtime
            })
    
    return checkpoints

if __name__ == "__main__":
    # Run standalone for testing
    print("=" * 60)
    print("       Resume Training")
    print("=" * 60)
    print()
    
    resume_training()
