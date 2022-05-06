import ctypes
import time
import hashlib
import urllib.request
import os


INTERVAL = 10
TOOTHLESS_HASH = 'e2fc8e63f49adcd9c52f01ce97dd16e233d7e2ffa90350c66ed6a021477e5252'
TOOTHLESS_URL = 'https://i.imgur.com/4rJR98e.png'


def getWallpaper() -> str:
    SPI_GETDESKWALLPAPER = 0x73
    ubuf = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, len(ubuf), ubuf, 0)
    return str(ubuf.value)


def setWallpaper(path) -> None:
    SPI_SETDESKWALLPAPER = 0x14
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDCHANGE = 0x02
    changed = SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, changed)


def check_bakground() -> None:
    wallpaper_path = getWallpaper()
    if not check_hash(wallpaper_path, TOOTHLESS_HASH):
        setWallpaper(wallpaper_path)
    

def get_toothless() -> str:
    urllib.request.urlretrieve(TOOTHLESS_URL, 'toothless.png')
    return os.path.join(os.getcwd(), 'toothless.png')


def check_hash(path: str, hash: str) -> bool:

    sha256 = hashlib.sha256()

    with open(path, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest() == hash
        

def main() -> None:

    while True:
        check_bakground()
        time.sleep(INTERVAL)




if __name__ == "__main__":
    main()

