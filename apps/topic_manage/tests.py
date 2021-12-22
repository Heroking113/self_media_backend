import os


if __name__ == '__main__':

    root_path = '/Users/heroking/Documents/convertible_bond/cb_backend/media/tmp_avatars/'
    files = os.listdir(root_path)
    for f in files:
        print(f)

