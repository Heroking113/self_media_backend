import eyed3

if __name__ == '__main__':
    mp3_file_path = '/Users/heroking/Documents/convertible_bond/cb_backend/media/zh_1.mp3'
    ret = eyed3.load(mp3_file_path)
    time_secs = int(ret.info.time_secs)
    print(time_secs)