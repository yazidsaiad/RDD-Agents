"""
Test de transformation des données IDAP/SCORE.

"""
import pandas as pd
from io import BytesIO
import datetime
import streamlit as st

codes_absences = [
    'AG',
    'AM',
    'AN',
    'AY',
    'AZ',
    'BA',
    'BG',
    'BI',
    'BLD',
    'BM',
    'BT',
    'CA',
    'CI',
    'CISS',
    'CJ',
    'CK',
    'CM',
    'DA',
    'DB',
    'DC',
    'EBR',
    'HA',
    'HH',
    'HK',
    'HN',
    'LE',
    'MA',
    'MB',
    'MS',
    'SA',
    'SG',
    'SI',
    'SK',
    'SL',
    'SN',
    'SO',
    'SP',
    'SS',
    'SY',
    'UM',
    'US',
    'UX',
    'YC',
    'YD',
    'YE',
    'YH',
    'YS',
    'ZA',
    'ZE',
    'ZF',
    'ZN',
    'ZT',
    '½CA',
    'RE']


@st.cache_data
def convert_df(df : pd.DataFrame):
   """
   Converts Dataframe into csv file
   """
   return df.to_csv(index=False, header=False, sep=';').encode('utf-8-sig')




def to_excel(df: pd.DataFrame):
    """
    This function converts a pandas dataframe to an excel file.

    Keyword argument : pandas dataframe.
    """
    in_memory_fp = BytesIO()
    df.to_excel(in_memory_fp)
    # Write the file out to disk to demonstrate that it worked.
    in_memory_fp.seek(0, 0)
    return in_memory_fp.read()



def recuperation__des__choix(idap_data : pd.DataFrame, control_data : pd.DataFrame) -> pd.DataFrame:
    """
    Ce script permet de transcrire les informations d'IDAP contenues dans le tableau adap_data
    pour les employés dont l'ID est contenu dans control_data pour les dates spécifiées.
    """

    # idap_data = idap_data.rename(columns={'CODE IMMATRICULATION':'ID'})
    control_data = control_data.rename(columns={control_data.columns[0]:'ID', 
                                                control_data.columns[1]:'Date de début',
                                                control_data.columns[2]: 'Date de fin'})
    
    df_output = pd.concat([control_data, idap_data], axis=1, join="inner")

    df_output = df_output.rename(columns={'PAIE HEURES SUPP':'Comp. TK payée',\
                              'PAIE DEPASSEMENTS': 'Comp. TD payée',\
                                'PAIE PRESENCES' : 'Astr. travail pay.',\
                                    'PAIE REPOS' : 'Astr. repos pay.',\
                                          'PAIE FERIES' : 'Astr. férié pay.'})
    
    df_output['Comp. TQ payée'] = df_output['Comp. TD payée']

    df_output['Date de début'] = [datetime.datetime.strftime(list(df_output['Date de début'])[k], "%d/%m/%Y") \
                                  for k in range(len(df_output))]
    
    df_output['Date de fin'] = [datetime.datetime.strftime(list(df_output['Date de fin'])[k], "%d/%m/%Y") \
                                  for k in range(len(df_output))]
    
    df_output = df_output.replace(to_replace='OUI', value=1).replace(to_replace='NON', value=0)

    df_output['LABEL'] = ['empbook' for k in range(len(df_output))]

    df_output = df_output[['LABEL', 'ID', 'Date de début', 'Date de fin', 'Comp. TK payée',\
                            'Comp. TD payée', 'Comp. TQ payée', 'Astr. férié pay.', \
                                'Astr. repos pay.', 'Astr. travail pay.']]
        
    return df_output



