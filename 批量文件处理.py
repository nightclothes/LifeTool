# -*- coding: utf-8 -*-
# @Author  : 雷智杰
# @Time    : 2024/10/20 16:27
# @File    : 批量文件重命名
# @Project : LifeTool
# @Software: PyCharm


import os
import re
import shutil


def move_files_to_parent(folder_path):
    """
    将指定目录下的所有文件移动到该目录下（递归）
    :param folder_path: 指定目录
    :return: None
    """
    # 获取文件夹中的所有文件和子文件夹
    for item in os.listdir(folder_path):
        # 构建完整的文件或文件夹路径
        item_path = os.path.join(folder_path, item)

        # 检查是文件还是文件夹
        if os.path.isfile(item_path):
            # 如果是文件，直接移动到父文件夹
            shutil.move(item_path, os.path.join(os.path.dirname(folder_path), item))
            print(f'Moved "{item_path}" to parent folder')
        elif os.path.isdir(item_path):
            # 如果是文件夹，递归调用函数
            move_files_to_parent(item_path)
            # 检查文件夹是否为空，如果为空，则删除空文件夹
            if not os.listdir(item_path):
                os.rmdir(item_path)


def rename_files(directory):
    """
    重命名指定目录下的所有文件
    :param directory: 路径
    :return: None
    """

    s_pattern = re.compile(r'S(\d+)')
    e_pattern = re.compile(r'EP(\d+)')
    e_pattern_ex = re.compile(r'E(\d+)')

    base_name = os.path.basename(directory)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            s_match = s_pattern.search(filename)
            e_match = e_pattern.search(filename)
            e_match_ex = e_pattern_ex.search(filename)

            new_name = base_name
            if s_match:
                s_number = s_match.group(1)
                new_name += f"第{s_number}季"
            if e_match:
                e_number = e_match.group(1)
                new_name += f"第{e_number}集"
            elif e_match_ex:
                e_number_ex = e_match_ex.group(1)
                new_name += f"第{e_number_ex}集"
            else:
                continue
            new_name += os.path.splitext(filename)[1]

            if not new_name == base_name:
                new_file_path = os.path.join(directory, new_name)
                os.rename(file_path, new_file_path)
                print(f'Renamed "{file_path}" to "{new_file_path}"')


def change_extension(directory, new_extension) -> None:
    """
    批量更改指定目录下的所有文件扩展名
    :param directory: 指定目录
    :param new_extension: 新的扩展名
    :return: None
    """

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file_path)
            if ext.lower() != f'.{new_extension.lower()}':
                new_file_path = os.path.splitext(file_path)[0] + f'.{new_extension}'
                os.rename(file_path, new_file_path)
                print(f'Renamed "{file_path}" to "{new_file_path}"')


if __name__ == '__main__':
    directory_path = r'C:\Users\void_pc\Downloads\假如'
    rename_files(directory_path)
