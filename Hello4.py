import streamlit as st
import pandas as pd

def comprobar_nombre_columna(column_name, uploaded_file):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(uploaded_file)
        
        # Get the names of all columns in the DataFrame
        columns = df.columns
        st.write(columns)
        
        # Initialize a list to store column names where the name is found
        found_columns = []
        
        # Iterate over each column and check if the name is in the first row
        for col in columns:
            if col == column_name:
                found_columns.append(col)
        
        if found_columns:
            st.write("The name '{column_name}' is found in the first row of the following columns:")
            for col in found_columns:
                print(col)
        else:
            st.write("The name '{column_name}' is not found in the first row of any column.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if 'button' not in st.session_state:
    st.session_state.button = False

def click_button():
    st.session_state.button = not st.session_state.button

st.button('Click me', on_click=click_button)

if st.session_state.button:
    # The message and nested widget will remain on the page
    st.write('Button is on!')
    st.slider('Select a value')
else:
    st.write('Button is off!')
    column_name = st.text_input("Ingrese el nombre de la columna que contiene los comentarios:")
    uploaded_file = st.file_uploader("Cargar archivo", type=["csv", "xlsx"])
    if st.button("Comprobar nombre"):
        comprobar_nombre_columna(column_name, uploaded_file)
    