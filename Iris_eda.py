import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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
        df.columns = ['sepal length', 'sepal width', 'petal length', 'petal width', 'class']
        return df
def create_pairplot(data, features, hue=None):
    """Crea un pairplot con le features selezionate"""
    fig = plt.figure(figsize=(12,12))
    fig = sns.pairplot(data[features], hue=hue, diag_kind='kde',height=1.5)
    #fig.title('Relazioni tra le Variabili Selezionate', y=1.02, size=16)
    return fig
def pairplotNoHue(data, features):
    """Crea un pairplot con le features selezionate"""
    fig = plt.figure(figsize=(12,12))
    fig = sns.pairplot(data[features],height=1.5)
    #fig.title('Relazioni tra le Variabili Selezionate', y=1.02, size=16)
    return fig    


st.title("EDA")
df =pd.DataFrame(load_data())
if not df.empty:
    st.dataframe(df)
    
    st.header('🎯 Opzioni di Visualizzazione')
    features = st.multiselect(
                            'Seleziona le variabili da visualizzare',
                            options=df.columns.tolist(),
                            help='Seleziona almeno due variabili per creare il pairplot'
                            )
    tab1,tab2 = st.tabs(["PairplotClass","PairplotNoClass"])
    if len(features) >= 2:
        with tab1:
            st.subheader('🎨 Pairplot delle Variabili Selezionate')
            with st.spinner('Generazione del pairplot in corso...'):
                fig = create_pairplot(df, features,hue='class')
                st.pyplot(fig,use_container_width=True)
                

        with tab2:
            fig2 = pairplotNoHue(df,features)
            st.pyplot(fig2,use_container_width=True)
                
    else:
        st.warning('⚠️ Seleziona almeno due variabili per visualizzare il pairplot.')
    

