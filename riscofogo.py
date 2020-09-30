# importanto bibliotecas
import geopandas as gpd # trabalhar com GeoDataFrame
import pandas as pd # trabalhar com DataFrame
import numpy as np # trabalhar com matrizes homogeneas de multidimensões
import matplotlib.pyplot as plt


# FUNÇÕES DO JUPYTER NOTEBOOK PROJETO8_Preprocessamento

# a função abaixo realizará os processamentos iniciais de um GeoDataframe contendo dados de foco de calor inseridos pelo usuário como argumento da função

def preproc (n):
    
# a função 'dropna' elimina as linhas com valores sem dados (NaN ou None) de uma coluna indicada no argumento subset
# a função 'drop' exclui colunas indicadas em uma lista, inserida no argumento 'columns', não desejadas no processamento
# a função 'sample' permite amostrar os dados aleatoriamente, com pesos que variam de 0-1, sendo que mais próximo de 1, maior número de dados amostrados.
    focos_final = n.dropna(subset=['riscofogo']).drop(columns=['frp','diasemchuv']).sample(frac=0.05, replace=False, random_state=1)
    
# Para iterar e fazer operações com a variação temporal no DataFrame ou GeoData frame, a função to_datetime do Pandas permite alterar o tipo de dado (booleano, inteiro, objeto) para 'datetime64[ns]'
    focos_final['datahora'] = pd.to_datetime(focos_final['datahora']) 
    
# criando uma coluna com níveis de riscofogo, de acordo com definido pelos autores do método.
    
# criando lista de condições
    conditions = [
        focos_final['riscofogo'] > 0.95,
        focos_final['riscofogo'] > 0.7,
        focos_final['riscofogo'] > 0.4,
        focos_final['riscofogo'] > 0.15]
# criando lista de escolhas
    choices = ['CRITICO', 'ALTO', 'MEDIO', 'BAIXO']
# a função select da numpy permite selecionar condições uma série e relacionar em uma correspondente de outra série um valor escolhido; o argumento default estabelece a escolha para os valores que não tiverem condições definidas.
    focos_final['risco_classe'] = np.select(conditions, choices, default='MINIMO')
    
# criar uma coluna de 'dia do ano', por meio da função 'dt.dayofyear' do Pandas aplicada sobre uma serie
    focos_final['dia do ano'] = focos_final['datahora'].dt.dayofyear
# pela coluna dias do ano é mais fácil definir a estação correspondente pela mesma função select do numpy
    conditions_estacao = [
        focos_final['dia do ano'] > 356, 
        focos_final['dia do ano'] > 264,
        focos_final['dia do ano'] > 172,
        focos_final['dia do ano'] > 80]
    choices_estacao = ['VERÃO','PRIMAVERA','INVERNO','OUTONO']
    focos_final['estacoes'] = np.select(conditions_estacao, choices_estacao, default='VERÃO')
    
# criando coluna de legenda para o mapa
    conditions_legenda = [
    focos_final['riscofogo'] > 0.95,
    focos_final['riscofogo'] > 0.7,
    focos_final['riscofogo'] > 0.4,
    focos_final['riscofogo'] > 0.15]
    choices_legenda = ['1','2', '3', '4']
    focos_final['legenda'] = np.select(conditions_legenda, choices_legenda, default="5")
    
# abrindo arquivo shape de unidades federativas para incluir dados de regiao no dataframe e convertendo sua projeção para a mesma dos focos de calor: EPSG:4326
    UF = gpd.read_file('uf-2018/BRUFE250GC_SIR.shp', encoding='utf-8').to_crs('EPSG:4326')
    
# deletando colunas que não serão necessárias para o dataframe final
    UF_Regiao = UF.drop(columns=['NM_ESTADO','CD_GEOCUF'])
    
# a função do GeoPandas sjoin com a opção intersect transporta as séries de dados do geodataframe no segundo argumento para  o primeiro a partir da relação de suas geometrias.
    focos_final = gpd.sjoin(focos_final, UF_Regiao, how='inner', op='intersects')
    
# retorna o resultado final da função   
    return focos_final
# As próximas funcoes (estacoes, estado, regiao, bioma) criarão tabelas dinâmicas a partir da função do Pandas 'pivot'_table, para cada delimitação geográfica que se pretende analisar o acerto do risco de fogo.

def pvtestacoes (estacoes):

