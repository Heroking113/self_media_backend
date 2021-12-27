import base64
import os

def file_name_walk(file_dir):
    file_paths = []
    for root, dirs, files in os.walk(file_dir):
        if '-' in root:
            # print("root", root)  # 当前目录路径
            # print("dirs", dirs)  # 当前路径下所有子目录
            # print("files", files)  # 当前路径下所有非目录子文件
            if files:
                for fi in files:
                    rel = root.split('/')[-1]
                    file_paths.append('school_card/'+rel+'/'+fi)
    return file_paths


if __name__ == '__main__':
    path = '/Users/heroking/Documents/convertible_bond/cb_backend/media/school_card/'
    file_name_walk(path)
