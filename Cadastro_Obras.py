import streamlit as st
import pandas as pd
import classes as cl
import numpy as np

def main():
    # Estilos de Texto ---------------------------------------
    st.markdown("""
                   <style>
                       .boxed {
                           text-align: center;
                           font-size: 70px;
                           font-weight: bold;
                           font-family: 'Helvetica', sans-serif;
                       }
                   </style>
               """, unsafe_allow_html=True)

    st.markdown("""
                       <style>
                           .title {
                               font-size: 42px;
                               text-align: center;
                               font-weight: bold;
                               font-family: 'Helvetica', sans-serif;
                               margin-bottom: 25px;
                           }
                       </style>
                   """, unsafe_allow_html=True)

    st.markdown("""
                       <style>
                           .fields {
                               font-size: 20px;
                               text-align: left;
                               margin-bottom: 5px;
                           }
                       </style>
                   """, unsafe_allow_html=True)

    st.markdown("""
                          <style>
                              .titulos {
                                  font-size: 25px;
                                  text-align: center;
                                  margin-top: -5px;
                              }
                          </style>
                      """, unsafe_allow_html=True)

    st.markdown("""
                              <style>
                                  .receita {
                                      font-size: 32px;
                                      text-align: center;
                                      margin-top: 0px;
                                  }
                              </style>
                          """, unsafe_allow_html=True)

    st.markdown("""
                           <style>
                               .headersidebar {
                                   font-size: 18px;
                                   text-align: center;
                               }
                           </style>
                       """, unsafe_allow_html=True)

    #BACK-END
    #Descobrindo o ID de preenchimento
    bd = cl.BD()
    bd.connect()
    bd.cur.execute('SELECT id_obra FROM obras ORDER BY id_obra DESC LIMIT 1')
    id = bd.cur.fetchone()
    bd.disconnect()
    if id:
        id = id[0]
        id = int(id) + 1
    else:
        id = 1


    #Visual
    #Definição de Colunas no Título
    col1, col2 = st.columns([6,3])
    # Adicione o título dentro da caixa
    st.markdown('<p class="boxed">{}</p>'.format('CADASTRO DE OBRA'), unsafe_allow_html=True)

    #Colunas Parte 1
    col1,col2,col3 = st.columns([0.5,2,6])

    # Preenchimento do ID
    col1.markdown('<p class="fields">{}</p>'.format('ID:'), unsafe_allow_html=True)
    col2.markdown('<p class="fields">{}</p>'.format(id), unsafe_allow_html=True)

    #Colunas Parte 2
    col1, col2, col3, col4 = st.columns([6, 4, 3,3])

    #Nome da Obra e Empresa
    col1.markdown('<p class="fields">{}</p>'.format('Nome da Obra:'), unsafe_allow_html=True)
    nome_obra = col1.text_input("nome_obra", label_visibility = 'collapsed')

    col1.markdown('<p class="fields">{}</p>'.format('Empresa:'), unsafe_allow_html=True)
    nome_empresa = col1.text_input("nome_empresa", label_visibility='collapsed')


    st.divider()

    #Colunas Parte 3
    col1, col2 = st.columns([3, 6])

    #Título
    st.markdown('<p class="title">{}</p>'.format('DATAS'), unsafe_allow_html=True)

    #Colunas Parte 3 Datas
    col1, col2, col3 = st.columns([3, 3, 3])

    #Campos de Data
    col1.markdown('<p class="fields">{}</p>'.format('Início das Vendas'), unsafe_allow_html=True)
    vendinha = col1.date_input("Inicio_Vendas", label_visibility='collapsed')
    col2.markdown('<p class="fields">{}</p>'.format('Início das Obras'), unsafe_allow_html=True)
    obrinha = col2.date_input("Inicio_Obras", label_visibility='collapsed')
    col3.markdown('<p class="fields">{}</p>'.format('Duração (Meses)'), unsafe_allow_html=True)
    Duracao = col3.number_input("Deuração", label_visibility='collapsed',)

    st.divider()

    # Colunas Título
    col1,col3,col2 = st.columns([3,2,3])
    #Título
    st.markdown('<p class="title">{}</p>'.format('ESCOPO'), unsafe_allow_html=True)

    #Colunas Parte4
    col1, col2, col3, col4 = st.columns([3, 3, 3, 3])

    #Quantidades e Preços de Venda
    col1.markdown('<p class="fields">{}</p>'.format('Qtd. MOD1'), unsafe_allow_html=True)
    Qtd_mod1 = col1.number_input("Qtd_mod1", label_visibility='collapsed')
    col2.markdown('<p class="fields">{}</p>'.format('Contrato MOD1'), unsafe_allow_html=True)
    contrato = col2.number_input("contrato1", label_visibility='collapsed')
    col3.markdown('<p class="fields">{}</p>'.format('R$ Médio MOD1'), unsafe_allow_html=True)
    Prç_mod1 = col3.number_input("Prç Médio Mod1", label_visibility='collapsed')
    col4.markdown('<p class="fields">{}</p>'.format('M²/Apt. 1'), unsafe_allow_html=True)
    metro2 = col4.number_input("metro21", label_visibility='collapsed')

    col1.markdown('<p class="fields">{}</p>'.format('Qtd. MOD2'), unsafe_allow_html=True)
    Qtd_mod2 = col1.number_input("Qtd_mod2", label_visibility='collapsed')
    col2.markdown('<p class="fields">{}</p>'.format('Contrato MOD2'), unsafe_allow_html=True)
    contrato2 = col2.number_input("contrato2", label_visibility='collapsed')
    col3.markdown('<p class="fields">{}</p>'.format('R$ Médio MOD2'), unsafe_allow_html=True)
    Prç_mod2 = col3.number_input("Prç Médio Mod2", label_visibility='collapsed')
    col4.markdown('<p class="fields">{}</p>'.format('M²/Apt. 2'), unsafe_allow_html=True)
    metro22 = col4.number_input("metro22", label_visibility='collapsed')

    col1.markdown('<p class="fields">{}</p>'.format('Qtd. MOD3'), unsafe_allow_html=True)
    Qtd_mod3 = col1.number_input("Qtd_mod3", label_visibility='collapsed')
    col2.markdown('<p class="fields">{}</p>'.format('Contrato MOD3'), unsafe_allow_html=True)
    contrato3 = col2.number_input("contrato3", label_visibility='collapsed')
    col3.markdown('<p class="fields">{}</p>'.format('R$ Médio MOD3'), unsafe_allow_html=True)
    Prç_mod3 = col3.number_input("Prç Médio Mod3", label_visibility='collapsed')
    col4.markdown('<p class="fields">{}</p>'.format('M²/Apt. 3'), unsafe_allow_html=True)
    metro23 = col4.number_input("metro23", label_visibility='collapsed')

    st.divider()

    # Colunas Parte 5
    col1, col3, col2 = st.columns([3, 2, 3])
    st.markdown('<p class="title">{}</p>'.format('ORÇAMENTO'), unsafe_allow_html=True)

    uploaded_orcamento = st.file_uploader("Escolha um arquivo de orçamento")
    if uploaded_orcamento:
        df_orcamento = pd.read_csv(uploaded_orcamento)
        st.dataframe(df_orcamento)

    bd.disconnect()

    st.divider()

    col1, col3, col2 = st.columns([3, 2, 3])
    st.markdown('<p class="title">{}</p>'.format('MEDIÇÃO'), unsafe_allow_html=True)

    uploaded_progresso = st.file_uploader("Escolha um arquivo de progresso")
    if uploaded_progresso:
        df_progresso = pd.read_csv(uploaded_progresso)
        st.dataframe(df_progresso)

        # BOTÃO DE GRAVAR PROGRESSO
        if st.button('Gravar Progresso'):
            bd.connect()
            for row in df_progresso.itertuples(index=False):
                query = 'INSERT INTO progresso(id_obra, mes, completude, venda) VALUES (%s, %s, %s, %s)'
                params = (id, row.Mês, row.Completude, row.Venda)
                bd.cur.execute(query, params)
                bd.conn.commit()

            bd.connect()
            for row in df_orcamento.itertuples(index=False):
                query = 'INSERT INTO orcamento(id_obra, despesa, mes1,mes2,mes3,mes4,mes5,mes6,mes7,mes8,mes9,mes10,mes11,mes12,mes13,mes14,mes15,mes16,mes17,mes18,mes19,mes20,mes21,mes22,mes23,mes24,mes25,mes26,mes27,mes28,mes29,mes30,mes31,mes32,mes33,mes34,mes35,mes36,mes37,mes38,mes39,mes40,mes41,mes42,mes43,mes44,mes45,modelo) VALUES (%s, %s, %s,%s, %s, %s,%s, %s,%s, %s, %s,%s, %s, %s,%s, %s,%s, %s, %s,%s, %s, %s,%s, %s,%s, %s, %s,%s, %s, %s,%s, %s,%s, %s, %s,%s, %s, %s,%s, %s,%s, %s, %s,%s, %s, %s,%s, %s)'
                params = (
                id, row.Despesa, row.mes1, row.mes2, row.mes3, row.mes4, row.mes5, row.mes6, row.mes7, row.mes8,
                    row.mes9, row.mes10, row.mes11, row.mes12, row.mes13, row.mes14, row.mes15, row.mes16, row.mes17,
                    row.mes18, row.mes19, row.mes20, row.mes21, row.mes22, row.mes23, row.mes24, row.mes25, row.mes26,
                    row.mes27, row.mes28, row.mes29, row.mes30, row.mes31, row.mes32, row.mes33, row.mes34, row.mes35,
                    row.mes36, row.mes37, row.mes38, row.mes39, row.mes40, row.mes41, row.mes42, row.mes43, row.mes44,
                    row.mes45, row.modelo)
                bd.cur.execute(query, params)
                bd.conn.commit()

            bd.connect()
            query = 'INSERT INTO obras(nome_obra, nome_empresa, init_vendas, init_obra, duracao) VALUES (%s, %s, %s, %s, %s)'
            params = (nome_obra, nome_empresa, vendinha, obrinha, Duracao)
            bd.cur.execute(query, params)
            bd.conn.commit()
            query = 'INSERT INTO modelos(id_obra, quantidade, preço_venda, contrato, metro2) VALUES (%s, %s, %s, %s, %s)'
            params = (id, Qtd_mod1, Prç_mod1, contrato, metro2)
            bd.cur.execute(query, params)
            bd.conn.commit()
            query = 'INSERT INTO modelos(id_obra, quantidade, preço_venda, contrato, metro2) VALUES (%s, %s, %s, %s, %s)'
            params = (id, Qtd_mod2, Prç_mod2, contrato2, metro22)
            bd.cur.execute(query, params)
            bd.conn.commit()
            query = 'INSERT INTO modelos(id_obra, quantidade, preço_venda, contrato, metro2) VALUES (%s, %s, %s, %s, %s)'
            params = (id, Qtd_mod3, Prç_mod3, contrato3, metro23)
            bd.cur.execute(query, params)
            bd.conn.commit()

        bd.disconnect()


if __name__ == '__main__':
        main()