def format_absence_oir(idap_data : pd.DataFrame, control_data : pd.DataFrame) -> pd.DataFrame:
    """
    Récupération des absences.
    """
    control_data = control_data.rename(columns={control_data.columns[0]:'ID'})

    df_output = idap_data[idap_data['CODE IMMATRICULATION'].isin(list(control_data['ID']))]\
        .rename(columns={'CODE IMMATRICULATION':'ID'})\
            [['ID', 'DATE DEBUT NPO', 'HEURE DEBUT NPO', 'DATE FIN NPO', 'HEURE FIN NPO', 'CODE NPO', 'VALEUR NPO']]
    
    df_output['HEURE DEBUT NPO'] = ["16'00" for k in range(len(df_output))]
    df_output['HEURE FIN NPO'] = ["36:00" for k in range(len(df_output))]

    df_output['DATE DEBUT NPO'] = [datetime.datetime.strftime(list(df_output['DATE DEBUT NPO'])[k], "%d/%m/%Y") \
                                  for k in range(len(df_output))]
    
    df_output['DATE FIN NPO'] = [datetime.datetime.strftime(list(df_output['DATE FIN NPO'])[k], "%d/%m/%Y") \
                                  for k in range(len(df_output))]

    df__ = df_output.copy()

    CODE_NPO = []
    for k in range(0, len(df_output)):
        if list(df_output['CODE NPO'])[k] == 'C':
            if list(df_output['VALEUR NPO'])[k] == 0.5:
                CODE_NPO.append("½CA")
            else:
                CODE_NPO.append("CA")
        else:
            CODE_NPO.append(list(df_output['CODE NPO'])[k])
    
    df__['CODE NPO'] = CODE_NPO
    df__['LABEL'] = ['absence' for k in range(len(df__))]

    df__ = df__[df__['CODE NPO'].isin(codes_absences)]

    return df__[['LABEL', 'ID', 'DATE DEBUT NPO', 'HEURE DEBUT NPO', 'DATE FIN NPO', 'HEURE FIN NPO', 'CODE NPO']]


def format_plan_date_assigned(idap_data : pd.DataFrame, control_data : pd.DataFrame) -> pd.DataFrame:
    """
    """
    control_data = control_data.rename(columns={control_data.columns[0]:'ID'})
    
    df_output = idap_data[idap_data['CODE IMMATRICULATION'].isin(list(control_data['ID']))]\
        .rename(columns={'CODE IMMATRICULATION':'ID'})\
            [['ID', 'DATE DEBUT NPO', 'CODE NPO']]
    
    df_output['DATE DEBUT NPO'] = [datetime.datetime.strftime(list(df_output['DATE DEBUT NPO'])[k], "%d/%m/%Y") \
                                  for k in range(len(df_output))]
    
    df_output['LABEL'] = ['plandatedasg' for k in range(len(df_output))]

    df_output['Col 1'] = [1 for k in range(len(df_output))]

    df_output['Col 2'] = ['RECOPIE_IDAP' for k in range(len(df_output))]

    df_output = df_output[df_output['CODE NPO'].isin(['RP', 'RU', 'VT', 'VC', 'RH'])]

    return df_output[['LABEL', 'ID', 'DATE DEBUT NPO', 'CODE NPO', 'Col 1', 'Col 2']]



def recuperation__regimes(idap_data : pd.DataFrame, control_data : pd.DataFrame) -> pd.DataFrame:
    """
    """
    control_data = control_data.rename(columns={control_data.columns[0]:'ID', 
                                                control_data.columns[1]:'Date de début',
                                                control_data.columns[2]: 'Date de fin'})
    
    df_output = pd.concat([control_data, idap_data], axis=1, join="inner")

    df_output['Date de début'] = [datetime.datetime.strftime(list(df_output['Date de début'])[k], "%d/%m/%Y") \
                                  for k in range(len(df_output))]
    
    df_output['Date de fin'] = [datetime.datetime.strftime(list(df_output['Date de fin'])[k], "%d/%m/%Y") \
                                  for k in range(len(df_output))]
    
    df_output['LABEL'] = ['empbook' for k in range(len(df_output))]
    
    df_output = df_output[['LABEL', 'CODE IMMATRICULATION', 'Date de début', 'Date de fin', 'CODE REGIME TRAVAIL']].rename(columns={'CODE IMMATRICULATION' : 'ID', 'CODE REGIME TRAVAIL':'Régime'})

    df_output['Régime'] = df_output['Régime'].replace(to_replace='FE', value='FJ205').replace(to_replace='FS', value='FJ210')

    return df_output


    
    
    

    







    



        
        









