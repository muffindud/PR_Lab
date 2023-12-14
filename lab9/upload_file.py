import ftplib
import sys


def main():
    ftp = ftplib.FTP("138.68.98.108")
    ftp.login("yourusername", "yourusername")
    ftp.cwd("~/faf213/CorneliuCatlabuga")
    with open(sys.argv[1], "rb") as file:
        ftp.storbinary("STOR " + sys.argv[1], file)
        print("Uploaded file successfully!")
        print("ftp://yourusername:yourusername@" + ftp.host + "/faf213/CorneliuCatlabuga/" + sys.argv[1])
        file.close()
    ftp.quit()


if __name__ == "__main__":
    main()
