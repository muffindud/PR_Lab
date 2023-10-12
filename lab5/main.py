import hashlib
import json
import re


def hash_file(file_path: str):
    h = hashlib.sha1()

    with open(file_path, 'rb') as file:
        chunk = 0

        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)

    return h.hexdigest()


def copy_file(file_path: str, new_file_path: str):
    with open(file_path, 'rb') as file:
        with open(new_file_path, 'wb') as new_file:
            chunk = 0

            while chunk != b'':
                chunk = file.read(1024)
                new_file.write(chunk)


def main():
    # f1 = "local/duck.png"
    # f2 = "local/new_duck.png"
    duck = open("local/duck.png", "rb")
    new_duck = open("local/new_duck.png", "wb")

    file_id = "!start!cornel@yas@duck.png!end!"
    file_id_binary = file_id.encode("utf-8") + duck.read()
    file_id_decoded = re.search(rb"!start!(.*)!end!", file_id_binary).group(1)

    print(file_id)
    # print(file_id_binary.removeprefix(b'!start!' + file_id_decoded + b'!end!'))
    print(file_id_decoded.decode("utf-8"))

    duck.close()
    new_duck.close()


if __name__ == '__main__':
    main()
