from ldap3 import Server, Connection, SIMPLE, SYNC, ASYNC, SUBTREE, ALL
import os
import subprocess
#############################################<Ядро программы>######################################################
def create_folder(AD_SERVER,AD_USER,AD_PASSWORD,AD_SEARCH_TREE,ABS_PATH,FOLDER):    
    # домен - example.com
    # DNS имя сервера Active Directory
    print("Start task")
    AD_SERVER = 'adserver'
    # Пользователь (логин) в Active Directory - нужно указать логин в AD 
    # в формате 'EXAMPLE\aduser' или 'aduser@example.com'
    AD_USER = 'company\\admin'
    AD_PASSWORD = 'password'
    AD_SEARCH_TREE = 'dc=company,dc=local'
    ABS_PATH = ABS_PATH
    FOLDER = FOLDER
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
            command10 = subprocess.run(f'icacls "{path}" /grant "gigant\malyshev":(NP)F', shell=True, check=True)
            command2 = subprocess.run(f'icacls "{path}" /grant "gigant\{AccountName}":(NP)F', shell=True, check=True)
            command3 = subprocess.run(f'icacls "{path}" /grant:r "gigant\it":R', shell=True, check=True)
            for folder_char in FOLDER:
                path2=f"{ABS_PATH}{strusr}\\{folder_char}"
                os.mkdir(path2)
                command4 = subprocess.run(f'icacls "{path2}" /T /Q /C /RESET', shell=True, check=True)
                command5 = subprocess.run(f'icacls "{path2}" /inheritance:d', shell=True, check=True)
                command6 = subprocess.run(f'icacls "{path2}" /grant "gigant\it":RW', shell=True, check=True)
                command7 = subprocess.run(f'icacls "{path2}" /grant "gigant\{AccountName}":(NP)F', shell=True, check=True)
                command8 = subprocess.run(f'icacls "{path2}" /grant "gigant\malyshev":(NP)F', shell=True, check=True)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)
        
    conn.entries