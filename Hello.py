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

def clasificar_comentario_gpt4(column_name, data):
    import openai
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, recall_score, f1_score, confusion_matrix, classification_report

# Establecer la clave de la API de OpenAI
    with open('api_key.txt', 'r') as file:
        api_key = file.read().strip()

    openai.api_key = api_key

# Seleccionar modelo  "gpt-4"
    model = "gpt-4"

# Cargar el archivo de Excel en un DataFrame de pandas
    #data = pd.read_excel("data.xlsx")

# Definir el texto del prompt para la clasificación
    prompt = """
        Tendrás un rol de clasificador de comentarios de una publicación relacionada con la vacuna contra el VPH.
        No tienes permitido responder otra cosa que no sean números. Las clasificaciones son:

        Si el comentario tiene una postura contraria a la vacuna contra el VPH (antivacuna).La respuesta es: 0
        Si el comentario tiene una postura a favor de la vacuna contra el VPH (provacuna).La respuesta es: 1
        Si el comentario refleja una duda o dudas relacionadas con la vacuna contra el VPH.La respuesta es: 2
        Si el comentario habla de cualquier otra cosa. La respuesta es: 3

        Trata de interpretar las intenciones de las personas, ya que se trata de comentarios de Facebook.
        Si no puedes clasificar, tu respuesta debe ser "3".

        Ahora, clasifica el siguiente comentario, teniendo en cuenta que tu respuesta es solo un número:
    """
#import time
# Parámetros de configuración
    batch_size = 20  # Tamaño del lote de comentarios a procesar antes de guardar
    output_file = "data_gpt_4.xlsx"  # Nombre del archivo de salida
    checkpoint_file = "checkpoint.txt"  # Nombre del archivo de checkpoint

# Variable para almacenar la posición actual en el bucle
    current_index = 0
    completed = False

    while not completed:
    # Verificar si existe un archivo de checkpoint
        try:
            with open(checkpoint_file, 'r') as f:
                current_index = int(f.read())
            print("Se encontró un archivo de checkpoint. Continuando desde la posición:", current_index)
        except FileNotFoundError:
            print("No se encontró un archivo de checkpoint. Comenzando desde el principio.")

    # Crear una columna vacía para almacenar las respuestas si aún no existe
        if 'Clasificación_gpt_4' not in data.columns:
            data['Clasificación_gpt_4'] = ''

    # Iterar sobre cada comentario en el DataFrame
        for index, row in data.iterrows():
        # Verificar si se debe retomar desde el punto de reinicio guardado
            if index < current_index:
                continue

            comment = row[column_name]

            try:
            # Crear la solicitud de completado de chat
                completion = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": comment}
                    ],
                    temperature=0,
                    max_tokens=1
                )

                response = completion.choices[0].message.content.strip()

            # Verificar si la respuesta es un número
                if response.isdigit():
                # Convertir la respuesta a entero
                    response = int(response)
                else:
                # Manejar el caso en el que la respuesta no es un número
                # Puedes asignar un valor predeterminado o tomar cualquier otra acción apropiada
                    response = None  # o cualquier otro valor predeterminado que prefieras

                data.at[index, 'Clasificación_gpt_4'] = response

            # Guardar el DataFrame en un archivo después de procesar un lote de comentarios
                if (index + 1) % batch_size == 0 or (index + 1) == len(data):
                    data[:index + 1].to_excel(output_file, index=False)
                    print("Guardando...")

            # Guardar la posición actual como punto de reinicio
                with open(checkpoint_file, 'w') as file:
                    file.write(str(index + 1))

            except openai.error.OpenAIError as e:
            # Manejar el error del servidor de OpenAI
                print("Error del servidor de OpenAI:", e)
                print("Reanudando el proceso desde la iteración", index)
                completed = False
            #print("Esperando 6 segundos antes de continuar...")
            #time.sleep(6)
                break

        else:
        # El bucle for se completó sin errores, terminar el proceso
            completed = True     
            with open(checkpoint_file, 'w') as file:
                    file.write(str(0))



    print("Procesamiento completado y resultados guardados en", output_file)
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
    return column_name
     # Botón para ocultar/mostrar la API de OpenAI
    api_key = st.text_input("API Key de OpenAI", type="password")
   
    
    # Botón para guardar la API en un documento de GitHub
    if api_key:
        if st.button("Guardar"):
            guardar_api_en_github(api_key)
            with open('api_key.txt', 'w') as file:
                file.write(api_key)
                        
    uploaded_file = st.file_uploader("Cargar archivo", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            file_ext = uploaded_file.name.split(".")[-1]
            if file_ext == "csv":
                data = pd.read_csv(uploaded_file)
                return data
            elif file_ext == "xlsx":
                data = pd.read_excel(uploaded_file)
                return data
            
            st.write("Datos cargados:")
            st.write(data)

            if st.button("Mostrar comentarios antivacunas"):
                comentarios_antivacunas = identificar_antivacunas(data, column_name)
                
                st.subheader("Comentarios antivacunas encontrados:")
                for comentario in comentarios_antivacunas:
                    st.write(comentario)

            if st.button("Mostrar dudas relacionadas"):
                comentarios_dudas = identificar_dudas(data, column_name)
                
                st.subheader("Dudas encontradas:")
                for comentario in comentarios_dudas:
                    st.write(comentario)
            
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

def identificar_antivacunas(data, column_name):
    comentarios_antivacunas = []

    # Procesar los comentarios en la columna 'Comentarios' (ajusta el nombre de la columna según tu CSV)
    for index, row  in data.iterrows():
        if row['Topic_c'] == 0:
            comentarios_antivacunas.append(row[column_name])

    return comentarios_antivacunas

def identificar_dudas(data, column_name):
    comentarios_dudas = []

    # Procesar los comentarios en la columna 'Clasificacion' (ajusta el nombre de la columna según tu CSV)
    for index, row  in data.iterrows():
        if row['Topic_c'] == 2:
            comentarios_dudas.append(row[column_name])

    return comentarios_dudas

if __name__ == "__main__":
    run()
