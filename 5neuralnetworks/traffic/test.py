from traffic import platform_independent_directory


def main():
    path1 = "/home/usr/kole/bin/python"
    path2 = "C:\\Documents\\Newsletters\\Summer2018.pdf"
    print(platform_independent_directory(path1))
    print(platform_independent_directory(path2))


if __name__ == "__main__":
    main()
