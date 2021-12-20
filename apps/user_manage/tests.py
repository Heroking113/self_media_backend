import base64

if __name__ == '__main__':

    name = 'heroking'
    nickname_encoder = base64.b64encode(name.encode("utf-8"))
    str_nickname = nickname_encoder.decode('utf-8')
    rname = base64.b64decode(str_nickname).decode('utf-8')
    print(nickname_encoder)
    print(str_nickname)
    print(rname)
