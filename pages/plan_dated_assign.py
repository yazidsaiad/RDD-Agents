import pandas as pd
import streamlit as st
import utils

def app():

    """
    This funtion generates the project features using streamlit library
    """

    # display images in separated columns
    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
    with col2:
        st.markdown("<h1 style='text-align: center; color: black; font-size : 25px;'>Interface de Traitement de l'Equipe Données</h1>", unsafe_allow_html=True)
    with col3 : 
        st.image('images/logo_sncf.png')
    with col1:
        st.image('images/logo-progres-simplifie.png')

    st.divider()
    st.markdown('<style>body{background-color: Grey;}</style>',unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black; font-size : 25px;'>Plan Dated Assign</h1>", unsafe_allow_html=True)
    st.divider()

    file_idap = st.file_uploader(label="Veuillez sélectionner un fichier IDAP")
    file_control = st.file_uploader(label="Veuillez sélectionner un fichier de contrôle")
    df_idap = pd.DataFrame()
    df_control = pd.DataFrame()
    if file_idap is not None and file_control is not None:
        df_idap = pd.read_excel(file_idap)
        df_control = pd.read_excel(file_control)

    st.divider()

    if  df_idap.empty or df_control.empty:
        st.warning("Veuillez importer les fichiers.")
    else:
        st.markdown("<h1 style='text-align: center; color: black; font-size : 20px;'>Fichiers d'entrées</h1>", unsafe_allow_html=True)
        col1_, col2_ = st.columns([0.7, 0.3])
        with col1_:
            st.dataframe(df_idap, hide_index=True)
        with col2_:
            st.dataframe(df_control, hide_index=True)
        st.divider()
        
        st.info('Génération du fichier en cours...')
        output = utils.format_plan_date_assigned(idap_data=df_idap, control_data=df_control)
        st.success('Génération terminée.')
        st.divider()
        st.markdown("<h1 style='text-align: center; color: black; font-size : 20px;'>Fichier généré</h1>", unsafe_allow_html=True)
        st.dataframe(output, hide_index=True)
        st.divider()
        st.markdown("<h1 style='text-align: center; color: black; font-size : 20px;'>Téléchargement du fichier généré</h1>", unsafe_allow_html=True)
        df_to_save = utils.to_excel(output)
        st.download_button(label="📥 Télécharger au format .xlsx", data=df_to_save, file_name='Plan dated assign IDAP pour SCORE.xlsx')

        csv = utils.convert_df(output)
        st.download_button(
            label="📥 Télécharger au format .csv",
            data=csv,
            file_name='Récupération des régimes IDAP pour SCORE.csv',
            mime="text/csv",
            key='download-csv'
        )

    st.divider()
