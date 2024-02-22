import streamlit as st
import pandas as pd
import classes as cl

def main():
    st.set_page_config(page_title='Obras', layout='wide', initial_sidebar_state='collapsed')

    uploaded_realizado = st.file_uploader("Escolha um arquivo de conciliação bancária")

    if uploaded_realizado:
        df = pd.read_csv(uploaded_realizado,decimal=',', sep=',')
        df['CREDITO'].replace('-', None, inplace=True)
        df['DEBITO'].replace('-', None, inplace=True)
        df['ID'].replace('-', None, inplace=True)
        df = df.dropna(how='all')
        df['CREDITO'].fillna(0, inplace=True)
        df['ID'].fillna(0, inplace=True)
        df['DEBITO'].fillna(0, inplace=True)

        df['CREDITO'] = df['CREDITO'].replace({'\.': ''}, regex=True)
        df['DEBITO'] = df['DEBITO'].replace({'\.': ''}, regex=True)
        df = df.replace(to_replace=',', value='.', regex=True)

        df['CREDITO'] = df['CREDITO'].astype(float)
        df['DEBITO'] = df['DEBITO'].astype(float)
        df['DATA'] = pd.to_datetime(df['DATA'], errors='coerce')

        st.dataframe(df, use_container_width=True)


    uploaded_realizado_progresso = st.file_uploader("Escolha um arquivo de progresso realizado")
    if uploaded_realizado_progresso:
        df_progresso_realizado = pd.read_csv(uploaded_realizado_progresso, decimal=',', sep=',')
        df_progresso_realizado['Medicao'] = df_progresso_realizado['Medicao'].replace({'\.': ''}, regex=True)
        df_progresso_realizado = df_progresso_realizado.replace(to_replace=',', value='.', regex=True)
        df_progresso_realizado['Medicao'] = df_progresso_realizado['Medicao'].astype(float)
        df_progresso_realizado['Venda_Realizada'] = df_progresso_realizado['Venda_Realizada'].astype(int)
        st.dataframe(df_progresso_realizado, use_container_width=True)


    bd = cl.BD()

    if st.button('Gravar Realizado'):
        bd.connect()
        bd.cur.execute('DELETE FROM realizado')
        bd.conn.commit()
        for row in df.itertuples(index=False):
            query = 'INSERT INTO realizado(data, nome, empresa, centro_custo, descricao, credito, debito) VALUES (%s, %s, %s,%s, %s, %s, %s)'
            params = (row.DATA, row.NOME, row.EMPRESA,row.CENTRO_CUSTO, row.DESCRICAO,row.CREDITO, row.DEBITO)
            bd.cur.execute(query, params)
            bd.conn.commit()
        bd.disconnect()
        bd.connect()
        bd.cur.execute('DELETE FROM progresso_realizado')
        bd.conn.commit()
        for row in df_progresso_realizado.itertuples(index=False):
            query = 'INSERT INTO progresso_realizado(data, obra, medicao, vendas) VALUES (%s, %s, %s,%s)'
            params = (
            row.Data, row.Obra, row.Medicao, row.Venda_Realizada)
            bd.cur.execute(query, params)
            bd.conn.commit()
        bd.disconnect()



if __name__ == '__main__':
    main()
