import os
import re
from pathlib import Path
import logging
from src.log import get_logger

def batch_rename_tv_series(folder_path):
    """
    批量重命名电视剧文件
    将指定文件夹下的文件重命名为"文件夹名+第x季+第y集"的格式，保持原文件扩展名不变
    
    @param folder_path: 电视剧文件夹的路径
    @return: 重命名结果统计信息
    """
    # 创建日志记录器
    logger = get_logger(logging.INFO, "BatchRename")
    
    try:
        # 转换为Path对象
        folder = Path(folder_path)
        
        if not folder.exists() or not folder.is_dir():
            logger.error(f"文件夹 '{folder_path}' 不存在或不是有效目录")
            return False
        
        # 获取文件夹名称作为电视剧名
        series_name = folder.name
        logger.info(f"开始处理电视剧：{series_name}")
        
        # 获取文件夹中的所有文件
        files = [f for f in folder.iterdir() if f.is_file()]
        
        if not files:
            logger.warning("文件夹中没有找到任何文件")
            return False
        
        renamed_count = 0
        skipped_count = 0
        
        for file_path in files:
            # 获取文件名和扩展名
            file_name = file_path.stem
            file_extension = file_path.suffix
            
            # 跳过非视频文件（可根据需要调整扩展名列表）
            video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.ts', '.rmvb'}
            if file_extension.lower() not in video_extensions:
                logger.debug(f"跳过非视频文件：{file_path.name}")
                skipped_count += 1
                continue
            
            # 尝试从文件名中提取季数和集数
            season, episode = extract_season_episode(file_name)
            
            if season is None or episode is None:
                logger.warning(f"无法识别季集信息，跳过文件：{file_path.name}")
                skipped_count += 1
                continue
            
            # 生成新的文件名
            new_name = f"{series_name} 第{season}季 第{episode}集{file_extension}"
            new_path = folder / new_name
            
            # 检查新文件名是否已存在
            if new_path.exists() and new_path != file_path:
                logger.warning(f"目标文件已存在，跳过：{new_name}")
                skipped_count += 1
                continue
            
            # 重命名文件
            try:
                file_path.rename(new_path)
                logger.info(f"重命名成功：{file_path.name} -> {new_name}")
                renamed_count += 1
            except Exception as e:
                logger.error(f"重命名失败：{file_path.name} - {str(e)}")
                skipped_count += 1
        
        logger.info(f"处理完成！成功重命名：{renamed_count} 个文件，跳过文件：{skipped_count} 个文件")
        
        return True
        
    except Exception as e:
        logger.error(f"处理过程中发生错误：{str(e)}")
        return False

def extract_season_episode(filename):
    """
    从文件名中提取季数和集数
    支持多种常见的命名格式
    
    @param filename: 文件名（不含扩展名）
    @return: (season, episode) 元组，如果无法识别则返回 (None, None)
    """
    # 常见的季集格式模式
    patterns = [
        # S01E01, S1E1 格式
        r'[Ss](\d{1,2})[Ee](\d{1,3})',
        # 第1季第1集 格式
        r'第(\d{1,2})季第(\d{1,3})集',
        # 1x01 格式
        r'(\d{1,2})x(\d{1,3})',
        # Season 1 Episode 1 格式
        r'[Ss]eason\s*(\d{1,2})\s*[Ee]pisode\s*(\d{1,3})',
        # 简单的数字格式，假设单季（01, 02, 03...）
        r'^.*?(\d{2,3}).*?$',
    ]
    
    for i, pattern in enumerate(patterns):
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            if i == len(patterns) - 1:  # 最后一个模式（简单数字）
                # 假设是第1季
                season = 1
                episode = int(match.group(1))
            else:
                season = int(match.group(1))
                episode = int(match.group(2))
            
            return season, episode
    
    return None, None

def main():
    """
    主函数，用于测试批量重命名功能
    """
    # 创建日志记录器
    logger = get_logger(logging.INFO, "BatchRenameMain")
    
    logger.info("电视剧文件批量重命名工具启动")
    logger.info("=" * 30)
    
    # 获取用户输入的文件夹路径
    folder_path = input("请输入电视剧文件夹路径：").strip()
    
    if not folder_path:
        logger.error("路径不能为空！")
        return
    
    # 执行批量重命名
    success = batch_rename_tv_series(folder_path)
    
    if success:
        logger.info("重命名操作完成！")
    else:
        logger.error("重命名操作失败！")

if __name__ == "__main__":
    main()