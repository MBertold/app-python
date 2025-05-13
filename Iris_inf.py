import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.pipeline import Pipeline
import io

loaded_model = joblib.load("logistic_reg_iris.pkl")
def predict_data(data):
    return loaded_model.predict([data])[0]
    
def load_data():
    uploaded_file = st.file_uploader("Scegli un file CSV o XLSX", type=['csv', 'xlsx','data'])
    if uploaded_file is not None:
        # Verifica l'estensione del file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            st.success("File CSV caricato con successo!")
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
            st.success("File XLSX caricato con successo!")
        elif uploaded_file.name.endswith('.data'):
            df = pd.read_csv(uploaded_file)
            st.success("File data caricato con successo!")
        else:
            st.error("Formato file non supportato!")
        df.columns = ['sepal length', 'sepal width', 'petal length', 'petal width']
        return df
def pred_batch(df_test):
    test_pred = loaded_model.predict(df_test)
    test_pred =pd.DataFrame( loaded_model.predict(df_test))
    test_pred.columns = ['class']
    df_ris = pd.concat([df_test,test_pred],axis=1)
    return df_ris
def convert_to_excel(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="data",index=False)
    
    writer.close()
    return output.getvalue()

st.title("Inferenza")

tab1,tab2 = st.tabs(["Self Predict","File Predict"])

with tab1:
    sepal_length = st.slider("sepal_length",0.0,10.0,0.1)
    sepal_width = st.slider("sepal_width",0.0,10.0,0.1)
    petal_length = st.slider("petal_length",0.0,10.0,0.1)
    petal_width = st.slider("petal_width",0.0,10.0,0.1)

    data = [sepal_length,sepal_width,petal_length,petal_width]
    if st.button("Calcola"):
        risultato = predict_data(data)
        st.write("Risultato : ", risultato)

with tab2:
    df_test =pd.DataFrame(load_data())
    if not df_test.empty:
        pred = pred_batch(df_test)
        st.dataframe(pred)
        st.download_button(
                                label="download as Excel-file",
                                data=convert_to_excel(pred),
                                file_name="data.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key="excel_download",
                                )


