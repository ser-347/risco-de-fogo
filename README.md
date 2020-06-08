# risco-de-fogo
Acurácia do produto risco de fogo no Brasil para diferentes estados, regiões, biomas e sazonalidades

Elaborado por: Eng. Florestal Bruno Vargas Adorno e MSc. Gabriel Máximo da Silva

Doscentes: Dr. Gilberto Ribeiro de Queiroz e Dr. Thales Sehn Körting


Este repositório contém a base de dados e Jupyter Notebook do Projeto 8 da turma SER-347-2020 entitulado: 
**"Acurácia do produto "Risco de fogo" no Brasil para diferentes Estados, Biomas, Regiões e Sazonalidade"**

A finalidade do projeto era avaliar o _acerto do produto risco de fogo da base de queimadas do INPE com base nos dados de focos de calor, da mesma base, para 5 anos de observação no espaço (nos diferentes estados, biomas e regiões do Brasil) e no tempo (diferentes estações e anos 2015-2019)_.

Para detalhar melhor a sequencia de códigos foram criados dois Jupyter Notebooks: Projeto8_Prepocessamento.ipynb e Projeto8_final.ipynb. O primeiro traz mais detalhes da sequência de tratamento dos dados, a serem analisados no segundo. Além disso, foi criado o módulo 'riscofogo.py' que reúne funções dos comandos criados nos dois jupyter notebooks para auxiar a replicação da mesma sequência de códigos para diferentes anos analisados.

Embora o projeto tenha focado nos anos 2015 - 2019, acredita-se que ele é flexível para acrescentar dados de outros anos, **desde que contenham informações de risco de fogo na tabela de atributos da base de dados do INPE.**

Ao fazer o download do repositório, descompactar a pasta em Dados_focos.zip na mesma pasta onde estão os arquivos 
Projeto8_final.ipynb e Projeto8_Prepocessamento.ipynb.

Seguem as versões das principais bibliotecas utilizadas para esse projeto:

 - Geopandas 0.7.0 (Canal condaforge)

 - Pandas 1.0.3

 - numpy 1.18.1

 - matplotlib 3.2.1

 - statsmodel 0.11.1
