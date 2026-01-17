"""
Roboflow Dataset Download Module
Downloads the Vehicle Detection dataset from Roboflow
"""
import os

# Roboflow Configuration
ROBOFLOW_API_KEY = "xWmGZqldGGdVHAeTBz8b"
WORKSPACE_NAME = "thaidetec"
PROJECT_NAME = "vehicle-detection-yg4le"
VERSION_NUMBER = 13
DATASET_FORMAT = "yolov11"
DOWNLOAD_LOCATION = "./data"  # แนะนำให้เป็น path สั้นมากบน Windows เช่น C:\yolo\data

def download_dataset(force_download: bool = False) -> str | None:
    """
    Download dataset from Roboflow
    
    Args:
        force_download: If True, download even if dataset already exists
        
    Returns:
        Path to the downloaded dataset, or None if failed
    """
    try:
        from roboflow import Roboflow
    except ImportError:
        print("❌ ไม่พบ roboflow package")
        print("   กรุณารัน: pip install roboflow")
        print("   ถ้าใช้ Colab: !pip install roboflow")
        return None
    
    # Check if dataset already exists
    expected_path = os.path.join(os.getcwd(), f"{PROJECT_NAME}-{VERSION_NUMBER}")
    if DOWNLOAD_LOCATION:
        expected_path = os.path.abspath(DOWNLOAD_LOCATION)
    
    if os.path.exists(expected_path) and not force_download:
        print(f"✅ พบ Dataset ที่มีอยู่แล้ว: {expected_path}")
        user_input = input("   ต้องการดาวน์โหลดใหม่หรือไม่? (y/N): ").strip().lower()
        if user_input != 'y':
            print("   ใช้ Dataset ที่มีอยู่")
            return expected_path
    
    print(f"\n📦 กำลังเชื่อมต่อกับ Roboflow...")
    print(f"   Workspace: {WORKSPACE_NAME}")
    print(f"   Project: {PROJECT_NAME}")
    print(f"   Version: {VERSION_NUMBER}")
    print(f"   Format: {DATASET_FORMAT}")
    if DOWNLOAD_LOCATION:
        print(f"   Location: {os.path.abspath(DOWNLOAD_LOCATION)}")
    print()
    
    try:
        # Initialize Roboflow
        rf = Roboflow(api_key=ROBOFLOW_API_KEY)
        
        # Get project
        project = rf.workspace(WORKSPACE_NAME).project(PROJECT_NAME)
        
        # Get version
        version = project.version(VERSION_NUMBER)
        
        # Download dataset
        print("⬇️  กำลังดาวน์โหลด Dataset...")
        if DOWNLOAD_LOCATION:
            dataset = version.download(DATASET_FORMAT, location=DOWNLOAD_LOCATION)
        else:
            dataset = version.download(DATASET_FORMAT)
        
        # Get the actual download location
        dataset_path = dataset.location
        
        print(f"\n✅ ดาวน์โหลดสำเร็จ!")
        print(f"   📁 Location: {dataset_path}")
        
        # Print dataset structure
        print("\n📂 โครงสร้าง Dataset:")
        for item in os.listdir(dataset_path):
            item_path = os.path.join(dataset_path, item)
            if os.path.isdir(item_path):
                file_count = len(os.listdir(item_path))
                print(f"   📁 {item}/ ({file_count} files)")
            else:
                print(f"   📄 {item}")
        
        return dataset_path
        
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {str(e)}")
        print("\n🔧 วิธีแก้ไข:")
        print("   1. ถ้าใช้ Windows ให้ย้ายโปรเจคไป path สั้น เช่น C:\\yolo")
        print("   2. ตั้งค่า DOWNLOAD_LOCATION ให้สั้น เช่น C:\\yolo\\data")
        print("   3. เปิด Long Path Support ใน Windows (ถาวร)")
        print("   4. ตรวจสอบชื่อ Workspace และ Project")
        return None

def get_dataset_info() -> dict:
    """Get information about the configured dataset"""
    return {
        "workspace": WORKSPACE_NAME,
        "project": PROJECT_NAME,
        "version": VERSION_NUMBER,
        "format": DATASET_FORMAT
    }

if __name__ == "__main__":
    # Run standalone for testing
    print("=" * 60)
    print("       Roboflow Dataset Download")
    print("=" * 60)
    print()
    
    dataset_path = download_dataset()
    
    if dataset_path:
        print(f"\n🎉 พร้อมสำหรับ Training ได้ที่: {dataset_path}")
    else:
        print("\n❌ การดาวน์โหลดล้มเหลว")
