# matchmatch.py Programa usado para criar match com recurso de
# duas planilhas de mentores e mentorandos, contendo ordem de
# prioridades de atividades para realizar o match.
#
#   LAST MODIFIED: 15/07/2020 BY GIOVANNI PRIETO AND VITORIA CANDEIRA
#   CREATED BY GIOVANNI PRIETO(git: GioDSP) AND VITORIA CANDEIRA

# FUNCTIONS:

def mentoradosSemRepetir(mentorados):
    """

    mentoradosSemRepetir Funcao que recebe elementos de mentorados para ordenar
    a lista de itens de mentorados priorizando quem tem menos
    opcoes de atividades no formulario

    Input variables:
    mentorados       -> Itens contidos no csv. Type: CSV Object

    Outputs:
    len(sem_repetir) -> Numero de atividades unicas. Type: Integer

    """
    atividades = []
    for coluna in mentorados:
        if coluna.find("Ordem de prioridade [") != -1: #Procura 'Ordem de prioridade' nas colunas. Caso não encontre,
                                                       #find retorna -1.
            atividades.append(coluna)
    sem_repetir = []                                   #Armazena as atividades unicas.
    for atividade in atividades:
        if atividade in sem_repetir:
            pass
        else:
            sem_repetir.append(atividade)
    return len(sem_repetir)

def matchFunction(mentorados_csv, mentores_csv, cont_ativ):
    """

    matchFunction Funcao que faz o match entre mentor e mentorado
    dependendo do critério de ordem de prioridade.

    Input variables:
    mentorados_csv    -> Lista de dicionarios no qual as chaves sao os titulos das colunas do csv de mentorados. Type: List
    mentores_csv      -> Lista de dicionarios no qual as chaves sao os titulos das colunas do csv de mentores. Type: List
    cont_ativ         -> Numero da ordem de preferencia. Type: Integer

    Outputs:
    mentores_csv      -> List of lines from CSV data about column. Type: List
    alocados          -> List of lines from CSV data about column. Type: List

    """
    alocados = 0
    for row in mentorados_csv:
        for mentor in mentores_csv:
            if len(mentor["Match"]) < int(mentor["Quantidade"]) and row["Alocado"] == "Não":
                if mentor["Atividades"].find(row["Ordem de prioridade [{}]".format(cont_ativ)]) != -1:#and len(mentor["Match"]) == 0:
                    mentor["Match"] += [row["E-mail"]]
                    row["Alocado"] = "Sim"
                    alocados += 1
                    break
            else:
                pass

    return int(alocados)

def naoAlocadosmatchFunction(mentorados_csv, mentores_csv):
    """

    matchFunction Funcao que faz o match entre mentor e mentorado
    dependendo do critério de ordem de prioridade.

    Input variables:
    mentorados_csv    -> Lista de dicionarios no qual as chaves sao os titulos das colunas do csv de mentorados. Type: List
    mentores_csv      -> Lista de dicionarios no qual as chaves sao os titulos das colunas do csv de mentores. Type: List
    cont_ativ         -> Numero da ordem de preferencia. Type: Integer

    Outputs:
    mentores_csv      -> List of lines from CSV data about column. Type: List
    alocados          -> List of lines from CSV data about column. Type: List

    """
    alocados = 0
    for row in mentorados_csv:
        for mentor in mentores_csv:
            if len(mentor["Match"]) < int(mentor["Quantidade"])and row["Alocado"] == "Não":
                mentor["Match"] += [row["E-mail"]]
                row["Alocado"] = "Sim"
                alocados += 1
                break
            else:
                pass

    return int(alocados)


#PROGRAM:

import csv

with open('Mentorados 2020.csv', 'r') as mentorados:
    mentorados_csv = list(csv.DictReader(mentorados, delimiter=';'))
    for mentorado in mentorados_csv:
        mentorado["Alocado"] = "Não"

