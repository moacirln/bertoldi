import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import classes as cl

@st.cache_data
def criar_realizado():
    bd = cl.BD()
    bd.connect()
    bd.cur.execute('SELECT * FROM realizado')
    df_realizado = pd.DataFrame(bd.cur.fetchall())
    bd.disconnect()
    df_realizado.columns = ['uuid', 'banco', 'data', 'mov', 'nome', 'cpf_cnpj', 'empresa',
                            'centro_custo', 'descricao', 'credito', 'debito', 'id']
    df_realizado['valor'] = df_realizado['credito']-df_realizado['debito']
    df_realizado = df_realizado.drop(['id'], axis=1)
    return df_realizado

@st.cache_data
def criar_progresso_realizado():
    bd = cl.BD()
    bd.connect()
    bd.cur.execute('SELECT * FROM progresso_realizado')
    df_realizado = pd.DataFrame(bd.cur.fetchall())
    bd.disconnect()
    df_realizado.columns = ['id', 'data', 'obra', 'medicao', 'vendas_realizadas']
    df_realizado['vendas_mes_realizado'] = df_realizado['vendas_realizadas'].diff()
    df_realizado['medicao_mes_realizado'] = df_realizado['medicao'].diff()
    df_realizado = df_realizado.drop(['id'], axis=1)
    return df_realizado


