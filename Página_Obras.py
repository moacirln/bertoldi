import streamlit as st
import pandas as pd
import numpy as np
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import classes as cl


@st.cache_data
def criar_obras():
    bd = cl.BD()
    bd.connect()
    bd.cur.execute('SELECT * FROM obras')
    df_obra = pd.DataFrame(bd.cur.fetchall())
    bd.disconnect()
    df_obra.columns = ['id_obra', 'nome_obra', 'nome_empresa','início_vendas','início_obra','duração']
    return df_obra

@st.cache_data
def criar_modelos():
    bd = cl.BD()
    bd.connect()
    bd.cur.execute('SELECT * FROM modelos LEFT OUTER JOIN obras ON modelos.id_obra = obras.id_obra')
    df_modelo = pd.DataFrame(bd.cur.fetchall())
    bd.disconnect()
    df_modelo.columns = ['id_modelo','id_obra','quantidade','preço_venda','contrato','metro2','id_obra2', 'nome_obra', 'nome_empresa','início_vendas','início_obra','duração']
    df_modelo = df_modelo.drop(['id_obra2'], axis=1)
    return df_modelo

@st.cache_data
def criar_orcamento():
    bd = cl.BD()
    bd.connect()
    bd.cur.execute('SELECT * FROM orcamento LEFT OUTER JOIN obras ON orcamento.id_obra = obras.id_obra')
    df_orcamento = pd.DataFrame(bd.cur.fetchall())
    bd.disconnect()
    nome = ['id_orcamento','id_obra','despesa']
    for i in range(1,46):
        novo_nome = f'mes{i}'
        nome.append(novo_nome)
    ult_nomes = ['modelo','id_obra2','nome_obra','nome_empresa','início_vendas','início_obra','duração']
    nome.extend(ult_nomes)
    df_orcamento.columns = nome
    df_orcamento = df_orcamento.drop(['id_obra2'], axis=1)
    return df_orcamento

@st.cache_data
def criar_progresso():
    bd = cl.BD()
    bd.connect()
    bd.cur.execute('SELECT * FROM progresso LEFT OUTER JOIN obras ON progresso.id_obra = obras.id_obra')
    df_progresso = pd.DataFrame(bd.cur.fetchall())
    bd.disconnect()
    df_progresso.columns = ['id_progresso','id_obra','mes','completude','venda','id_obra2', 'nome_obra', 'nome_empresa','início_vendas','início_obra','duração']
    df_progresso = df_progresso.drop(['id_obra2'], axis=1)
    df_progresso['vendas_mes'] = df_progresso['venda'].diff()
    df_progresso['comp_mes'] = df_progresso['completude'].diff()
    df_progresso['completude'] = df_progresso['completude'].astype(float)
    df_progresso['venda'] = df_progresso['venda'].astype(float)
    df_progresso['vendas_mes'] = df_progresso['vendas_mes'].astype(float)
    df_progresso['comp_mes'] = df_progresso['comp_mes'].astype(float)
    return df_progresso

@st.cache_data
def criar_realizado():
    bd = cl.BD()
    bd.connect()
    bd.cur.execute('SELECT * FROM realizado')
    df_realizado = pd.DataFrame(bd.cur.fetchall())
    bd.disconnect()
    df_realizado.columns = ['uuid', 'banco', 'data', 'mov', 'nome', 'cpf_cnpj', 'empresa',
                            'centro_custo', 'descricao', 'credito', 'debito', 'id']
    df_realizado['data'] = df_realizado['data'].dt.strftime('%B %Y')
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
    df_realizado['data'] = df_realizado['data'].dt.strftime('%B %Y')
    df_realizado['vendas_mes_realizado'] = df_realizado['vendas_realizadas'].diff()
    df_realizado['medicao_mes_realizado'] = df_realizado['medicao'].diff()
    df_realizado = df_realizado.drop(['id'], axis=1)
    return df_realizado

def progresso2 (df_progresso):
    df_progresso['vendas_mes'] = df_progresso['venda'].diff()
    df_progresso['comp_mes'] = df_progresso['completude'].diff()
    df_progresso['completude'] = df_progresso['completude'].astype(float)
    df_progresso['venda'] = df_progresso['venda'].astype(float)
    df_progresso['vendas_mes'] = df_progresso['vendas_mes'].astype(float)
    df_progresso['comp_mes'] = df_progresso['comp_mes'].astype(float)
    return df_progresso

def cabecalhos (df, nome):
    novos_nomes_colunas = df.iloc[0]
    df.columns = novos_nomes_colunas
    df = df.drop(df.index[0])
    df.reset_index(drop=True, inplace=True)
    df['Visão'] = nome
    coluna1 = 'Visão'
    colunas = [coluna1] + [col for col in df.columns if col != coluna1]
    df = df[colunas]
    return df

