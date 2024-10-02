# -*- coding: utf-8 -*-
# @Author  : 雷智杰
# @Time    : 2024/10/2 13:23
# @File    : 电视剧重命名
# @Project : LifeTool
# @Software: PyCharm

import os
import re


def rename_files(folder_path):
    # 电视剧名为文件名
    show_name = os.path.basename(folder_path)

    # 正则表达式，用于匹配季和集数
    pattern = re.compile(r'(S\d{2})E(\d{2})')

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        match = pattern.search(filename)
        if match:
            season = match.group(1)  # 匹配到的季数
            episode = match.group(2)  # 匹配到的集数

            # 构建新的文件名
            new_filename = f"{show_name}.S{season[1:]}E{episode}"

            # 获取文件的扩展名
            file_extension = os.path.splitext(filename)[1]

            # 构建完整的新文件名
            new_filename_with_extension = f"{new_filename}{file_extension}"

            # 获取文件的完整路径
            old_file = os.path.join(folder_path, filename)
            new_file = os.path.join(folder_path, new_filename_with_extension)

            # 重命名文件
            os.rename(old_file, new_file)
            print(f"'{filename}' --> '{new_filename_with_extension}'")


if __name__ == '__main__':
    # 指定要遍历的文件夹路径
    folder_path = r'E:\鱿鱼游戏'
    rename_files(folder_path)
