""" 与 flask 无关的功能代码块 """
import os


def all_file_name(file_dir, exclude=None):
    '''
    @description: 获得某路径下的所有py文件名称（不包含后缀）
    @param {str} 路径
    @return: list
    '''
    all_files = []
    for file in os.listdir(file_dir):
        if not file.endswith('.py') or file.startswith('__'):
            continue
        if exclude is not None and file.startswith(exclude):
            continue
        all_files.append(file.replace('.py', ''))
    return all_files