def mdf_vendas_mes (df):
    array_mes = []
    array_vendas = []
    for i, row in enumerate(df.itertuples(), 1):
        array_mes.append(f"Mês {i}")
        array_vendas.append(f"{row.vendas_mes}")
    array_vendas = np.array([array_mes, array_vendas])
    df = pd.DataFrame(array_vendas)
    return df

def mdf_vendas_realizado_mes (df):
    array_mes = []
    array_vendas = []
    for i, row in enumerate(df.itertuples(), 1):
        array_mes.append(f"Mês {i}")
        array_vendas.append(f"{row.vendas_mes_realizado}")
    array_vendas = np.array([array_mes, array_vendas])
    df = pd.DataFrame(array_vendas)
    return df

def mdf_vendas_projetado_mes (df):
    array_mes = []
    array_vendas = []
    for i, row in enumerate(df.itertuples(), 1):
        array_mes.append(f"Mês {i}")
        array_vendas.append(f"{row.vendas_projetadas_atualizadas}")
    array_vendas = np.array([array_mes, array_vendas])
    df = pd.DataFrame(array_vendas)
    return df


def coluna_meses (df):
    array_mes = []
    array_vendasmes = []
    array_compmes = []
    for i, row in enumerate(df.itertuples(), 1):
        array_mes.append(f"Mês {i}")
        array_vendasmes.append(row.vendas_mes)
        array_compmes.append(row.comp_mes)
    df_vendas = pd.DataFrame({
        'mês': array_mes,
        'vendas': array_vendasmes,
        'completude': array_compmes
    })
    return df_vendas

def mdf_receita_real (df, receita):
    array_vendas = []
    for i, row in enumerate(df.itertuples(), 1):
        array_vendas.append(f"{(row.venda*receita)*(row.completude/100)}")
    df_vendas = pd.DataFrame(array_vendas)
    rec = ['rec']
    df_vendas.columns = rec
    df_vendas['rec'] = df_vendas['rec'].astype(float)
    df_vendas['Receita'] = df_vendas['rec'].diff()
    df_vendas['Receita'].fillna(df_vendas['rec'].iloc[0], inplace=True)
    df_vendas = df_vendas.drop('rec', axis=1)
    return df_vendas

def mdf_completude_mes (df):
    array_completude = []
    for i, row in enumerate(df.itertuples(), 1):
        array_completude.append(f"{row.comp_mes}")
    df_completude = pd.DataFrame(array_completude)
    colunas = ['comp.']
    df_completude.columns = colunas
    return df_completude

def datas (df, duracao):
    inicio = df['início_vendas'].values[0]
    datas = pd.date_range(start=inicio, end='2045-01-01', freq='M')
    df_datas = pd.DataFrame({'data': datas})
    df_datas = df_datas.drop(df_datas.index[duracao+1:])
    df_datas['data'] = df_datas['data'].dt.strftime('%B %Y')
    return df_datas

def filtrar_obra(df_obra, obra):
    df_obra = df_obra[df_obra['nome_obra'] == obra]
    return df_obra

def filtrar_realizado(df, empresa, coluna):
    df = df[df[coluna] == empresa]
    return df

#Converte datas
def convert_date(df, coluna):
    data = df[coluna].values[0].astype('M8[s]').astype('O')
    data = data.date()
    data = data.strftime("%d-%m-%Y")
    return data

def montar_projeção_atualizada(df, coluna_projetada, coluna_realizada, nome_nova_coluna):
    df.loc[df['data_controle'] < df['hoje'], nome_nova_coluna] = df[coluna_realizada]
    somatorio_projetado = df.loc[df['data_controle'] < df['hoje'], coluna_projetada].sum()
    somatorio_realizado = df.loc[df['data_controle'] < df['hoje'], nome_nova_coluna].sum()
    df.loc[df['data_controle'] >= df['hoje'], nome_nova_coluna] = (df[coluna_projetada] / somatorio_projetado) * somatorio_realizado
    return df


linhas_orcamento = []
for i in range(1, 46):
    novo_nome = f'mes{i}'
    linhas_orcamento.append(novo_nome)


