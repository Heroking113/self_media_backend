import base64


def encode_file_to_base64st(path):
    with open(path, 'rb') as f:
        buffer = base64.b64encode(f.read())
        return str(buffer, encoding="utf-8")

if __name__ == '__main__':
    path = '/Users/heroking/Pictures/pictures/IMG20170707223157.jpg'
    a = encode_file_to_base64st(path)
    print(a)