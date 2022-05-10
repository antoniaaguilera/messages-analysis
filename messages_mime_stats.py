"""
Created on Monday 28-03-2022
Last Modified:
@author: antoniaaguilera
country: CHILE
Objective: message stats and analysis
"""
import pandas as pd
import numpy as np
import matplotlib
import nltk
from datetime import datetime, date
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import webtext
from nltk.probability import FreqDist
import re
#nltk.download("stopwords")
#nltk.download('punkt')


#paths
mensajes_mime = "/Users/antoniaaguilera/ConsiliumBots Dropbox/ConsiliumBots/Projects/Chile/Explorador/Data/messages"
save_path = "/Users/antoniaaguilera/ConsiliumBots Dropbox/antoniaaguilera@consiliumbots.com/mensajes_mime/data"

# --------------------------------------------------------------- #
# ---------------------- TRABAJAR MENSAJES ---------------------- #
# --------------------------------------------------------------- #
mime_all = pd.read_excel(f"{save_path}/raw/mime_all.xlsx")
# --- messages to string and lowercase
mime_all['message'] = mime_all['message'].astype(str).str.lower()

# --- tokenize
regexp = RegexpTokenizer('\w+')
mime_all['message_token'] = mime_all['message'].apply(regexp.tokenize)

# --- stop words
stop_list = nltk.corpus.stopwords.words("spanish")
len(stop_list)
# agregar nuevas stopwords
new_words = ['si', 'buenos', 'buenas', 'días', 'tardes','dias', ',', 'mas', 'hola', 'estimado', 'buen', 'día',
':', 'gracias', 'estimados', 'estimadas', 'estimada', 'ke', '.', '()', ')', 'estimada/o','sra', 'estimad', '!', 'nan',
'estimado(a)', 'hijo', 'hija', 'nombre', 'niño', 'niña', 'acabo', 'años', 'año', 'saludos', 'muchas']
stop_list.extend(new_words)

# --- sacar stopwords
mime_all['message_token'] = mime_all['message_token'].apply(lambda x: [item for item in x if item not in stop_list])
messages_filtered = mime_all['message_token']

# ----------------------------------------------------- #
# ----------------- STATS PARA CHRIS ------------------ #
# ----------------------------------------------------- #
mime_all['timestamp']=pd.to_datetime(mime_all['timestamp'])
mime_all['date']=pd.to_datetime(mime_all['timestamp']).dt.date
min(mime_all['date'])
max(mime_all['date'])
#mime_all.count()
#mime_oldold.count()
mime_2 = mime_all[mime_all['origen']!='oldold']
mime_2.count()
#mails unicos
mime_all['mail_from'].value_counts()
mime_2['mail_from'].value_counts()
#contact_type
mime_all['contact_type_old'].value_counts()
mime_all['contact_type'].value_counts()


# --- contar frecuencia
all_words = []
for word_list in mime_all['message_token']:
    all_words += word_list
freq_palabras = FreqDist(all_words)
freq_palabras.plot(25, cumulative=False)
freq_palabras = pd.DataFrame.from_dict(freq_palabras, orient='index')
freq_palabras.columns = ['Frecuencia']
freq_palabras.index.name = 'palabra'
freq_palabras.to_excel('/Users/antoniaaguilera/ConsiliumBots Dropbox/antoniaaguilera@consiliumbots.com/MENSAJES MIME/freq_palabras.xlsx')


