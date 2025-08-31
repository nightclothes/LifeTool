import os
import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from 批量重命名 import batch_rename_tv_series

def create_demo_files():
    """
    创建演示用的测试文件
    
    @return: 创建的测试目录路径
    """
    # 在test目录下创建演示文件夹
    demo_dir = Path(__file__).parent / "演示数据" / "权力的游戏"
    demo_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建各种格式的测试文件
    demo_files = [
        "Game.of.Thrones.S01E01.Winter.Is.Coming.mp4",
        "Game.of.Thrones.S01E02.The.Kingsroad.mkv",
        "Game.of.Thrones.S01E03.Lord.Snow.avi",
        "Game.of.Thrones.S02E01.The.North.Remembers.mp4",
        "Game.of.Thrones.S02E02.The.Night.Lands.mkv",
        "第1季第4集.mp4",
        "第1季第5集.mkv",
        "1x06.avi",
        "1x07.mp4",
        "Season 2 Episode 3.mkv",
        "Season 2 Episode 4.avi",
        "08.mp4",  # 简单数字格式
        "09.mkv",
        "10.avi",
        "unknown_format.mp4",  # 无法识别的格式
        "subtitle.srt",  # 非视频文件
        "poster.jpg",   # 非视频文件
    ]
    
    print(f"在目录 {demo_dir} 中创建演示文件:")
    for filename in demo_files:
        file_path = demo_dir / filename
        file_path.touch()
        print(f"  创建: {filename}")
    
    return demo_dir

def show_files_before_after(demo_dir):
    """
    显示重命名前后的文件对比
    
    @param demo_dir: 演示目录路径
    """
    print(f"\n重命名前的文件列表:")
    files_before = sorted([f.name for f in demo_dir.iterdir() if f.is_file()])
    for i, filename in enumerate(files_before, 1):
        print(f"  {i:2d}. {filename}")
    
    print(f"\n开始执行批量重命名...")
    print("=" * 60)
    
    # 执行批量重命名
    success = batch_rename_tv_series(str(demo_dir))
    
    print("=" * 60)
    print(f"\n重命名后的文件列表:")
    files_after = sorted([f.name for f in demo_dir.iterdir() if f.is_file()])
    for i, filename in enumerate(files_after, 1):
        print(f"  {i:2d}. {filename}")
    
    return success

def main():
    """
    主演示函数
    """
    print("电视剧批量重命名功能演示")
    print("=" * 50)
    
    try:
        # 创建演示文件
        demo_dir = create_demo_files()
        
        # 询问用户是否继续
        print(f"\n演示文件已创建完成！")
        user_input = input("是否开始演示批量重命名功能？(y/n): ").strip().lower()
        
        if user_input in ['y', 'yes', '是', '']:
            # 显示重命名前后对比
            success = show_files_before_after(demo_dir)
            
            if success:
                print(f"\n✓ 演示完成！重命名功能正常工作。")
                print(f"\n演示文件保存在: {demo_dir}")
                print(f"您可以查看该目录来验证重命名结果。")
            else:
                print(f"\n✗ 演示过程中出现错误。")
        else:
            print(f"\n演示已取消。演示文件保存在: {demo_dir}")
            print(f"您可以手动运行以下命令来测试:")
            print(f"  python -c \"from src.批量重命名 import batch_rename_tv_series; batch_rename_tv_series(r'{demo_dir}')\"")
    
    except Exception as e:
        print(f"\n演示过程中发生错误: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main()