# como argumento da função temos na sequência: 1- o (Geo)dataframe de entrada, 2- a coluna cujos valores servirão de base para a operação definida no argumento 'aggfunc', 3- a coluna do (Geo)dataframe que vai compor os índices (as linhas) da tabela dinâmica, 4- a coluna do geodataframe que vai compor as colunas da tabela dinâmica, 5 a operação que será realizada sobre os valores definidos em 2 (que no caso é a contagem - atribui-se valor 1 para cada célula com dados), 6- valor para preencher células com valores que faltam, 7 - opção se quer apresentar o somatório das linhas e colunas na tabela dinâmica. 
    pvt_estacoes = pd.pivot_table(estacoes, values=['riscofogo'], index=['estacoes'],
                     columns=['risco_classe'], aggfunc=['count'],
                     fill_value=0, margins=False) 
    
    return pvt_estacoes
 
# idem para os dois últimos comentários    
def pvtestado (estado):

    pvt_estado = pd.pivot_table(estado, values=['riscofogo'], index=['estado'],
                     columns=['risco_classe'], aggfunc=['count'],
                     fill_value=0, margins=False)
    
    return pvt_estado

# idem
def pvtregiao (regiao):
    
    pvt_regiao = pd.pivot_table(regiao, values=['riscofogo'], index=['NM_REGIAO'],
                     columns=['risco_classe'], aggfunc=['count'],
                     fill_value=0, margins=False)
    
    return pvt_regiao
# idem  
def pvtbioma (bioma):
    
    pvt_bioma = pd.pivot_table(bioma, values=['riscofogo'], index=['bioma'],
                     columns=['risco_classe'], aggfunc=['count'],
                     fill_value=0, margins=False)
    
    return pvt_bioma

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# FUNÇÕES DO JUPYTER NOTEBOOK PROJETO8_Final

def mapasporano (focos):


    UF = gpd.read_file('uf-2018/BRUFE250GC_SIR.shp', encoding='utf-8').to_crs('EPSG:4326')

    new_legend = {'1':'Crítico', '2':'Alto', '3':'Médio', '4':'Baixo', '5':'Mínimo'}

    f,ax = plt.subplots(1,4,figsize=(20,20))
    UF.plot(ax=ax[0], color='white', edgecolor='k');
    focos[focos.estacoes=='VERÃO'].plot(ax=ax[0], marker='x', column = 'legenda', cmap='RdYlGn', markersize=3,legend = True)
    UF.plot(ax=ax[1], color='white', edgecolor='k');
    focos[focos.estacoes=='OUTONO'].plot(ax=ax[1], marker='x', column = 'legenda', cmap='RdYlGn', markersize=3,legend = False)
    UF.plot(ax=ax[2], color='white', edgecolor='k');
    focos[focos.estacoes=='INVERNO'].plot(ax=ax[2], marker='x', column = 'legenda', cmap='RdYlGn', markersize=3,legend = False)
    UF.plot(ax=ax[3], color='white', edgecolor='k');
    focos[focos.estacoes=='PRIMAVERA'].plot(ax=ax[3], marker='x', column = 'legenda', cmap='RdYlGn', markersize=3,legend = False)
    ax[0].set_title('Verão - '+ str(np.unique(focos.datahora.dt.year)))
    ax[1].set_title('Outono - '+ str(np.unique(focos.datahora.dt.year)))
    ax[2].set_title('Inverno - '+ str(np.unique(focos.datahora.dt.year)))
    ax[3].set_title('Primavera - '+str(np.unique(focos.datahora.dt.year)))

    def replace_legend_items(legend, mapping):
        for txt in legend.texts:
            for k,v in mapping.items():
                if txt.get_text() == str(k):
                    txt.set_text(v)
# Escolhendo label para legenda
    replace_legend_items(ax[0].get_legend(), new_legend)

    mapa = plt.show()
        
    return mapa





# essa função apresenta uma média para todos os anos analisados a partir da quantidade de tabelas dinâmicas geradas. Para 5 anos analisados o usuário entra como argumento uma lista contendo tabela dinâmica para cada ano (e.g. [pvt_ano1, pvt_ano2, pvt_ano3, pvt_ano4, pvt_ano5])

def mediadosanos (x):

# será realizada soma de matrizes seguida da divisão do número de itens dentro da lista (tamanho da lista).
    soma = 0
    for i in range(len(x)):
        soma += x[i] # a variável soma recebe e adiciona a ela mesma o item na posição i até iterar sobre todos os itens.

    average = soma/len(x)

# organizando as colunas de nível crítico a mínimo
    average = average[[
    ('count', 'riscofogo', 'CRITICO'),
    ('count', 'riscofogo', 'ALTO'),
    ('count', 'riscofogo', 'MEDIO'),
    ('count', 'riscofogo', 'BAIXO'),
    ('count', 'riscofogo', 'MINIMO')]]
    
    return average

