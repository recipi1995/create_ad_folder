from ldap3 import Server, Connection, SIMPLE, SYNC, ASYNC, SUBTREE, ALL
import os
import subprocess
import configparser
from pathlib import Path
#############################################<Ядро программы>######################################################
def create_folder():    
    # домен - example.com
    # DNS имя сервера Active Directory
    path = Path(__file__)
    ROOT_DIR = path.parent.absolute()
    config_path = os.path.join(ROOT_DIR, "settings.ini")
    path = config_path
    print(path)
    config = configparser.ConfigParser()
    config.read(path)
    # Читаем некоторые значения из конфиг. файла.
    AD_SERVER = config.get("Settings", "dns_name")
    AD_USER = config.get("Settings", "login_name")
    AD_PASSWORD = config.get("Settings", "password")
    AD_SEARCH_TREE = config.get("Settings", "scheme")
    ABS_PATH = config.get("Settings", "full_path")
    folder = config.get("Settings", "folder")
    FOLDER = folder.split(",")
    print("Start task")

    server = Server(AD_SERVER)
    conn = Connection(server,user=AD_USER,password=AD_PASSWORD)
    conn.bind()
    # в ответ должно быть - True

    
    conn.search(AD_SEARCH_TREE,'(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(givenName=*)(sn=*))',
        SUBTREE,
        attributes =['cn','sAMAccountName']
        )
    # после этого запроса в ответ должно быть - True

    # можно посмотреть на результат
    #print(conn.entries)

    for username in conn.entries:
        strusr=str(username.cn)
        AccountName=str(username.sAMAccountName)
        print(AccountName)
        path = f"{ABS_PATH}{strusr}"
        try:
            os.mkdir(path)
            command0 = subprocess.run(f'icacls "{path}" /T /Q /C /RESET', shell=True, check=True)
            command1 = subprocess.run(f'icacls  "{path}" /inheritance:d', shell=True, check=True)
            command10 = subprocess.run(f'icacls "{path}" /grant "{AD_USER}":(NP)F', shell=True, check=True)
            command2 = subprocess.run(f'icacls "{path}" /grant "comapny\{AccountName}":(NP)F', shell=True, check=True)
            command3 = subprocess.run(f'icacls "{path}" /grant:r "company\Domain Users":R', shell=True, check=True)
            for folder_char in FOLDER:
                path2=f"{ABS_PATH}{strusr}\\{folder_char}"
                os.mkdir(path2)
                command4 = subprocess.run(f'icacls "{path2}" /T /Q /C /RESET', shell=True, check=True)
                command5 = subprocess.run(f'icacls "{path2}" /inheritance:d', shell=True, check=True)
                command6 = subprocess.run(f'icacls "{path2}" /grant "company\Domain Users":RW', shell=True, check=True)
                command7 = subprocess.run(f'icacls "{path2}" /grant "company\{AccountName}":(NP)F', shell=True, check=True)
                command8 = subprocess.run(f'icacls "{path2}" /grant "{AD_USER}":(NP)F', shell=True, check=True)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)
        
    conn.entries

if __name__ == "__main__":
    create_folder()


