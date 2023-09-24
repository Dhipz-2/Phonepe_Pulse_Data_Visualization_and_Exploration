import os
import json
import pandas as pd
import psycopg2

#AGGREGATED TRANSACTION
folder_path = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\aggregated\transaction\country\india\state'
state_list = os.listdir(folder_path)

folder_path2 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\aggregated\transaction\country\india\state\tamil-nadu'
year_list = os.listdir(folder_path2)
year_list.remove('2023')

folder_path3 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\aggregated\transaction\country\india\state\tamil-nadu\2018'
json_list = os.listdir(folder_path3)

d1=[]
for i in state_list:
    i1 = os.path.join(folder_path,i)
    for j in year_list:
        j1 = os.path.join(i1,j)
        n=1
        for k in json_list:
            k1 = os.path.join(j1,k)
            f = open(k1)
            text = json.load(f)
            length = len(text['data']['transactionData'])
            for l in range(length):
                d = dict(TransactionName = text['data']['transactionData'][l]['name'],
                         NumberOfTransactions = text['data']['transactionData'][l]['paymentInstruments'][0]['count'],
                         TransactionAmount = text['data']['transactionData'][l]['paymentInstruments'][0]['amount'],
                         Quater = n,
                         Year = j,
                         State = i)
                d1.append(d)
            n=n+1
df1 = pd.DataFrame(d1)


#AGGREGATED USER
folder_path4 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\aggregated\user\country\india\state'
state_list = os.listdir(folder_path4)

folder_path5 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\aggregated\user\country\india\state\tamil-nadu'
year_list = os.listdir(folder_path5)
year_list.remove('2023')

folder_path6 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\aggregated\user\country\india\state\tamil-nadu\2018'
json_list = os.listdir(folder_path6)

d2=[]
for i in state_list:
    i1 = os.path.join(folder_path4,i)
    for j in year_list:
        j1 = os.path.join(i1,j)
        n=1
        for k in json_list:
            k1 = os.path.join(j1,k)
            f = open(k1)
            text = json.load(f)
            if text['data']['usersByDevice']!=None:
                length = len(text['data']['usersByDevice'])
                for l in range(length):
                    d = dict(Brand = text['data']['usersByDevice'][l]['brand'],
                            RegisteredUsers = text['data']['usersByDevice'][l]['count'],
                            RegisteredUsersPercentage = text['data']['usersByDevice'][l]['percentage'],
                            Quater = n,
                            Year = j,
                            State = i)
                    d2.append(d)
            elif text['data']['usersByDevice']==None:
                d2.append(dict(Brand = None,
                               RegisteredUsers = text['data']['aggregated']['registeredUsers'],
                               RegisteredUsersPercentage = None,
                               Quater = n,
                               Year = j,
                               State = i))
            n=n+1
df2 = pd.DataFrame(d2)
#print(df2)
#print(df2.isnull().sum())
df2 = df2.dropna()


#MAP TRANSACTION
folder_path7 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\map\transaction\hover\country\india\state'
state_list = os.listdir(folder_path7)

folder_path8 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\map\transaction\hover\country\india\state\tamil-nadu'
year_list = os.listdir(folder_path8)
year_list.remove('2023')

folder_path9 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\map\transaction\hover\country\india\state\tamil-nadu\2018'
json_list = os.listdir(folder_path9)

d3=[]
for i in state_list:
    i1 = os.path.join(folder_path7,i)
    for j in year_list:
        j1 = os.path.join(i1,j)
        n=1
        for k in json_list:
            k1 = os.path.join(j1,k)
            f = open(k1)
            text = json.load(f)
            length = len(text['data']['hoverDataList'])
            for l in range(length):
                d = dict(District = text['data']['hoverDataList'][l]['name'],
                         NumberOfTransactions = text['data']['hoverDataList'][l]['metric'][0]['count'],
                         TransactionAmount = text['data']['hoverDataList'][l]['metric'][0]['amount'],
                         Quater = n,
                         Year = j,
                         State = i)
                d3.append(d)
            n=n+1

df3 = pd.DataFrame(d3)
#print(df3)


#MAP USER
folder_path10 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\map\user\hover\country\india\state'
state_list = os.listdir(folder_path10)

folder_path11 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\map\user\hover\country\india\state\tamil-nadu'
year_list = os.listdir(folder_path11)
year_list.remove('2023')

folder_path12 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\map\user\hover\country\india\state\tamil-nadu\2018'
json_list = os.listdir(folder_path12)

d4=[]
for i in state_list:
    i1 = os.path.join(folder_path10,i)
    for j in year_list:
        j1 = os.path.join(i1,j)
        n=1
        for k in json_list:
            k1 = os.path.join(j1,k)
            f = open(k1)
            text = json.load(f)
            length = len(text['data']['hoverData'])
            for l in text['data']['hoverData'].keys():
                d = dict(District = l,
                         RegisteredUser = text['data']['hoverData'][l]['registeredUsers'],
                         Quater = n,
                         Year = j,
                         State = i)
                d4.append(d)
            n=n+1

