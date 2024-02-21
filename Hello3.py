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

import numpy as np
import streamlit as st
import pandas as pd

def guardar_api_en_github(api_key):
    with open('api_key.txt', 'w') as file:
        file.write(api_key)
    st.write("API key guardada con éxito en 'api_key.txt'")

def initialize_session_state():
    if "button" not in st.session_state:
        st.session_state.button = False

def run():
    st.set_page_config(
        page_title="VaxClass",
        page_icon="📊",
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
    #o_data = False
    column_name = st.text_input("Ingrese el nombre de la columna que contiene los comentarios:")

    # Botón para ocultar/mostrar la API de OpenAI
    api_key = st.text_input("API Key de OpenAI", type="password")
   
    # Botón para guardar la API en un documento de GitHub
    if api_key and st.button("Guardar"):
        guardar_api_en_github(api_key)
                        
    uploaded_file = st.file_uploader("Cargar archivo", type=["csv", "xlsx"])

    # Inicializar session_state antes de cualquier acceso
    initialize_session_state()

    if uploaded_file is not None:
        try:
            file_ext = uploaded_file.name.split(".")[-1]
            if file_ext == "csv":
                data = pd.read_csv(uploaded_file)
            elif file_ext == "xlsx":
                data = pd.read_excel(uploaded_file)
            
            st.write("Datos cargados:")
            st.write(data)
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

    # Botón para clasificar comentarios y mostrar resultados
    button1 = st.button("Clasificar Comentarios")
    if not st.session_state.button:
        st.session_state.button = button1
        if st.session_state.button:
            st.write("button1 is true")
            if 'Clasificacion-gpt-4' not in data.columns:
                # Inicializar la columna 'Clasificacion-gpt-4' con valores predeterminados
                data['Clasificacion-gpt-4'] = np.random.randint(0, 4, size=len(data))
                st.write("Datos actualizados:")
                st.write(data)
                #o_data = True
                # Guardar el archivo actualizado
                data.to_csv("output_data.csv", index=False)

    # Cargar la data actualizada 
    data = pd.read_csv('output_data.csv')
        #st.write(data)

    if st.button("Mostrar comentarios antivacunas") and api_key:
        if 'Clasificacion-gpt-4' not in data.columns:
            st.warning("Primero debe clasificar los comentarios.")
        else:
            comentarios_antivacunas = identificar_antivacunas(data, column_name)
            st.subheader("Comentarios antivacunas encontrados:")
            for comentario in comentarios_antivacunas:
                st.write(comentario)

    if st.button("Mostrar dudas relacionadas") and api_key:
        if 'Clasificacion-gpt-4' not in data.columns:
            st.warning("Primero debe clasificar los comentarios.")
        else:
            comentarios_dudas = identificar_dudas(data, column_name)
            st.subheader("Dudas encontradas:")
            for comentario in comentarios_dudas:
                st.write(comentario)    
            
       
    

def identificar_antivacunas(data, column_name):
    comentarios_antivacunas = []

    # Procesar los comentarios en la columna 'Comentarios' (ajusta el nombre de la columna según tu CSV)
    for index, row  in data.iterrows():
        if row['Clasificacion-gpt-4'] == 0:
            comentarios_antivacunas.append(row[column_name])

    return comentarios_antivacunas

def identificar_dudas(data, column_name):
    comentarios_dudas = []

    # Procesar los comentarios en la columna 'Clasificacion' (ajusta el nombre de la columna según tu CSV)
    for index, row  in data.iterrows():
        if row['Clasificacion-gpt-4'] == 2:
            comentarios_dudas.append(row[column_name])

    return comentarios_dudas

if __name__ == "__main__":
    run()
