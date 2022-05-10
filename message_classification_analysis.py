"""
Created on Tuesday 10-05-2022
Last Modified on
@author: antoniaaguilera
country: CHILE
Objective: analysis
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#paths
mensajes_mime = "/Users/antoniaaguilera/ConsiliumBots Dropbox/ConsiliumBots/Projects/Chile/Explorador/Data/messages"
data_path = "/Users/antoniaaguilera/ConsiliumBots Dropbox/antoniaaguilera@consiliumbots.com/mensajes_mime/data"
figures_path = "/Users/antoniaaguilera/ConsiliumBots Dropbox/antoniaaguilera@consiliumbots.com/mensajes_mime/figures"

# --------------------------------------------------------------- #
# ---------------------- TRABAJAR MENSAJES ---------------------- #
# --------------------------------------------------------------- #
mime_all = pd.read_excel(f"{data_path}/clean/messages_analysis.xlsx")


"""
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
"""
