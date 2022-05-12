"""
Created on Monday 28-03-2022
Last Modified on Tuesday 12-05-2022
@author: antoniaaguilera
country: CHILE
Objective: message classification for automatic answers
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
'estimado(a)', 'nombre', 'acabo', 'años', 'año', 'saludos', 'muchas']
stop_list.extend(new_words)

# --- sacar stopwords
mime_all['message_token'] = mime_all['message_token'].apply(lambda x: [item for item in x if item not in stop_list])
messages_filtered = mime_all['message_token']

mime_all['timestamp']=pd.to_datetime(mime_all['timestamp'])
mime_all['date']=pd.to_datetime(mime_all['timestamp']).dt.date
min(mime_all['date'])
max(mime_all['date'])
mime_all = mime_all[mime_all['origen']!='oldold']
mime_all = mime_all.reset_index(drop=True)

mime_all['msg_length'] = mime_all['message'].str.len()

# ----------------------------------------------------------------------------------------- #
# ----------------------------------- CLASSIFICATION -------------------------------------- #
# ----------------------------------------------------------------------------------------- #
mime_all['Category'] = ''
mime_all['grade']=''
# ---------------------------------------------------------------------- #
# ------------------------- IDENTIFICAR NIVEL -------------------------- #
# ---------------------------------------------------------------------- #
prek = mime_all['message'].str.contains('prekinder|pre-kinder|pre kinder|prekimder|prek')
kinder = mime_all['message'].str.contains('kinder')

basica_1 =  mime_all['message'].str.contains('básico|basico|básica|basica|primaria') & mime_all['message'].str.contains('1|1b|1ro|1ero|1º|1°|primero')
basica_2 =  mime_all['message'].str.contains('básico|basico|básica|basica|primaria') & mime_all['message'].str.contains('2|2b|2do|2º|2°|segundo')
basica_3 =  mime_all['message'].str.contains('básico|basico|básica|basica|primaria') & mime_all['message'].str.contains('3|3b|3ro|3ero|3º|3°|tercero')
basica_4 =  mime_all['message'].str.contains('básico|basico|básica|basica|primaria') & mime_all['message'].str.contains('4|4b|4to|4º|4°|cuarto')

basica_5 =  mime_all['message'].str.contains('5|5to|5º|5°|quinto|5basico|5basica')
basica_6 =  mime_all['message'].str.contains('6|6to|6º|6°|sexto|6basico|6basica')
basica_7 =  mime_all['message'].str.contains('7|7mo|7º|7°|septimo|séptimo|7basico|7basica')
basica_8 =  mime_all['message'].str.contains('8|8vo|8º|8°|octavo|8basico|8basica')

media_1 =  mime_all['message'].str.contains('medio|media') & mime_all['message'].str.contains('1|1ro|1ero|1º|1°|primero|iº|i°|i*')
media_2 =  mime_all['message'].str.contains('medio|media') & mime_all['message'].str.contains('2|2do|2º|2°|segundo|iiº|ii°|ii*')
media_3 =  mime_all['message'].str.contains('medio|media') & mime_all['message'].str.contains('3|3ro|3ero|3º|3°|tercero|iiiº|iii°|iii*')
media_4 =  mime_all['message'].str.contains('medio|media') & mime_all['message'].str.contains('4|4to|4º|4°|cuarto|ivº|iv°|iii*')


for x in range(len(basica_1)) :
    if prek.loc[x] ==True :
        mime_all['grade'][x] = "Pre-Kinder"
    elif kinder.loc[x] ==True :
        mime_all['grade'][x] = "Kinder"
    elif basica_1.loc[x] ==True :
        mime_all['grade'][x] = "1º básico"
    elif basica_2.loc[x] == True:
        mime_all['grade'][x] = "2º básico"
    elif basica_3.loc[x] == True:
        mime_all['grade'][x] = "3º básico"
    elif basica_4.loc[x] == True:
        mime_all['grade'][x] = "4º básico"
    elif basica_5.loc[x] == True:
        mime_all['grade'][x] = "5º básico"
    elif basica_6.loc[x] == True:
        mime_all['grade'][x] = "6º básico"
    elif basica_7.loc[x] == True:
        mime_all['grade'][x] = "7º básico"
    elif basica_8.loc[x] == True:
        mime_all['grade'][x] = "8º básico"
    elif media_1.loc[x] == True:
        mime_all['grade'][x] = "Iº medio"
    elif media_2.loc[x] == True:
        mime_all['grade'][x] = "IIº medio"
    elif media_3.loc[x] == True:
        mime_all['grade'][x] = "IIIº medio"
    elif media_4.loc[x] == True:
        mime_all['grade'][x] = "IVº medio"
    else:
        mime_all['grade'][x] = "Sin curso"


# ---------------------------------------------------------------------- #
# ---------------------- PARENTS/LEGAL GUARDIANS ----------------------- #
# ---------------------------------------------------------------------- #
verb = 'ver|tiene|necesito|necesita|busco|busca|buscando|quiero|requiero|quisiera|quería|interesada|interesado|interesa|cuenta con|cuentan con|tengo interés|tengo interes|solicitar|solicito|solicitud|saber|ayudar|ayude|indicar|hay'

kid = 'hijo|hija|niño|niña|infante'
age = 'años|año|edad'
stage = 'básico|basico|medio|media|básica|basica|prekinder|pre-kinder|pre kinder|pre-kínder|pre kínder|kinder|grado|septimo|setimo|séptimo|sétimo|octavo|8vo|7mo'

vacante = 'vacante|vacantes|vacant|bacante|cupo|cupos|sobre cupo|sobrecupo'
matricula = 'matrícula|matricula|matricularme|postular|postulacion|postulación|inscribir|inscribirme|admitir|admisión'
requirements = 'información|requisitos|requerimientos|seguir|proceder|papeles|documentos|documentación|documentacion'
payments = 'costo|precio|arancel|pago|mensualidad|beca|becas|tarifa|pensión|pension|mensual|valor|copago|co pago|co-pago'

lista_espera = 'lista de espera|lista espera|listaespera'
traslado = 'traslado|trasladar|cambiar|cambio'

pie = 'pie|autista|autismo|discapacidad auditiva|discapacidad visual|discapacidad intelectual|discapacidad múltiple|sordoceguera|disfasia'
horario = 'horario de clases|horario'

beca = 'beca'
#busca vacante: verbo + vacante + hijo o curso
mime_all['lg_busca_vacante'] = mime_all['message'].str.contains(verb) & mime_all['message'].str.contains(vacante) & (mime_all['message'].str.contains(kid)|mime_all['message'].str.contains(stage)|mime_all['message'].str.contains(age) )
mime_all['lg_busca_vacante'] = np.where((mime_all['message'].str.contains(vacante)&mime_all['message'].str.contains(stage)), True,mime_all['lg_busca_vacante'])
mime_all['lg_busca_vacante'] = np.where((mime_all['message'].str.contains(stage)&mime_all['lg_busca_vacante']==False), True,mime_all['lg_busca_vacante'])

#busca matricula: verbo + matricula + hijo o curso
mime_all['lg_busca_matricula'] = (mime_all['message'].str.contains(verb) & mime_all['message'].str.contains(matricula))|((mime_all['message'].str.contains(stage)|mime_all['message'].str.contains(age)) & mime_all['message'].str.contains(matricula))
mime_all['lg_busca_matricula'] = np.where(mime_all['message'].str.contains('me interesa postular a este establecimiento'), True,mime_all['lg_busca_matricula'])

#busca información:
mime_all['lg_busca_requisitos'] = mime_all['message'].str.contains(verb) & mime_all['message'].str.contains(requirements) & (mime_all['message'].str.contains(kid)|mime_all['message'].str.contains(stage)|mime_all['message'].str.contains(age) )
mime_all['lg_busca_requisitos'] = np.where(mime_all['message'].str.contains('quiero saber más sobre el proceso de matrícula'), True ,mime_all['lg_busca_requisitos'])

#busca información:
mime_all['lg_busca_costo'] = mime_all['message'].str.contains(payments)

#está en lista de espera
mime_all['lg_lista_espera'] = mime_all['message'].str.contains(lista_espera)

#busca traslado
mime_all['lg_traslado'] = mime_all['message'].str.contains(verb) & mime_all['message'].str.contains(traslado)

#busca pie
mime_all['lg_pie'] = mime_all['message'].str.contains(kid) & mime_all['message'].str.contains(pie)

#conocer horario
mime_all['lg_horario'] = mime_all['message'].str.contains(verb) & mime_all['message'].str.contains(horario) & mime_all['message'].str.contains(stage)

#conocer horario
mime_all['lg_vacantes_scurso'] = mime_all['message'].str.contains(verb) & mime_all['message'].str.contains(vacante) & mime_all['grade']==''


mime_all['Category'] = np.where(mime_all['lg_busca_vacante']==True, 'Parent/Legal Guardian',mime_all['Category'])
mime_all['Category'] = np.where(mime_all['lg_busca_matricula']==True, 'Parent/Legal Guardian',mime_all['Category'])
mime_all['Category'] = np.where(mime_all['lg_busca_requisitos']==True, 'Parent/Legal Guardian',mime_all['Category'])
mime_all['Category'] = np.where(mime_all['lg_busca_costo']==True, 'Parent/Legal Guardian',mime_all['Category'])
mime_all['Category'] = np.where(mime_all['lg_lista_espera']==True, 'Parent/Legal Guardian',mime_all['Category'])
mime_all['Category'] = np.where(mime_all['lg_traslado']==True, 'Parent/Legal Guardian',mime_all['Category'])
mime_all['Category'] = np.where(mime_all['lg_pie']==True, 'Parent/Legal Guardian',mime_all['Category'])
mime_all['Category'] = np.where(mime_all['lg_horario']==True, 'Parent/Legal Guardian',mime_all['Category'])
mime_all['Category'] = np.where(mime_all['lg_vacantes_scurso']==True, 'Parent/Legal Guardian',mime_all['Category'])

# ---------------------------------------------------------------------- #
# -------------------------- ADULT EDUCATION --------------------------- #
# ---------------------------------------------------------------------- #
#ed adultos
mime_all['ae_adultos'] = mime_all['message'].str.contains('para adultos')
mime_all['ae_adultos_basica'] = mime_all['message'].str.contains('para adultos') & mime_all['message'].str.contains('basica|básica|basico|básico')
mime_all['ae_adultos_media'] = mime_all['message'].str.contains('para adultos') & mime_all['message'].str.contains('medio|media')

mime_all['Category'] = np.where(mime_all['ae_adultos']==True, 'Adult Education', mime_all['Category'])

mime_all['grade'] = np.where(mime_all['ae_adultos_basica']==True , 'Básica Adultos' , mime_all['grade'])
mime_all['grade'] = np.where(mime_all['ae_adultos_media']==True  , 'Media Adultos'  , mime_all['grade'])


# ---------------------------------------------------------------------- #
# -------------------------- PLATFORM CONTACT -------------------------- #
# ---------------------------------------------------------------------- #
#sige
update = 'agregar|agrego|agregó|actualizamos|actualicé|actualizó|actualizar|actualiza|cambiamos|cambié|cambió|cambiar|cambia|modificamos|modifiqué|modificó|modificar|modifica|encarga|encargue'
sige_person = 'encargado|encargada'
document = 'sige|pei'

mime_all['pc_update'] = (mime_all['message'].str.contains(update)|mime_all['message'].str.contains('error')) & mime_all['message'].str.contains(document)
mime_all['pc_sigeperson']  = mime_all['message'].str.contains(sige_person) & mime_all['message'].str.contains(document)


mime_all['Category'] = np.where(mime_all['pc_update']==True, 'Platform Contact',mime_all['Category'])
mime_all['Category'] = np.where(mime_all['pc_sigeperson']==True, 'Platform Contact',mime_all['Category'])

# ---------------------------------------------------------------------- #
# ------------------------- SERVICE PROVIDERS -------------------------- #
# ---------------------------------------------------------------------- #
#preuniversitarios, cortinas, paseos
offer = 'ofrezco|ofrecidos|ofrecido|ofrecer|ofrece|mostrar|mostrarles|presentar|presentarles|brindarle|disposición'
services = 'servicios|servicio|propuesta|programa|programas|consultor|consultores'

highered = 'universidad|ed superior|educación superior|educacion superior|preuniversitario|pre universitario|pre-universitario'
access = 'ingreso|admisión|difusión|acceso'

mime_all['sp_offer']  = mime_all['message'].str.contains(offer) & mime_all['message'].str.contains(services)
mime_all['sp_highered'] = mime_all['message'].str.contains(highered) & mime_all['message'].str.contains(access)

mime_all['Category'] = np.where(mime_all['sp_offer']==True, 'Service Provider',mime_all['Category'])
mime_all['Category'] = np.where(mime_all['sp_highered']==True, 'Service Provider',mime_all['Category'])

# ---------------------------------------------------------------------- #
# -------------------------- LOOKING FOR JOB --------------------------- #
# ---------------------------------------------------------------------- #
teacher = 'profesor|profesora|docente|educador|educadora|equipo docente|egresado|egresada|licenciada|licenciado'
therapy =  'fonoaudióloga|fonoaudiologa|fonoaudiólogo|fonoaudiologo|psicóloga|psicologa|psicólogo|psicologo|kinesiologo|kinesiologa|kinesiólogo|kinesióloga'
classroom_asistance = 'psicopedagogo|psicopedagoga|auxiliar|asistente|orientador|orientadora|inspector|inspectora|bibliotecólogo|bibliotecóloga|bibliotecologo|bibliotecologa|utp'

resume = 'cv|curriculum|curriculo|curriculum vitae|currículo|curriculo'
job = 'trabajo|puesto de trabajo|oportunidad laboral|empleo|trabajar|integrarme a su equipo|requieren docentes|vacante laboral|adherirme al proyecto|entrevista'

mime_all['jobs_teaching'] = mime_all['message'].str.contains(teacher) & (mime_all['message'].str.contains(job)|mime_all['message'].str.contains(resume))
mime_all['jobs_therapy']  = mime_all['message'].str.contains(therapy) & (mime_all['message'].str.contains(job)|mime_all['message'].str.contains(resume))
mime_all['jobs_asistance']  = mime_all['message'].str.contains(classroom_asistance) & (mime_all['message'].str.contains(job)|mime_all['message'].str.contains(resume))


mime_all['Category'] = np.where(mime_all['jobs_teaching']==True, 'Looking for Jobs',mime_all['Category'])
mime_all['Category'] = np.where(mime_all['jobs_therapy']==True, 'Looking for Jobs',mime_all['Category'])
mime_all['Category'] = np.where(mime_all['jobs_asistance']==True, 'Looking for Jobs',mime_all['Category'])

# ---------------------------------------------------------------------- #
# ------------------------------ OTHERS -------------------------------- #
# ---------------------------------------------------------------------- #
students = 'soy estudiante|soy alumno|soy alumna|exalumno|exalumna|ex-alumno|ex-alumno|ex alumna|ex alumno|realizar|hacer'
institution = 'universidad|instituto|pedagogía|psicopedagogía|pedagogia|psicopedagogia'
internship = 'práctica|práctica profesional|practica|practica profesional|proyecto de título|proyecto de titulo|cátedra|catedra|ramo'
colision = 'colision|colisión|colisionado|colisionada'
link = 'link|página web|pagina web|web'
#necesito el contacto
mime_all['other_internship'] = mime_all['message'].str.contains(students) & mime_all['message'].str.contains(internship) & mime_all['message'].str.contains(institution)
mime_all['other_colision'] = mime_all['message'].str.contains(colision)
mime_all['other_link'] = mime_all['message'].str.contains(link)


mime_all['Category'] = np.where(mime_all['other_internship']==True , 'Other',mime_all['Category'])
mime_all['Category'] = np.where(mime_all['other_colision']==True , 'Other',mime_all['Category'])
#mime_all['Category'] = np.where(mime_all['other_link']==True , 'Other',mime_all['Category'])

# ---------------------------------------------------------------------- #
# --------------------------- CORRECTIONS ------------------------------ #
# ---------------------------------------------------------------------- #
#mime_all['lg_busca_vacante'] = np.where(mime_all['Category']!='Parent/Legal Guardian', False ,mime_all['lg_busca_vacante'])

#solicito beca
mime_all['lg_busca_beca'] = mime_all['message'].str.contains(beca)
mime_all['Category'] = np.where(mime_all['lg_busca_beca']==True, 'Parent/Legal Guardian',mime_all['Category'])


# ----------------------------------------------------------------------------- #
# --------------------------- MERGE CON RBD Y SECTOR -------------------------- #
# ----------------------------------------------------------------------------- #
campus = pd.read_csv("/Users/antoniaaguilera/ConsiliumBots Dropbox/antoniaaguilera@consiliumbots.com/Explorador_Chile/E_Escolar/latest_from_back/cb_explorer_chile_institutions_campus.csv")
campus = campus[['institution_code', 'sector_id']]
campus = campus.drop_duplicates(subset=['institution_code'])


cross_walk = pd.read_stata("/Users/antoniaaguilera/ConsiliumBots Dropbox/ConsiliumBots/Projects/Chile/Explorador/Data/mixpanel_analysis_2022/crosswalk_schools_full.dta")
df = mime_all.merge(cross_walk, how='left', on = 'school_id')

df = df.merge(campus, how='left', on = 'institution_code')

df
# ---------------------------------------------------------------------- #
# ----------------------------- SAVE FILE ------------------------------ #
# ---------------------------------------------------------------------- #


df.to_excel(f'{save_path}/clean/messages_analysis.xlsx')
