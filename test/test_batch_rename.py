import os
import sys
import tempfile
import shutil
from pathlib import Path

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from 批量重命名 import batch_rename_tv_series, extract_season_episode

def create_test_files(test_dir):
    """
    创建测试用的文件
    
    @param test_dir: 测试目录路径
    @return: 创建的测试文件列表
    """
    test_files = [
        # 标准格式
        "S01E01.mp4",
        "S01E02.mkv",
        "S02E01.avi",
        "S02E10.mp4",
        
        # 中文格式
        "第1季第1集.mp4",
        "第1季第5集.mkv",
        "第2季第3集.avi",
        
        # 数字x数字格式
        "1x01.mp4",
        "1x05.mkv",
        "2x03.avi",
        
        # Season Episode格式
        "Season 1 Episode 1.mp4",
        "Season 2 Episode 5.mkv",
        
        # 简单数字格式
        "01.mp4",
        "05.mkv",
        "10.avi",
        
        # 无法识别的格式
        "random_name.mp4",
        "movie.mkv",
        "episode.avi",
        
        # 非视频文件
        "readme.txt",
        "subtitle.srt",
        "poster.jpg",
    ]
    
    created_files = []
    for filename in test_files:
        file_path = test_dir / filename
        # 创建空文件
        file_path.touch()
        created_files.append(file_path)
        print(f"创建测试文件: {filename}")
    
    return created_files

def test_extract_season_episode():
    """
    测试季集信息提取功能
    
    @return: 测试结果
    """
    print("\n=== 测试季集信息提取功能 ===")
    
    test_cases = [
        # (输入文件名, 期望的(季数, 集数))
        ("S01E01", (1, 1)),
        ("S02E10", (2, 10)),
        ("s03e05", (3, 5)),
        ("第1季第1集", (1, 1)),
        ("第2季第15集", (2, 15)),
        ("1x01", (1, 1)),
        ("2x10", (2, 10)),
        ("Season 1 Episode 1", (1, 1)),
        ("Season 2 Episode 5", (2, 5)),
        ("01", (1, 1)),  # 简单数字格式，默认第1季
        ("15", (1, 15)),
        ("random_name", (None, None)),  # 无法识别
        ("movie", (None, None)),  # 无法识别
    ]
    
    passed = 0
    failed = 0
    
    for filename, expected in test_cases:
        result = extract_season_episode(filename)
        if result == expected:
            print(f"✓ {filename} -> {result}")
            passed += 1
        else:
            print(f"✗ {filename} -> {result}, 期望: {expected}")
            failed += 1
    
    print(f"\n季集提取测试结果: 通过 {passed}, 失败 {failed}")
    return failed == 0

def test_batch_rename():
    """
    测试批量重命名功能
    
    @return: 测试结果
    """
    print("\n=== 测试批量重命名功能 ===")
    
    # 创建临时测试目录
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir) / "美好的世界"
        test_dir.mkdir()
        
        print(f"创建测试目录: {test_dir}")
        
        # 创建测试文件
        created_files = create_test_files(test_dir)
        
        print(f"\n测试前文件列表:")
        for file_path in sorted(test_dir.iterdir()):
            print(f"  {file_path.name}")
        
        # 执行批量重命名
        print(f"\n开始执行批量重命名...")
        success = batch_rename_tv_series(str(test_dir))
        
        print(f"\n测试后文件列表:")
        renamed_files = []
        for file_path in sorted(test_dir.iterdir()):
            print(f"  {file_path.name}")
            renamed_files.append(file_path.name)
        
        # 验证重命名结果
        expected_renames = [
            "美好的世界 第1季 第1集.mp4",
            "美好的世界 第1季 第2集.mkv",
            "美好的世界 第2季 第1集.avi",
            "美好的世界 第2季 第10集.mp4",
            "美好的世界 第1季 第5集.mkv",
            "美好的世界 第2季 第3集.avi",
        ]
        
        print(f"\n验证重命名结果:")
        validation_passed = True
        
        # 检查期望的重命名文件是否存在
        for expected_name in expected_renames:
            if expected_name in renamed_files:
                print(f"✓ 找到期望文件: {expected_name}")
            else:
                print(f"✗ 未找到期望文件: {expected_name}")
                validation_passed = False
        
        # 检查应该被跳过的文件
        skipped_files = ["readme.txt", "subtitle.srt", "poster.jpg"]
        for skipped_file in skipped_files:
            if skipped_file in renamed_files:
                print(f"✓ 非视频文件被正确跳过: {skipped_file}")
            else:
                print(f"✗ 非视频文件丢失: {skipped_file}")
                validation_passed = False
        
        return success and validation_passed

def test_edge_cases():
    """
    测试边界情况
    
    @return: 测试结果
    """
    print("\n=== 测试边界情况 ===")
    
    # 测试不存在的目录
    print("测试不存在的目录...")
    result1 = batch_rename_tv_series("C:\\不存在的目录")
    print(f"不存在目录测试结果: {not result1}")
    
    # 测试空目录
    with tempfile.TemporaryDirectory() as temp_dir:
        empty_dir = Path(temp_dir) / "空目录"
        empty_dir.mkdir()
        print(f"\n测试空目录: {empty_dir}")
        result2 = batch_rename_tv_series(str(empty_dir))
        print(f"空目录测试结果: {not result2}")
    
    return (not result1) and (not result2)

def main():
    """
    主测试函数
    """
    print("电视剧批量重命名功能测试")
    print("=" * 50)
    
    # 运行所有测试
    test1_passed = test_extract_season_episode()
    test2_passed = test_batch_rename()
    test3_passed = test_edge_cases()
    
    # 汇总测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print(f"季集提取测试: {'通过' if test1_passed else '失败'}")
    print(f"批量重命名测试: {'通过' if test2_passed else '失败'}")
    print(f"边界情况测试: {'通过' if test3_passed else '失败'}")
    
    all_passed = test1_passed and test2_passed and test3_passed
    print(f"\n总体测试结果: {'全部通过' if all_passed else '存在失败'}")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)