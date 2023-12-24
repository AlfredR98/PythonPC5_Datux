'''
Empleando los datos del archivo './src/crypto_currency'.

Genere un agrupamiento de información a manera de obtener un resumen de los datos.
Almacene dichos datos en un reporte excel.
Apoyandose del ejercicio 2. Cree una imagen que sea guarda en el archivo excel
Emplee un método de envio de correos
'''

import pandas as pd 
import sqlite3 as bd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

path = './doc_bd/cripto_currency.xlsx'
df = pd.read_excel(path, sheet_name='BTC-USD')
df1 = pd.read_excel(path, sheet_name='DOGE-USD')
df2 = pd.read_excel(path, sheet_name='USDT-USD')

dfConcat1 = pd.concat([df, df1, df2], axis=0)
database = 'cripto.bd'
dfConcat1['Moneda'] = 'USD'

with bd.connect(database) as conn:

    try:
        df.to_sql('cripto_currency',conn,index=False, if_exists='replace')
        print('Datos guardados en la BD')

    except Exception as e: 
        print('Ha ocurrido un error: ',e)

with pd.ExcelWriter(f"./reportes/cripto_currency.xlsx", engine= "xlsxwriter") as excelBook:
    sheet_name = f"Report-cripto_currency"
    df.to_excel(excelBook, index=False, sheet_name= sheet_name)
    excel_sheet = excelBook.sheets[sheet_name]
    image_pie_path = f"./reportes/images/cripto_currency/pie_chart.png"
    excel_sheet.insert_image(1, df.shape[1]+2, image_pie_path)
    print(f'Se generó reporte')
    pass
print('Se finalizó la generación de reportes')

smtp_server = 'smtp.gmail.com'  
smtp_port = 587
sender_email = 'tu_correo@gmail.com'
sender_password = 'tu_contraseña'


receiver_email = 'alfredoraico3@gmail.com'
subject = 'Envio Reporte de Candidates'
body = 'Buenas tades,\nSe adjunta el documento en base a lo solicitado.'

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))