with open('Mentores 2020.csv', 'r') as mentores:
    mentores_csv = list(csv.DictReader(mentores, delimiter=';'))
    for mentor in mentores_csv:
        mentor["Match"] = []

tot_ativ = sum("Ordem de prioridade" in coluna for coluna in mentorados_csv[0])

suporta=0
for mentor in mentores_csv:
    suporta += int(mentor["Quantidade"])

#ALOCAR PESSOAS COM PREFERENCIA DE GENERO
mentoras=[]
for mentor in mentores_csv:
    if mentor["Gênero"]=="Feminino":
        mentoras.append(mentor)

suporta=0
for mentor in mentores_csv:
    suporta += int(mentor["Quantidade"])

mentoradas = []
for ment in mentorados_csv:
    if ment["Gênero"] == "Feminino" and ment["Preferência"] == "Sim":
        mentoradas.append(ment)

mentoradas.sort(key=mentoradosSemRepetir) #ordena os mentorados por ordem de um único elemento diferente presente, a pessoa só quer quem estagia por exemplo

mentoradas_match=[]
mentoradas_match.extend(mentoradas)

alocados0 = 0
for num_prioridade in range(1, tot_ativ+1):
    x = matchFunction(mentoradas, mentoras, num_prioridade)
    alocados0 += x

novoAlocados = alocados0

falta=0
for mentorada in mentoradas:
    if mentorada["Alocado"]=="Não":
        falta += 1

print("suporta(F):", suporta, "alocados(F):", novoAlocados,"falta(F):", falta)

alocados1 = naoAlocadosmatchFunction(mentoradas, mentoras)

novoAlocados += alocados1

falta=0
for mentorada in mentoradas:
    if mentorada["Alocado"]=="Não":
        falta += 1

print("suporta(F):", suporta,"alocadosNovo(F):", int(novoAlocados),"faltaNovo(F):",falta)

for ment in mentoradas:
    if ment in mentoradas_match:
        mentoradas_match.remove(ment)

for ment in mentorados_csv:
    if ment in mentoradas_match:
        mentorados_csv.remove(ment)

mentorados_csv.sort(key=mentoradosSemRepetir)
for mentor in mentores_csv:
    for mentora in mentoras:
        if mentor["E-mail"]==mentora["E-mail"]:
            mentor["Match"]=mentora["Match"]

#ALOCAR PESSOAS SEM PREFERENCIA DE GENERO
alocados2 = 0
for num_prioridade in range(1, tot_ativ+1):
    x = matchFunction(mentorados_csv, mentores_csv, num_prioridade)
    alocados2 += x

falta=0
for mentorado in mentorados_csv:
    if mentorado["Alocado"]=="Não":
        falta += 1

novoAlocados+=alocados2
print("suporta:", suporta,"alocados:", novoAlocados,"falta:",falta)

#ALOCAR PESSOAS QUE SOBRARAM
alocados3=naoAlocadosmatchFunction(mentorados_csv, mentores_csv)

falta=0
for mentorado in mentorados_csv:
    if mentorado["Alocado"]=="Não":
        falta += 1
        print(mentorado["E-mail"])

novoAlocados+=alocados3
print("suporta:", suporta,"alocadosNovo:", int(novoAlocados),"faltaNovo:",falta)

for mentor in mentores_csv:
    print(mentor["E-mail"], mentor["Match"])

#CRIANDO ARQUIVO CONTENDO SOMENTE OS MATCHS:

with open('MatchsRealizados.csv', 'w', newline='') as arquivo:
    fieldnames = ['Mentor', 'Matchs']
    writer = csv.DictWriter(arquivo, fieldnames=fieldnames)
    writer.writeheader()
    for mentor in mentores_csv:
        match = ""
        for ment in mentor["Match"]:
            match += ment+", "
        #mentormatch  = ",".join(mentor["Match"])
        #mentormatch2 = mentormatch.replace("'", "")
        writer.writerow({'Mentor': mentor["E-mail"], 'Matchs': match})