def main():
    st.set_page_config(page_title='Obras', layout='wide', initial_sidebar_state='collapsed')

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

    #Criação do DataFrame
    df_realizado = criar_realizado()
    df_realizado['data'] = pd.to_datetime(df_realizado['data'],format='%d/%m/%y').dt.date
    df_progresso = criar_progresso_realizado()
    df_progresso['data'] = pd.to_datetime(df_progresso['data'], format='%d/%m/%y').dt.date

    #Sidebar --------------------------------------------------------------------------------
    sidebar = st.sidebar
    sidebar.title('FILTRO DE DATA')
    inicio_data = sidebar.date_input('Data de Início',df_realizado['data'].min())
    final_data = sidebar.date_input('Data Final', df_realizado['data'].max())



    #BACK_END -------------------------------------------------------------------------------
    df_realizadof = df_realizado[df_realizado['data'].between(inicio_data, final_data)]
    df_progressof = df_progresso[df_progresso['data'].between(inicio_data, final_data)]
    df_realizadovf = df_realizadof.groupby('data').sum().reset_index()
    df_realizadovf = df_realizadovf.drop(['banco','mov','nome', 'empresa','cpf_cnpj','uuid','centro_custo','descricao'], axis=1)
    df_realizadovf['saldo'] = df_realizadovf['valor'].cumsum()
    df_progressovf = df_progressof.groupby('obra').max()
    df_progressovf = df_progressovf.drop(['data','vendas_mes_realizado','medicao_mes_realizado'], axis=1)
    df_realizadovfg = df_realizadof.drop(['data','banco','mov','nome','cpf_cnpj','uuid','centro_custo','descricao'], axis=1)
    df_realizadovfg = df_realizadovfg.groupby('empresa').sum().reset_index()
    df_realizadovfg.columns = ['obra','receita','despesa','saldo']

    df_progressovf = pd.merge(df_progressovf, df_realizadovfg, on='obra', how='inner')


    # Visual-----------------------------------------------------------------------------------------------
    col1, col2 = st.columns([4, 5])

    st.markdown('<p class="boxed">{}</p>'.format('VISÃO GERAL'), unsafe_allow_html=True)


    #CONTAINER COM INFORMAÇÔES BÁSICAS ---------------------------------------------------------------------
    col1, col2, col3 = st.columns([2,4,2])
    container = col2.container(border=True, height=170)
    container.markdown('<p class="titulos"><strong>Receita:</strong> {}</p>'.format(df_realizadof['credito'].sum()), unsafe_allow_html=True)
    container.markdown('<p class="titulos"><strong>Despesa:</strong> {}</p>'.format(df_realizadof['debito'].sum()), unsafe_allow_html=True)
    container.markdown('<p class="titulos"><strong>Saldo:</strong> {}</p>'.format(df_realizadovf['credito'].sum()-df_realizadovf['debito'].sum()), unsafe_allow_html=True)

    #PRIMEIRO GRÁFICO --------------------------------------------------------------------------------------
    st.divider()
    st.markdown('<p class="title">{}</p>'.format('OBRAS'), unsafe_allow_html=True)

    st.dataframe(df_progressovf, hide_index=True, use_container_width=True, height=100)

    select = st.selectbox('Qual dimensão deseja ver', ('Série Temporal', 'Por Obra'))

    if select == 'Série Temporal':
        x_line = df_realizadovf['data']
        y_line = df_realizadovf['credito']
        y_line2 = df_realizadovf['debito']
    else:
        x_line = df_progressovf['obra']
        y_line = df_progressovf['receita']
        y_line2 = df_progressovf['despesa']

    if select == 'Série Temporal':
        fig = make_subplots(specs=[[{'secondary_y': False}]])
        fig.add_trace(go.Scatter(x=x_line, y=y_line, name='receitas', opacity=0.5, marker=dict(color='yellow')))
        fig.add_trace(go.Scatter(x=x_line, y=y_line2, name='despesas', opacity=0.5, marker=dict(color='red')))
    else:
        fig = make_subplots(specs=[[{'secondary_y': False}]])
        fig.add_trace(go.Bar(x=x_line, y=y_line, name='receitas', opacity=0.5, marker=dict(color='yellow')))
        fig.add_trace(go.Bar(x=x_line, y=y_line2, name='despesas', opacity=0.5, marker=dict(color='red')))

    fig.update_layout(
        xaxis_title='Dimensão',
        yaxis_title='Métrica',
    )
    st.plotly_chart(fig,use_container_width=True)

    st.divider()

    st.markdown('<p class="title">{}</p>'.format('FLUXO DE CAIXA'), unsafe_allow_html=True)

    df_realizadovf['data'] = pd.to_datetime(df_realizadovf['data'], errors='coerce', format='%B %Y')
    df_realizadovf['mês'] = df_realizadovf['data'].dt.month
    df_realizadovf['ano'] = df_realizadovf['data'].dt.year
    df_realizadovf['mês_ano'] = df_realizadovf['mês'].astype(str) + ' ' + df_realizadovf['ano'].astype(str)
    df_realizadovf = df_realizadovf.drop(['mês','ano','data'], axis=1)
    df_realizadovf = df_realizadovf.groupby('mês_ano').sum().reset_index()
    df_realizadovf['data'] = pd.to_datetime(df_realizadovf['mês_ano'], errors='coerce')
    df_realizadovf['data'] = pd.to_datetime(df_realizadovf['mês_ano'], errors='coerce')
    df_realizadovf = df_realizadovf.drop(['mês_ano'], axis=1)
    df_realizadovf['mês_ano'] = df_realizadovf['data'].dt.strftime('%B %Y')
    df_realizadovf.columns = ['receita','despesa','saldo','saldo acumulado','data','mês_ano']

    st.dataframe(df_realizadovf, use_container_width=True, column_order=['data','mês_ano','receita','despesa','saldo','saldo acumulado'], hide_index=True)


    fig = make_subplots(specs=[[{'secondary_y': False}]])

    x_line = df_realizadovf.sort_values(by='data')['mês_ano']
    y_line = df_realizadovf['saldo acumulado']

    fig.add_trace(go.Scatter(x=x_line, y=y_line, name='saldo acumulado', opacity=0.5, marker=dict(color='yellow')))

    fig.update_layout(
        xaxis_title='Dimensão',
        yaxis_title='Métrica',
        title = 'Fluxo de Caixa',
    )

    st.plotly_chart(fig,use_container_width=True)





if __name__ == '__main__':
    main()