#INÍCIO DO APP STREAMLIT
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

    # Título 'PÁGINA DE OBRAS'
    st.markdown('<p class="boxed">{}</p>'.format('PÁGINA DE OBRAS'), unsafe_allow_html=True)


    #DATAFRAMES E MÉTRICAS--------------------------------------------------------------------------------------------
    df_obra = criar_obras() #criação do Dataframe Obras
    df_realizado = criar_realizado() #Criação de DataFrade Realizado
    df_progresso_realizado = criar_progresso_realizado() #Criação de DataFrame de Progresso Realizado
    select_obra = st.selectbox('Selecione a Obra', (df_obra['nome_obra'].unique())) #Filtro de Obra na Página
    select_realizado = st.selectbox('Selecione o filtro de realizado', (df_realizado['empresa'].unique()))  # Filtro de Realizado na Página
    hoje = datetime.datetime.today() #dia atual para captura de progresso
    df_obra['estágio'] = hoje - df_obra['início_vendas'] #Criação de estágio
    df_obra['estágio'] = df_obra['estágio'].dt.days #Criação de estágio
    df_obra['estágio'] = df_obra['estágio'].astype(int) #Criação de estágio
    df_obra['estágio'] = df_obra['estágio'] // 30 #Criação de estágio
    df_modelo = criar_modelos() #Criação do DataFrame Modelos
    df_obraf = filtrar_obra(df_obra, select_obra) #df_Obra filtrado por obra
    df_modelof = filtrar_obra(df_modelo, select_obra) #df_modelo filtrado por obra
    df_orcamento = criar_orcamento() #Criação DataFrame de Orçamento
    df_orcamento['TOTAL'] = df_orcamento[linhas_orcamento].sum(axis=1) # Criação da Coluna Total de despesa
    df_orcamentof = filtrar_obra(df_orcamento, select_obra) #df_orcamento filtrado por obra
    df_progresso = criar_progresso()#Criação do DataFrame de Progresso
    df_progressof = filtrar_obra(df_progresso, select_obra) #df_progresso filtrado por obra
    df_realizadof = filtrar_realizado(df_realizado,select_realizado, 'empresa')



    df_realizadou = df_realizado.drop(['uuid', 'banco','mov','nome','cpf_cnpj','empresa','centro_custo','descricao'], axis=1)
    df_realizadoa = df_realizadou.groupby('data').sum()
    df_realizadoa['receita_acumulada_realizado'] = df_realizadoa['credito'].cumsum()
    df_realizadoa['despesa_acumulada_realizado'] = df_realizadoa['debito'].cumsum()
    df_realizadoa['saldo_acumulado_realizado'] = df_realizadoa['credito'] - df_realizadoa['debito']
    df_progresso_realizadof = filtrar_realizado(df_progresso_realizado,select_realizado, 'obra')



    expander_sim1 = st.expander('Simulação de Receita')
    editable_df_progresso = expander_sim1.data_editor(df_progressof,hide_index=True,use_container_width=True, column_config = {'id_progresso':None, 'id_obra': None, 'nome_obra': None,
                                                                                'nome_empresa': None, 'início_vendas': None,
                                                                                'início_obra': None, 'duração':None,
                                                                                'vendas_mes':None,'comp_mes':None, '':None}) # Criação do DataFrame editável do Progresso

    expander_sim2 = st.expander('Simulação de Despesa')
    editable_df_orcamento = expander_sim2.data_editor(df_orcamentof, hide_index=True, use_container_width=True,column_config = {'id_orcamento':None, 'id_obra':None, '':None})  # Criação do DataFrame editável do Progresso

    editable_df_progresso = progresso2(editable_df_progresso)
    editable_df_progresso['vendas_mes'].iloc[0] = editable_df_progresso['venda'].iloc[0]  # Ajuste da primeira linha
    editable_df_progresso['comp_mes'].iloc[0] = editable_df_progresso['completude'].iloc[0]  # Ajuste da primeira linha
    df_datas = datas(df_obraf, df_obraf['duração'].values[0]) #Criaçao do DataFrame de data

    df_txadm = editable_df_orcamento[editable_df_orcamento['despesa'] == 'Tx. Adm']#Criação do DataFrame de Tx. de Administração
    tx_Adm = df_txadm['TOTAL'].sum() #Criação da métrica Tx. de Administração
    totalm2 = (df_modelof['metro2'].values[0]*df_modelof['quantidade'].values[0] #Criação da métrica total de m2
               +df_modelof['metro2'].values[1]*df_modelof['quantidade'].values[1]
               +df_modelof['metro2'].values[2]*df_modelof['quantidade'].values[2])
    totalapt = df_modelof['quantidade'].values[0]+df_modelof['quantidade'].values[1]+df_modelof['quantidade'].values[2] #Criação a métrica totalapt
    area_apt = totalm2/totalapt #Criação da métrica área por apt.
    orc_total = editable_df_orcamento['TOTAL'].sum() #Criação da métrica orçamento total
    orc_total = float(orc_total) #Definição do tipo de dado
    custo_apt = orc_total/totalapt #Criação da métrica custo por Apt.
    custo_m2 = orc_total/totalm2 #Criação da métrica custo por M2
    rec_proj = (df_modelof['preço_venda'].values[0]*df_modelof['quantidade'].values[0] # Criação da métrica receita projetada
               +df_modelof['preço_venda'].values[1]*df_modelof['quantidade'].values[1]
               +df_modelof['preço_venda'].values[2]*df_modelof['quantidade'].values[2])
    receita_media = rec_proj/totalapt #Criação da métrica receita média
    receita_media = float(receita_media) #Tipo de dados
    mes_curso = df_obraf['estágio'].values[0].astype(int) #Criação da métrica de estágio de progresso
    rec_realizada = df_realizadof['credito'].sum()

    # DATAFRAME DE VENDAS APRESENTAÇÃO
    df_vendas = mdf_vendas_mes(editable_df_progresso)
    df_vendas_realizado = mdf_vendas_realizado_mes(df_progresso_realizadof)
    df_vendas = cabecalhos(df_vendas, 'Projetado')
    df_vendas_realizado = cabecalhos(df_vendas_realizado, 'Realizado')


    # DATAFRAME DE RECEITA REAL
    df_receita_real = mdf_receita_real(editable_df_progresso, receita_media)

    # DATAFRAME DE VENDAS COMPLETO
    df_completo = coluna_meses(editable_df_progresso)
    df_completo['receita'] = df_receita_real['Receita']
    df_completo['data'] = df_datas['data']
    df_completo = df_completo[['data','mês','completude','vendas','receita']]


    # DATAFRAME VISUALIZAÇÃO GRÁFICO DESPESA
    df_orcamento_visual = editable_df_orcamento.drop(
        ['modelo', 'id_obra', 'nome_obra', 'nome_empresa', 'início_vendas', 'início_obra', 'duração', 'id_orcamento'],
        axis=1)

    # EXCLUSÃO DE COLUNAS ZERADAS - CONTROLE DE DURAÇÃO
    for i in df_orcamento_visual:
        if df_orcamento_visual[i].sum() == 0:
            df_orcamento_visual = df_orcamento_visual.drop(i, axis=1)

    somas = []
    meses_soma = []

    # DATAFRAME FORMATO USADO NO GRÁFICO
    df_orcamento_grafico = df_orcamento_visual.drop(['despesa', 'TOTAL'], axis=1)
    controle = 1
    for i in df_orcamento_grafico:
        soma = df_orcamento_grafico[i].sum()
        somas.append(soma)
        mes = f'mes{controle}'
        meses_soma.append(mes)
        controle = controle + 1

    df_despesas = pd.DataFrame(meses_soma, columns=['mês'])
    df_despesas_valor = pd.DataFrame(somas, columns=['despesa'])
    df_despesas['valor'] = df_despesas_valor['despesa']

    #DATAFRAME COMPLETO
    df_completo['despesa'] = df_despesas['valor'].astype(float)
    df_completo['saldo'] = df_completo['receita'] - df_completo['despesa']
    df_completo['saldo acumulado'] = df_completo['saldo'].cumsum()
    df_completo['vendas'] = df_completo['vendas'].astype(float)
    df_completo['completude'] = df_completo['completude'].astype(float)
    df_completo['venda acumulada'] = df_completo['vendas'].cumsum()
    df_completo['receita acumulada'] = df_completo['receita'].cumsum()
    df_completo['completude total'] = df_completo['completude'].cumsum()

    df_realizadom = pd.merge(df_completo, df_realizadoa, on='data', how='outer')
    df_realizadom = pd.merge(df_realizadom, df_progresso_realizadof, on='data', how='outer')
    df_realizadom['data_controle'] = pd.to_datetime(df_realizadom['data'], format='%B %Y')
    df_realizadom.columns = ['data', 'mês', 'medição_projetada', 'vendas_projetadas', 'receita_projetada',
                             'despesa_projetada', 'saldo_mês_projetado', 'saldo_acumulado_projetado',
                             'venda_acumulada_projetada', 'receita_acumulada_projetada', 'medição_acumulada_projetada',
                             'receita_realizada', 'despesa_realizada', 'saldo_mês_realizado',
                             'receita_acumulada_realizada', 'despesa_acumulada_realizada', 'saldo_acumulado_realizado',
                             'nome_obra', 'medição_acumulada_realizada', 'vendas_acumulada_realizadas',
                             'vendas_realizadas', 'medição_realizada', 'data_controle']


    df_realizadom = df_realizadom.sort_values(by='data_controle', ascending=True)
    df_realizadom['hoje'] = hoje
    df_realizadom['medição_realizada'] = df_realizadom['medição_realizada'].astype(float)
    df_realizadom['despesa_realizada'] = df_realizadom['despesa_realizada'].astype(float)
    df_realizadom['receita_realizada'] = df_realizadom['receita_realizada'].astype(float)

    #Criação de Coluna Projetada Ajustada de Medição mês a mês
    df_realizadom = (montar_projeção_atualizada
                     (df_realizadom,'medição_projetada',
                      'medição_realizada','medição_projetada_atualizada'))

    # Criação de Coluna Projetada Ajustada de Vendas mês a mês
    df_realizadom = (montar_projeção_atualizada
                     (df_realizadom, 'vendas_projetadas',
                      'vendas_realizadas', 'vendas_projetadas_atualizadas'))

    # Criação de Coluna Projetada Ajustada de Despesa mês a mês
    df_realizadom = (montar_projeção_atualizada
                     (df_realizadom, 'despesa_projetada',
                      'despesa_realizada', 'despesas_projetadas_atualizadas'))

    # Criação de Coluna Projetada Ajustada de Receita mês a mês
    df_realizadom = (montar_projeção_atualizada
                     (df_realizadom, 'receita_projetada',
                      'receita_realizada', 'receita_projetada_atualizada'))

    # Criação de Colunas Projetada Ajustada acumuladas
    df_realizadom['med_acumulada_proj_ajust'] = df_realizadom['medição_projetada_atualizada'].cumsum()
    df_realizadom['vendas_acumulada_proj_ajust'] = df_realizadom['vendas_projetadas_atualizadas'].cumsum()
    df_realizadom['despesas_acumulada_proj_ajust'] = df_realizadom['despesas_projetadas_atualizadas'].cumsum()
    df_realizadom['receita_acumulada_proj_ajust'] = df_realizadom['receita_projetada_atualizada'].cumsum()

    #Criação de saldo projetado ajustado e saldo acumulado projetado ajustado
    df_realizadom['saldo_proj._ajust.'] = df_realizadom['receita_projetada_atualizada']-df_realizadom['despesas_projetadas_atualizadas']
    df_realizadom['saldo_acumulado_proj._ajust.'] = df_realizadom['receita_acumulada_proj_ajust']- df_realizadom['despesas_acumulada_proj_ajust']

    df_realizadom.columns = ['data', 'mês', 'medição_projetada', 'vendas_projetadas', 'receita_projetada',
                             'despesa_projetada', 'saldo_mês_projetado', 'saldo_acumulado_projetado',
                             'venda_acumulada_projetada', 'receita_acumulada_projetada', 'medição_acumulada_projetada',
                             'receita_realizada', 'despesa_realizada', 'saldo_mês_realizado',
                             'receita_acumulada_realizada', 'despesa_acumulada_realizada', 'saldo_acumulado_realizado',
                             'nome_obra', 'medição_acumulada_realizada', 'vendas_acumulada_realizadas',
                             'vendas_realizadas', 'medição_realizada', 'data_controle','hoje','medição_projetada_atualizada',
                             'vendas_projetadas_atualizadas','despesas_projetadas_atualizadas','receita_projetada_atualizada',
                             'med_acumulada_proj_ajust','vendas_acumulada_proj_ajust','despesas_acumulada_proj_ajust',
                             'receita_acumulada_proj_ajust','saldo_proj._ajust.','saldo_acumulado_proj._ajust.']

    df_vendas_ajustado = mdf_vendas_projetado_mes(df_realizadom)
    df_vendas_ajustado = cabecalhos(df_vendas_ajustado, 'Projetado Ajustado')
    df_vendas = pd.concat([df_vendas, df_vendas_realizado,df_vendas_ajustado])


    # INFORMAÇÕES GERAIS -------------------------------------------------------------------------------------
    st.divider()

    st.markdown('<p class="title">{}</p>'.format('INFORMAÇÕES GERAIS'), unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([3, 3, 3, 3])
    container1 = col1.container(border=True, height=63)
    container2 = col2.container(border=True, height=63)
    container3 = col3.container(border=True, height=63)
    container4 = col4.container(border=True, height=63)

    container1.markdown('<p class="titulos"><strong>Identificação</strong></p>', unsafe_allow_html=True)
    container2.markdown('<p class="titulos"><strong>Dimensões</strong></p>', unsafe_allow_html=True)
    container3.markdown('<p class="titulos"><strong>Orçamento e Contrato</strong></p>', unsafe_allow_html=True)
    container4.markdown('<p class="titulos"><strong>Medidas</strong></p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([3,3,3,3])
    container1 = col1.container(border=True, height = 290)
    container2 = col2.container(border=True, height = 290)
    container3 = col3.container(border=True, height = 290)
    container4 = col4.container(border=True, height = 290)

    container1.markdown('<p class="fields"><strong>ID:</strong> {}</p>'.format(df_obraf['id_obra'].values[0]), unsafe_allow_html=True)
    container1.markdown('<p class="fields"><strong>Nome: </strong>{}</p>'.format(df_obraf['nome_obra'].values[0]), unsafe_allow_html=True)
    container1.markdown('<p class="fields"><strong>Início Vendas: </strong>{}</p>'.format(convert_date(df_obraf,'início_vendas')), unsafe_allow_html=True)
    container1.markdown('<p class="fields"><strong>Previsão: </strong>{}</p>'.format(df_obraf['duração'].values[0]), unsafe_allow_html=True)
    container1.markdown('<p class="fields"><strong>Estágio: </strong>{}</p>'.format(df_obraf['estágio'].values[0]/df_obraf['duração'].values[0]), unsafe_allow_html=True)
    container1.markdown('<p class="fields"><strong>% Completo: </strong>{:,.2f}</p>'.format(df_completo['completude total'].values[mes_curso]), unsafe_allow_html=True)
    container1.markdown('<p class="fields"><strong>% Permuta:  </strong>{}</p>'.format('12%'), unsafe_allow_html=True)
    container1.markdown('<p class="fields">{}</p>'.format(''), unsafe_allow_html=True) #ESPAÇO

    container2.markdown('<p class="fields"><strong>Qtd. Modelo 1:  </strong>{}</p>'.format(df_modelof['quantidade'].values[0]), unsafe_allow_html=True)
    container2.markdown('<p class="fields"><strong>Qtd. Modelo 2:  </strong>{}</p>'.format(df_modelof['quantidade'].values[1]), unsafe_allow_html=True)
    container2.markdown('<p class="fields"><strong>Qtd. Modelo 3:  </strong>{}</p>'.format(df_modelof['quantidade'].values[2]), unsafe_allow_html=True)
    container2.markdown('<p class="fields">{}</p>'.format(''), unsafe_allow_html=True)  # ESPAÇO
    container2.markdown('<p class="fields"><strong>Qtd. Total:  </strong>{}</p>'.format(totalapt), unsafe_allow_html=True)
    container2.markdown('<p class="fields"><strong>Total M²:  </strong>{}</p>'.format(totalm2), unsafe_allow_html=True)
    container2.markdown('<p class="fields"><strong>Área/Apt.: </strong>{}</p>'.format(area_apt), unsafe_allow_html=True)
    container2.markdown('<p class="fields">{}</p>'.format(''), unsafe_allow_html=True) #ESPAÇO

    container3.markdown('<p class="fields"><strong>Orçamento 1: </strong>{:,.2f}</p>'.format(df_orcamentof[df_orcamentof['modelo'] == 1]['TOTAL'].sum()), unsafe_allow_html=True)
    container3.markdown('<p class="fields"><strong>Orçamento 2: </strong>{:,.2f}</p>'.format(df_orcamentof[df_orcamentof['modelo'] == 2]['TOTAL'].sum()), unsafe_allow_html=True)
    container3.markdown('<p class="fields"><strong>Orçamento 3: </strong>{:,.2f}</p>'.format(df_orcamentof[df_orcamentof['modelo'] == 3]['TOTAL'].sum()), unsafe_allow_html=True)
    container3.markdown('<p class="fields">{}</p>'.format(''), unsafe_allow_html=True) #ESPAÇO

    container3.markdown('<p class="fields"><strong>Contrato 1: </strong>{:,.2f}</p>'.format(df_modelof['contrato'].values[0]), unsafe_allow_html=True)
    container3.markdown('<p class="fields"><strong>Contrato 2: </strong>{:,.2f}</p>'.format(df_modelof['contrato'].values[1]), unsafe_allow_html=True)
    container3.markdown('<p class="fields"><strong>Contrato 3: </strong>{:,.2f}</p>'.format(df_modelof['contrato'].values[2]), unsafe_allow_html=True)
    col3.markdown('<p class="fields">{}</p>'.format(''), unsafe_allow_html=True) #ESPAÇO

    container4.markdown('<p class="fields"><strong>Receita Modelo1 : </strong>{:,.2f}</p>'.format(df_modelof['preço_venda'].values[0]), unsafe_allow_html=True)
    container4.markdown('<p class="fields"><strong>Receita Modelo2 : </strong>{:,.2f}</p>'.format(df_modelof['preço_venda'].values[1]), unsafe_allow_html=True)
    container4.markdown('<p class="fields"><strong>Receita Modelo3 : </strong>{:,.2f}</p>'.format(df_modelof['preço_venda'].values[2]), unsafe_allow_html=True)
    container4.markdown('<p class="fields">{}</p>'.format(''), unsafe_allow_html=True) #ESPAÇO

    container4.markdown('<p class="fields"><strong>Tx. Adm.: </strong>{:,.2f}</p>'.format(tx_Adm), unsafe_allow_html=True)

    container4.markdown('<p class="fields"><strong>Custo/Apt.: </strong>{:,.2f}</p>'.format(custo_apt), unsafe_allow_html=True)
    container4.markdown('<p class="fields"><strong>Custo/M²: </strong>{:,.2f}</p>'.format(custo_m2), unsafe_allow_html=True)
    container4.markdown('<p class="fields">{}</p>'.format(''), unsafe_allow_html=True) #ESPAÇO

    st.markdown('<p class="receita"><strong>Receita Projetada: </strong>{:,.2f}</p>'.format(rec_proj), unsafe_allow_html=True)
    st.markdown('<p class="receita"><strong>Receita Realizado: </strong>{:,.2f}</p>'.format(rec_realizada), unsafe_allow_html=True)

    st.divider()

    #TABELA GERAL -------------------------------------------------------------------------------------------------
    st.markdown('<p class="title">{}</p>'.format('TABELA GERAL'), unsafe_allow_html=True)


    opcoes_tabela = ['data', 'mês', 'medição_projetada', 'vendas_projetadas', 'receita_projetada',
                             'despesa_projetada', 'saldo_mês_projetado', 'saldo_acumulado_projetado',
                             'venda_acumulada_projetada', 'receita_acumulada_projetada', 'medição_acumulada_projetada',
                             'receita_realizada', 'despesa_realizada', 'saldo_mês_realizado',
                             'receita_acumulada_realizada', 'despesa_acumulada_realizada', 'saldo_acumulado_realizado',
                             'nome_obra', 'medição_acumulada_realizada', 'vendas_acumulada_realizadas',
                             'vendas_realizadas', 'medição_realizada', 'data_controle','hoje','medição_projetada_atualizada',
                             'vendas_projetadas_atualizadas','despesas_projetadas_atualizadas','receita_projetada_atualizada',
                             'med_acumulada_proj_ajust','vendas_acumulada_proj_ajust','despesas_acumulada_proj_ajust',
                             'receita_acumulada_proj_ajust','saldo_proj._ajust.','saldo_acumulado_proj._ajust.']

    options_table = st.multiselect('O que deseja vizualizart na tabela?', opcoes_tabela)
    st.dataframe(df_realizadom, hide_index=True, use_container_width=True, column_order=options_table)

    #RECEITA -----------------------------------------------------------------------------------------
    st.divider()
    st.markdown('<p class="title">{}</p>'.format('RECEITA'), unsafe_allow_html=True)

    col1, col2 = st.columns([3,3])

    #FILTRO DE VISÃO
    metrica = col1.selectbox('Qual métrica da linha?', ('vendas_projetadas','vendas_projetadas_atualizadas','vendas_acumulada_proj_ajust', 'medição_projetada','medição_projetada_atualizada','med_acumulada_proj_ajust', 'medição_acumulada_projetada','medição_acumulada_realizada','venda_acumulada_projetada','vendas_acumulada_realizadas','vendas_realizadas','medição_realizada'))
    metrica2 = col2.selectbox('Qual métrica da barra?', ('receita_projetada', 'receita_projetada_atualizada','receita_acumulada_proj_ajust','receita_realizada','receita_acumulada_realizada', 'receita_acumulada_projetada'))

    # VISUALIZAÇÃO DF_VENDAS
    st.dataframe(df_vendas, hide_index=True, height=160)

    # Dados do gráfico de linha
    x_line = df_realizadom['mês']
    y_line = df_realizadom[metrica]

    # Dados do gráfico de barras (eixo secundário)
    x_bar = df_realizadom['mês']
    y_bar = df_realizadom[metrica2]

    # Criar o gráfico principal de linha
    fig = make_subplots(specs=[[{'secondary_y': True}]])

    fig.add_trace(go.Bar(x=x_bar, y=y_bar, name='Receita', opacity=0.5), secondary_y=True)
    fig.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines+markers', name=metrica,marker=dict(color='purple')))

    fig.update_traces(hovertemplate='%{y:.2f}')
    fig.update_layout(
        xaxis_title='Mês',
        title='Série Temporal da Receita',
        legend=dict(
            x=0.02,
            y=1,
            traceorder="normal",
            orientation="h",
        )
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    #DESPESAS -------------------------------------------------------------------------------------------------
    st.divider()


    st.markdown('<p class="title">{}</p>'.format('DESPESAS'), unsafe_allow_html=True)
    st.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)


    # Dados do gráfico de linha
    x_line = df_completo['mês']
    y_line = df_completo['saldo']

    # Dados do gráfico de linha
    x_line2 = df_realizadom['mês']
    y_line2 = df_realizadom['saldo_mês_realizado']

    # Dados do gráfico de linha
    x_line3 = df_realizadom['mês']
    y_line3 = df_realizadom['saldo_acumulado_proj._ajust.']

    # Dados do gráfico de linha
    x_bar2 = df_realizadom['mês']
    y_bar2 = df_realizadom['receita_realizada']

    # Dados do gráfico de linha
    x_bar3 = df_realizadom['mês']
    y_bar3 = df_realizadom['despesa_realizada']
    y_bar4 = df_realizadom['despesas_projetadas_atualizadas']
    y_bar6 = df_realizadom['receita_projetada_atualizada']

    # Dados do gráfico de barras (eixo secundário)
    x_bar = df_completo['mês']
    y_bar = df_completo['despesa']
    y_bar5 = df_completo['receita']

    selecao_grafico_despesa = st.multiselect('Selecione o que deseja ver', ['despesa projetada', 'receita projetada','receita realizada','despesa realizada','saldo projetado','saldo realizado','receitas projetadas_ajustadas','despesas projetadas_ajustadas','saldo projetado_ajustado'])

    # Criar o gráfico principal de linha
    fig = make_subplots(specs=[[{'secondary_y': True}]])

    if 'despesa projetada' in selecao_grafico_despesa:
        fig.add_trace(go.Bar(x=x_bar, y=y_bar, name='despesas', opacity=0.5,marker=dict(color='red')), secondary_y=True)

    if 'receita projetada' in selecao_grafico_despesa:
        fig.add_trace(go.Bar(x=x_bar, y=y_bar5, name='receita', opacity=0.5), secondary_y=True)

    if 'receita realizada' in selecao_grafico_despesa:
        fig.add_trace(go.Bar(x=x_bar2, y=y_bar2, name='receita_realizada', opacity=0.5, marker=dict(color='green')), secondary_y=True)

    if 'despesa realizada' in selecao_grafico_despesa:
        fig.add_trace(go.Bar(x=x_bar3, y=y_bar3, name='despesa_realizada', opacity=0.5, marker=dict(color='lightblue')), secondary_y=True)

    if 'saldo projetado' in selecao_grafico_despesa:
        fig.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines+markers', name='saldo do período',marker=dict(color='purple')))

    if 'saldo realizado' in selecao_grafico_despesa:
        fig.add_trace(
            go.Scatter(x=x_line2, y=y_line2, mode='lines+markers', name='saldo realizado', marker=dict(color='darkblue')))

    if 'receitas projetadas_ajustadas' in selecao_grafico_despesa:
        fig.add_trace(go.Scatter(x=x_bar, y=y_bar6, name='receitas projetadas_ajustadas',marker=dict(color='yellow')), secondary_y=True)

    if 'despesas projetadas_ajustadas' in selecao_grafico_despesa:
        fig.add_trace(go.Scatter(x=x_bar, y=y_bar4, name='despesas projetadas_ajustadas',marker=dict(color='pink')), secondary_y=True)

    if 'saldo projetado_ajustado' in selecao_grafico_despesa:
        fig.add_trace(go.Scatter(x=x_line3, y=y_line3, mode='lines+markers', name='saldo projetado_ajustado',marker=dict(color='darkgreen')))


    fig.update_layout(barmode='group')
    fig.update_traces(hovertemplate='%{y:.2f}%<br>%{x}')
    fig.update_layout(
        xaxis_title='Mês',
        title='Série Temporal Despesa',
        legend=dict(
            x=0.02,
            y=1,
            traceorder="normal",
            orientation="h",
        )
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    expander = st.expander('Ver tabela de despesas projetadas')
    expander.dataframe(df_orcamento_visual, hide_index=True)

    expander = st.expander('Ver tabela de despesas realizadas')
    expander.dataframe(df_realizadof, hide_index=True, column_order=['data','centro_custo','nome','empresa','descricao','credito','debito','valor'])


    # FLUXO DE CAIXA ---------------------------------------------------------------------------------------------
    st.divider()

    st.markdown('<p class="title">{}</p>'.format('FLUXO DE CAIXA'), unsafe_allow_html=True)
    st.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)

    # DATAFRAME FLUXO DE CAIXA
    #linha0 = df_completo['mês']
    #linha1 = df_completo['receita']
    #linha2 = df_completo['despesa']
    #linha3 = df_completo['saldo']
    #linha4 = df_completo['saldo acumulado']

    #array_fluxo_caixa = np.array([linha0, linha1, linha2, linha3, linha4])
    #df_fluxo = pd.DataFrame(array_fluxo_caixa)
    #df_fluxo = cabecalhos(df_fluxo, 'Projetado')
    #df_fluxo.rename(columns={'Visão': 'Métrica'}, inplace=True)
    #df_fluxo['Métrica'] = ['receita','despesa','saldo','saldo acumulado']

    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(
        go.Scatter(x=df_realizadom['mês'], y=df_realizadom['saldo_acumulado_projetado'], name='Projetado', opacity=0.8,
                   marker=dict(color='red')),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_realizadom['mês'], y=df_realizadom['saldo_acumulado_realizado'], name='Realizado', opacity=0.8,
                   marker=dict(color='blue')),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_realizadom['mês'], y=df_realizadom['saldo_acumulado_proj._ajust.'], name='Projetado Ajustado', opacity=0.8,
                   marker=dict(color='yellow')),
        secondary_y=False,
    )


    fig.update_layout(
        xaxis_title='Mês',
        yaxis_title='Valor',
        title='Série Temporal do Fluxo de Caixa'
    )


    fig.update_traces(hovertemplate='%{y:.2f}')


    st.plotly_chart(fig, use_container_width=True)



if __name__ == '__main__':
        main()