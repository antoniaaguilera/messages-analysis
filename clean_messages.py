"""
Created on Monday 28-03-2022
Last Modified:
@author: antoniaaguilera
country: CHILE
Objective: Clean messages
"""

# -------------------------------------------------------- #
# ---------------------- PREAMBULO  ---------------------- #
# -------------------------------------------------------- #
import pandas as pd
import numpy as np
import os
import matplotlib
import nltk
from datetime import datetime, date, timedelta
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
yesterday = date.today() - timedelta(days = 1)

# ------------------------------------------------------------- #
# ---------------------- CARGAR MENSAJES ---------------------- #
# ------------------------------------------------------------- #
# --- load data
#messages mime old old
mime_oldold = pd.read_excel(f"{mensajes_mime}/mime_oldold/Formulario de Contacto MIME (Responses).xlsx")
mime_oldold['origen'] ='oldold'
mime_oldold['date']=pd.to_datetime(mime_oldold['timestamp']).dt.date
min(mime_oldold['date'])
max(mime_oldold['date'])

#messages mime old
mime_old = pd.read_excel(f"{mensajes_mime}/mime_old/messages_2022_3_21.xlsx")
mime_old = mime_old.rename(columns={"school_id": "school_uuid"})
mime_old = mime_old[["mail_from", "school_name", "school_email", "school_uuid", "timestamp", "parent_uuid", "message_id", "country", "phone", "message"]]
mime_old = mime_old.reset_index(drop=True)
mime_old['origen'] ='old'
mime_old['date']=pd.to_datetime(mime_old['timestamp']).dt.date
min(mime_old['date'])
max(mime_old['date'])

#messages mime new
mime_new = pd.read_excel(f"{mensajes_mime}/mime_new/messages_hasta2022-{yesterday.month}-{yesterday.day}.xlsx")
mime_new = mime_new[["mail_from", "school_name", "school_email", "school_uuid", "timestamp", "parent_uuid", "message_id", "country", "phone", "contact_type", "message"]]
mime_new = mime_new.reset_index(drop=True)
mime_new['origen'] ='new'
mime_new.count()

mime_all = mime_old.append(mime_new)
mime_all = mime_oldold.append(mime_all)
mime_all = mime_all.reset_index(drop=True)
mime_all
#keep country Chile

# ----------------------------------------------------------------------------- #
# ------------------------------- MERGE CON RBD  ------------------------------ #
# ----------------------------------------------------------------------------- #
mime_all = mime_all.rename(columns={"school_uuid": "school_id"})

cross_walk = pd.read_stata("/Users/antoniaaguilera/ConsiliumBots Dropbox/ConsiliumBots/Projects/Chile/Explorador/Data/mixpanel_analysis_2022/crosswalk_schools_full.dta")
df = mime_all.merge(cross_walk, how='left', on = 'school_id')


mime_all.to_excel(f"{save_path}/raw/mime_all.xlsx", index=False, header=True)


# -------------------------------------------------------- #
# -------------------- CREAR CONTACTOS  ------------------ #
# -------------------------------------------------------- #
contacts = mime_all[mime_all['origen']!='oldold']
contacts_aux = contacts

contacts = contacts[['mail_from', 'school_name']]
contacts = contacts[pd.isna(contacts['school_name'])==False]
contacts = contacts.drop_duplicates(subset=['mail_from'])
contacts['school_name'] = contacts['school_name'].str.upper()
contacts
contacts.to_csv(f"{save_path}/clean/mime_contacts.csv", index=False, header=True)
