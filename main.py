"""
Main entry point for YOLO training pipeline
Usage: python main.py
"""
import os
import sys

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print the application banner"""
    print("=" * 60)
    print("       YOLO Vehicle Detection Training Pipeline")
    print("=" * 60)
    print()

def main_menu():
    """Display the main menu and get user choice"""
    print("กรุณาเลือกโหมดการทำงาน (Please select mode):")
    print()
    print("  [1] เริ่มใหม่หมด (Start Fresh)")
    print("      - ดาวน์โหลด Dataset ใหม่จาก Roboflow")
    print("      - เริ่ม Training ใหม่ตั้งแต่ต้น")
    print()
    print("  [2] Resume Training")
    print("      - ทำการ Training ต่อจาก Checkpoint ล่าสุด")
    print("      - ใช้เมื่อ Training หยุดกลางคัน")
    print()
    print("  [3] ดาวน์โหลด Dataset อย่างเดียว (Download Dataset Only)")
    print()
    print("  [4] ออกจากโปรแกรม (Exit)")
    print()
    
    while True:
        choice = input("เลือกตัวเลือก (Enter choice) [1-4]: ").strip()
        if choice in ['1', '2', '3', '4']:
            return int(choice)
        print("❌ กรุณาเลือก 1, 2, 3 หรือ 4")

def check_gpu():
    """Check if CUDA GPU is available"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"✅ GPU พร้อมใช้งาน: {gpu_name}")
            print(f"   CUDA Version: {torch.version.cuda}")
            return True
        else:
            print("⚠️  ไม่พบ GPU - จะใช้ CPU ในการ Training (ช้ากว่ามาก)")
            return False
    except ImportError:
        print("❌ ไม่พบ PyTorch - กรุณารัน setup.bat ก่อน")
        return False

def main():
    """Main function"""
    clear_screen()
    print_banner()
    
    # Check GPU availability
    print("🔍 ตรวจสอบ GPU...")
    check_gpu()
    print()
    
    choice = main_menu()
    
    if choice == 1:
        # Start Fresh - Download dataset and train from scratch
        print("\n" + "=" * 60)
        print("🚀 เริ่มต้นใหม่ทั้งหมด...")
        print("=" * 60)
        
        # Step 1: Download dataset
        print("\n📥 Step 1: ดาวน์โหลด Dataset จาก Roboflow...")
        from robo import download_dataset
        dataset_path = download_dataset()
        
        if dataset_path:
            # Step 2: Start training
            print("\n🏋️ Step 2: เริ่ม Training...")
            from train import start_training
            start_training(dataset_path, resume=False)
        else:
            print("❌ ไม่สามารถดาวน์โหลด Dataset ได้")
            sys.exit(1)
            
    elif choice == 2:
        # Resume Training
        print("\n" + "=" * 60)
        print("🔄 Resume Training จาก Checkpoint...")
        print("=" * 60)
        
        from resume import resume_training
        resume_training()
        
    elif choice == 3:
        # Download Dataset Only
        print("\n" + "=" * 60)
        print("📥 ดาวน์โหลด Dataset...")
        print("=" * 60)
        
        from robo import download_dataset
        dataset_path = download_dataset()
        
        if dataset_path:
            print(f"\n✅ Dataset ถูกดาวน์โหลดที่: {dataset_path}")
        else:
            print("❌ ไม่สามารถดาวน์โหลด Dataset ได้")
            
    elif choice == 4:
        print("\n👋 ขอบคุณที่ใช้งาน!")
        sys.exit(0)

if __name__ == "__main__":
    main()