# --- identificar palabras clave
mime_all['soy_profesor'] = mime_all['message'].str.contains('soy profesor|soy profesora')
mime_all['soy_docente'] = mime_all['message'].str.contains('soy docente')
mime_all['equipo_docente'] = mime_all['message'].str.contains('equipo docente')
mime_all['para_profesor'] = mime_all['message'].str.contains('para profesor|para profesora')
mime_all['como_profesor'] = mime_all['message'].str.contains('como profesor|como profesora')
mime_all['egresado'] = mime_all['message'].str.contains('egresado|egresada')
mime_all['cv'] = mime_all['message'].str.contains('cv|curriculum|curriculo|curriculum vitae')
#mime_all['arroba'] = mime_all['message'].str.contains('@')
mime_all['puesto_trabajo'] = mime_all['message'].str.contains('puesto de trabajo')
mime_all['busco_trabajo'] = mime_all['message'].str.contains('busco trabajo')
mime_all['oportunidad_laboral'] = mime_all['message'].str.contains('oportunidad laboral')
mime_all['busco_empleo'] = mime_all['message'].str.contains('busco empleo')
mime_all['ofrecer'] = mime_all['message'].str.contains('ofrecer')
mime_all['servicio'] = mime_all['message'].str.contains('servicio')
mime_all['fono'] = mime_all['message'].str.contains('soy fonoaudióloga|soy fonoaudiologa|soy fonoaudiólogo|soy fonoaudiologo')
mime_all['psico'] = mime_all['message'].str.contains('soy psicóloga|soy psicologa|soy psicólogo|soy psicologo')

mime_all['is_teacher'] = (mime_all['soy_profesor']==True)| (mime_all['soy_docente']==True)| (mime_all['soy_docente']==True)|(mime_all['equipo_docente']==True)|(mime_all['para_profesor']==True)|(mime_all['como_profesor']==True)|(mime_all['cv']==True)|(mime_all['busco_trabajo']==True)|(mime_all['puesto_trabajo']==True)|(mime_all['busco_empleo']==True)|(mime_all['oportunidad_laboral']==True)
mime_all['is_provider'] = (mime_all['ofrecer']==True)| (mime_all['servicio']==True)


mime_all['is_teacher'].value_counts()
mime_teacher = mime_all[mime_all['is_teacher']==True]
mime_teacher['mail_from'].value_counts().count()

mime_all['is_provider'].value_counts()
mime_provider = mime_all[mime_all['is_provider']==True]
mime_provider['mail_from'].value_counts().count()

mime_all['fono'].value_counts()
mime_fono = mime_all[mime_all['fono']==True]
mime_fono['mail_from'].value_counts().count()

mime_all['psico'].value_counts()
mime_psico = mime_all[mime_all['psico']==True]
mime_psico['mail_from'].value_counts().count()

mime_teachers = mime_all

mime_all.to_excel(f'{save_path}/clean/messages_analysis.xlsx')
mime_teachers.to_excel(f'{save_path}/clean/messages_analysis_seba.xlsx')


# ---------------------------------------------------------------------------- #
# -------------------- CREAR BASE PARA PEGAR CON RESPUESTA  ------------------ #
# ---------------------------------------------------------------------------- #
contacts_aux = mime_all
contacts_aux = contacts_aux[pd.isna(contacts_aux['school_name'])==False]
contacts_aux = contacts_aux.drop_duplicates(subset=['mail_from'])

respuestas = pd.read_excel(f"{save_path}/raw/respuestas.xlsx")

aux = respuestas.merge(contacts_aux, how='left', on = 'mail_from')
aux['school_name'] = aux['school_name'].astype(str).str.upper()

positiva = aux[aux['recibio']=='SI']
positiva = positiva[positiva['message']!=np.NaN]
positiva = positiva.dropna(subset=['message'])
positiva = positiva['message_token']
positiva
# --- reemplazar establecimiento por colegio
positiva = positiva.reset_index()
positiva

# --- contar frecuencia
all_words2 = []
for word_list in range(len(positiva)):
    all_words2 += positiva['message_token'][word_list]
    print(word_list)

all_words2 = list(map(lambda x: x.replace('establecimiento', 'colegio'), all_words2))

freq_palabras = FreqDist(all_words2)
freq_palabras.plot(25, cumulative=False)
freq_palabras = pd.DataFrame.from_dict(freq_palabras, orient='index')
freq_palabras.columns = ['Frecuencia']
freq_palabras.index.name = 'palabra'

freq_palabras.to_excel(f'{save_path}/clean/freq_palabras.xlsx')
freq_palabras
aux.to_excel(f"{save_path}/clean/mime_respuestas.xlsx", index=False, header=True)
