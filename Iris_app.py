import streamlit as st

def main():
    pages = {
        "Iris":[
            st.Page("Iris_eda.py",title="EDA"),
            st.Page("Iris_inf.py",title="Inferenza")
        ]
    }

    pg = st.navigation(pages)
    pg.run()

if __name__ == '__main__':
    main()