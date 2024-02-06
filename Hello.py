# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import pandas as pd
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Bienvenidos a la página! ❤️")

    

    st.markdown(
        """
        Aquí, nos sumergimos en conversaciones significativas relacionadas con la vacuna contra el 
        Virus del Papiloma Humano (VPH). Utilizamos un clasificador especializado para analizar y 
        categorizar los comentarios de manera precisa y eficiente.
        El objetivo principal es dar los comentarios antivacunas para entender las diversas perspectivas
        expresadas por la comunidad en torno a la vacuna contra el VPH.  

        Nuestro clasificador asigna números específicos a cada comentario 
        para reflejar la postura del autor. La clasificación es la siguiente:

        0: Postura contraria a la vacuna contra el VPH (Antivacuna).  
        1: Postura a favor de la vacuna contra el VPH (Provacuna).  
        2: Expresa dudas relacionadas con la vacuna contra el VPH.  
        3: Comentarios que no se relacionan con la vacuna contra el VPH.  
    """
    )
    column_name = st.text_input("Ingrese el nombre de la columna que contiene los comentarios:")
    uploaded_file = st.file_uploader("Cargar archivo", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            file_ext = uploaded_file.name.split(".")[-1]
            if file_ext == "csv":
                data = pd.read_csv(uploaded_file)
            elif file_ext == "xlsx":
                data = pd.read_excel(uploaded_file)
            
            st.write("Datos cargados:")
            st.write(data)

            if st.button("Mostrar comentarios antivacunas"):
                comentarios_antivacunas = identificar_antivacunas(data)
                
                st.subheader("Comentarios antivacunas encontrados:")
                for comentario in comentarios_antivacunas:
                    st.write(comentario)

            if st.button("Mostrar dudas relacionadas"):
                comentarios_dudas = identificar_dudas(data)
                
                st.subheader("Dudas encontradas:")
                for comentario in comentarios_dudas:
                    st.write(comentario)
             # Botón para ocultar/mostrar la API de OpenAI
            if st.checkbox("Mostrar/ocultar API de OpenAI"):
                api_key = st.text_input("API Key de OpenAI", type="password")
                st.write("API Key:", api_key)
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

def identificar_antivacunas(data):
    comentarios_antivacunas = []

    # Procesar los comentarios en la columna 'Comentarios' (ajusta el nombre de la columna según tu CSV)
    for comentario in data['Comentarios']:
        if "anti-vacuna" in str(comentario).lower():
            comentarios_antivacunas.append(comentario)

    return comentarios_antivacunas

def identificar_dudas(data):
    comentarios_dudas = []

    # Procesar los comentarios en la columna 'Clasificacion' (ajusta el nombre de la columna según tu CSV)
    for index, row  in data.iterrows():
        if row['Topic_c'] == 2:
            comentarios_dudas.append(row['Comentarios'])

    return comentarios_dudas

if __name__ == "__main__":
    run()
