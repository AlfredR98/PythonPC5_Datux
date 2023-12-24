import matplotlib.pyplot as plt 
from PIL import Image
import pandas as pd 
import xlsxwriter
import sqlite3
import os

DB = 'candidates.db'
TABLE_NAME ='candidate'
path = './doc_bd/candidates.csv'
df = pd.read_csv(path,sep=';')

'''
CASO 1
'''
with sqlite3.connect(DB) as conn:
   pass
    

def alamacenar_pandas_to_sql(df: pd.DataFrame, database_name: str, table_name: str) -> None:
    column_rename = {c: c.replace(' ','') for c in df.columns}
    df.rename(column_rename,axis = 'columns', inplace=True)
    df.to_sql(table_name,conn, index = False, if_exists='replace')
    sql_table_schema = f'{database_name}.{table_name}'
    cantidad_registros = df.shape[0]
    print(f'Se almacenaron {cantidad_registros} sobre la tabla {sql_table_schema}')
alamacenar_pandas_to_sql(df,DB,TABLE_NAME)

'''
CASO 2
'''

listado_paises = {'United States of America', 'Brazil','Colombia','Ecuador'}

column_rename = {c: c.replace(' ','') for c in df.columns}
df.rename(column_rename,axis = 'columns', inplace=True)

def genero_grafico_circular(df:pd.DataFrame, country:str) ->None:
  tec = df.groupby('Technology')['Technology'].count()
  tec.plot.pie(figsize=(11, 7))
  plt.savefig(f"./reportes/images/{country}/pie_chart.png",dpi=300, bbox_inches='tight')
  plt.close()
  print('Se generó gráfico circular ...')


def genero_grafico_barras(df:pd.DataFrame, country:str)->None:
  """Funcion que se encarga de crear el gráfico de barras"""

  senority_group = df.groupby('Seniority')['Seniority'].count()
  senority_group.plot.bar()

  plt.savefig(f"./reportes/images/{country}/bar_chart.png",dpi=300, bbox_inches='tight')
  plt.close()
  print('Se genero gráfico barras ...')  

  # genero carpetas necesarias
if not os.path.isdir('./reportes'):
  os.mkdir('reportes')
  os.mkdir('./reportes/images')


filtro_df = df[df['Country'].isin(listado_paises)]
filtro_df = filtro_df[(filtro_df['CodeChallengeScore'] >= 7) & (filtro_df['TechnicalInterviewScore'] >= 7)]
print(filtro_df.head(3))


for country in listado_paises:

  if not os.path.isdir(f'./reportes/images/{country}'):
    os.mkdir(f'./reportes/images/{country}')

  countryDf = filtro_df[filtro_df['Country']==country]

  genero_grafico_circular(countryDf, country)
  genero_grafico_barras(countryDf, country)

  with pd.ExcelWriter(f"./reportes/{country}.xlsx", engine= "xlsxwriter") as excelBook:

    sheet_name = f"Report-{country}"
    countryDf.to_excel(excelBook, index=False, sheet_name= sheet_name)

    excel_sheet = excelBook.sheets[sheet_name]

    image_pie_path = f"./reportes/images/{country}/pie_chart.png"
    image_bar_path = f"./reportes/images/{country}/bar_chart.png"

    excel_sheet.insert_image(1, countryDf.shape[1]+2, image_pie_path)
    excel_sheet.insert_image(countryDf.shape[0]+2, countryDf.shape[1]+2, image_bar_path)

    print(f'Se generó reporte para el país {country}')
    pass
  print('Se finalizó  la generacion de reportes')

'''
CASO 3
'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os 


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



file_path = './reportes/Ecuador.xlsx'
with open(file_path, 'rb') as file:
    attachment = MIMEApplication(file.read(), _subtype="xlsx")
    attachment.add_header('Content-Disposition', 'attachment', filename=file_path)
    msg.attach(attachment)

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls() 
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())

print('Correo enviado exitosamente')


def func_sender_email(**args):
  return NotImplementedError
os.chdir('reportes')

func_sender_email(
  sender_email='alfredoraico3@gmail.com',
  sender_password='tupass',
  receiver_email='destinatario@gmail.com',
  subject='Reporte Brazil',
  message='Reporte excel Brazil',
  archivo_adjunto='Brazil.xlsx')