df4 = pd.DataFrame(d4)
#print(df4)


#TOP TRANSACTION
folder_path13 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\top\transaction\country\india\state'
state_list = os.listdir(folder_path13)

folder_path14 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\top\transaction\country\india\state\tamil-nadu'
year_list = os.listdir(folder_path14)
year_list.remove('2023')

folder_path15 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\top\transaction\country\india\state\tamil-nadu\2018'
json_list = os.listdir(folder_path15)

d5=[]
for i in state_list:
    i1 = os.path.join(folder_path13,i)
    for j in year_list:
        j1 = os.path.join(i1,j)
        n=1
        for k in json_list:
            k1 = os.path.join(j1,k)
            f = open(k1)
            text = json.load(f)
            length = len(text['data']['districts'])
            for l in range(length):
                d = dict(TopDistrict = text['data']['districts'][l]['entityName'],
                         TotalTransaction = text['data']['districts'][l]['metric']['count'],
                         TotalValue = text['data']['districts'][l]['metric']['amount'],
                         Quater = n,
                         Year = j,
                         State = i)
                d5.append(d)
            n=n+1

df5 = pd.DataFrame(d5)
#print(df5)


#TOP USER
folder_path16 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\top\user\country\india\state'
state_list = os.listdir(folder_path16)

folder_path17 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\top\user\country\india\state\tamil-nadu'
year_list = os.listdir(folder_path17)
year_list.remove('2023')

folder_path18 = r'C:\Users\Dhipika\OneDrive\Desktop\streamlit\pulse\data\top\user\country\india\state\tamil-nadu\2018'
json_list = os.listdir(folder_path18)

d6=[]
for i in state_list:
    i1 = os.path.join(folder_path16,i)
    for j in year_list:
        j1 = os.path.join(i1,j)
        n=1
        for k in json_list:
            k1 = os.path.join(j1,k)
            f = open(k1)
            text = json.load(f)
            length = len(text['data']['districts'])
            for l in range(length):
                d = dict(TopDistrict = text['data']['districts'][l]['name'],
                         TotalRegisteredUsers = text['data']['districts'][l]['registeredUsers'],
                         Quater = n,
                         Year = j,
                         State = i)
                d6.append(d)
            n=n+1

df6 = pd.DataFrame(d6)
#print(df6)

df1 = df1.values.tolist()
df2 = df2.values.tolist()
df3 = df3.values.tolist()
df4 = df4.values.tolist()
df5 = df5.values.tolist()
df6 = df6.values.tolist()

hostname = 'localhost'
database = 'phonepe_db'
username = 'postgres'
pwd = ''
port_id = 5432

conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)

cur = conn.cursor()

try:
    create_script1 = '''CREATE TABLE IF NOT EXISTS transaction_type(
    Transaction_name varchar(40),
    Number_of_transactions int,
    Transaction_amount float,
    Quater int,
    Year int,
    State varchar(40)
    )'''
    cur.execute(create_script1)
    cur.executemany('INSERT INTO transaction_type VALUES (%s, %s, %s, %s, %s, %s)', df1)

    create_script2 = '''CREATE TABLE IF NOT EXISTS register_phone_users(
    Brand varchar(30),
    Registered_users int,
    Users_percentage float,
    Quater int,
    Year int,
    State varchar(40)
    )'''
    cur.execute(create_script2)
    cur.executemany('INSERT INTO register_phone_users VALUES (%s, %s, %s, %s, %s, %s)', df2)

    create_script3 = '''CREATE TABLE IF NOT EXISTS statelevel_transaction(
    District varchar(40),
    Number_of_transactions int,
    Transaction_amount float,
    Quater int,
    Year int,
    State varchar(40)
    )'''
    cur.execute(create_script3)
    cur.executemany('INSERT INTO statelevel_transaction VALUES (%s, %s, %s, %s, %s, %s)', df3)

    create_script4 = '''CREATE TABLE IF NOT EXISTS statelevel_users(
    District varchar(40),
    Registered_user int,
    Quater int,
    Year int,
    State varchar(40)
    )'''
    cur.execute(create_script4)
    cur.executemany('INSERT INTO statelevel_users VALUES (%s, %s, %s, %s, %s)', df4)

    create_script5 = '''CREATE TABLE IF NOT EXISTS top_transactions(
    Top_district varchar(40),
    Total_number_of_transactions int,
    Total_transaction_amount float,
    Quater int,
    Year int,
    State varchar(40)
    )'''
    cur.execute(create_script5)
    cur.executemany('INSERT INTO top_transactions VALUES (%s, %s, %s, %s, %s, %s)', df5)

    create_script6 = '''CREATE TABLE IF NOT EXISTS top_users(
    Top_district varchar(40),
    Top_registered_users int,
    Quater int,
    Year int,
    State varchar(40)
    )'''
    cur.execute(create_script6)
    cur.executemany('INSERT INTO top_users VALUES (%s, %s, %s, %s, %s)', df6)

except Exception as error:
            print(error)

conn.commit()
conn.close()


