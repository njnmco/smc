


def colab_map_drive():
    from google.colab import drive
    drive.mount("/content/drive",force_remount=True)

ONET_PATH ="/content/drive/MyDrive/smc/data/onet.sqlite3"

def onet_db(db_path=ONET_PATH):
    import sqlite3
    return sqlite3.connect(db_path)

