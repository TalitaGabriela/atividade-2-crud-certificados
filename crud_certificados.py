certificados = []
contador = 1

def cadastrar_certificado(cont):
    titulo = input("Entre com o título do curso: ")
    carga_horaria = int(input("Entre com a carga horária do curso:"))
    data_inicio = input("Entre com a data de início do curso:")
    data_fim = input("Entre com a data final do curso:")
    instituicao = input("Entre com a instituição do curso:")
    status = True if input("O curso foi finalizado? (Sim/Não):").lower() == "sim" else False

    certificado = {
        "id": cont,
        "titulo": titulo,
        "cargaHoraria": carga_horaria,
        "dataInicio": data_inicio,
        "dataFim": data_fim,
        "instituicao": instituicao,
        "status": status
    }

    cont += 1
    certificados.append(certificado)
    grava_certificado(certificado)
    return cont

def listar_certificados():
    if len(certificados) == 0:
        print("Não há certificados cadastrados.")
    else:
        for c in certificados:
            imprimir_certificado(c)

def busca_binaria(valorBuscado, estrutura):
    # só funciona porque os id's vão em ordem crescente (cadastro sempre incrementa)
    inicio = 0
    fim = len(estrutura) - 1

    while inicio <= fim:
        meio = int((inicio+fim)/2)
        if estrutura[meio]["id"] == valorBuscado: return meio
        if estrutura[meio]["id"] < valorBuscado: inicio = meio + 1
        else: fim = meio - 1
    return -1

def busca_por_id(id):
    posicao = busca_binaria(id, certificados)
    if posicao >= 0:
        imprimir_certificado(certificados[posicao])
    else:
        print("Certificado não encontrado!")

def imprimir_certificado(certificado):
    print("---Certificado ", certificado["id"], "---")
    print("|Título:", certificado["titulo"])
    print("|Carga Horária:", certificado["cargaHoraria"])
    print("|Data de início:", certificado["dataInicio"])
    print("|Data de finalização:", certificado["dataFim"])
    print("|Instituição:", certificado["instituicao"])
    print("|Finalizado:", "Sim" if certificado["status"] == True else "Não")
    print("--------------------")

def grava_certificado(certificado):
    arquivo = open("certificados.txt", "a")
    #arquivo.write(certificado["titulo"])

    arquivo.write(str(certificado["id"]))
    arquivo.write("\n"+str(certificado["titulo"]))
    arquivo.write("\n"+str(certificado["cargaHoraria"]))
    arquivo.write("\n"+str(certificado["dataInicio"]))
    arquivo.write("\n"+str(certificado["dataFim"]))
    arquivo.write("\n"+str(certificado["instituicao"]))
    arquivo.write("\n"+str(certificado["status"])+"\n")
    arquivo.close()

def regravar_arquivo():
    # abre com "w" só pra zerar o arquivo, depois grava tudo de novo
    arquivo = open("certificados.txt", "w")
    arquivo.close()
    for c in certificados:
        grava_certificado(c)

def carregar_dados(cont):
    # na primeira vez que rodar, o arquivo não existe ainda, aí só segue vazio
    try:
        arquivo = open("certificados.txt", "r")
    except FileNotFoundError:
        return cont

    for i in arquivo:
        certificado = {
                "id": int(i.strip()),
                "titulo": arquivo.readline().strip(),
                "cargaHoraria": int(arquivo.readline().strip()),
                "dataInicio": arquivo.readline().strip(),
                "dataFim": arquivo.readline().strip(),
                "instituicao": arquivo.readline().strip(),
                "status": arquivo.readline().strip() == "True"
        }
        certificados.append(certificado)
        cont += 1
    arquivo.close()
    return cont

def buscar_por_instituicao():
    instituicao = input("Entre com o nome da instituição:").strip().lower()
    encontrou = False
    for c in certificados:
        if c["instituicao"].lower() == instituicao:
            imprimir_certificado(c)
            encontrou = True
    if not encontrou:
        print("Nenhum certificado encontrado para essa instituição.")

def listar_concluidos():
    encontrou = False
    for c in certificados:
        if c["status"] == True:
            imprimir_certificado(c)
            encontrou = True
    if not encontrou:
        print("Não há certificados concluídos.")

def carga_horaria_total():
    total = 0
    for c in certificados:
        total += c["cargaHoraria"]
    print("Carga horária total:", total, "horas")

def alterar_situacao():
    id = int(input("Entre com o id do certificado:"))
    posicao = busca_binaria(id, certificados)
    if posicao == -1:
        print("Certificado não encontrado!")
        return

    # só inverte o valor que já está lá (true vira false e vice-versa)
    certificados[posicao]["status"] = not certificados[posicao]["status"]
    regravar_arquivo()

    situacao = "Concluído" if certificados[posicao]["status"] == True else "Não concluído"
    print("Situação alterada para:", situacao)

def buscar_por_carga_minima():
    minimo = int(input("Entre com a carga horária mínima:"))
    encontrou = False
    for c in certificados:
        if c["cargaHoraria"] >= minimo:
            imprimir_certificado(c)
            encontrou = True
    if not encontrou:
        print("Nenhum certificado com carga horária igual ou maior que", minimo, "horas.")

def maior_carga_horaria():
    if len(certificados) == 0:
        print("Não há certificados cadastrados.")
        return

    maior = certificados[0]
    for c in certificados:
        if c["cargaHoraria"] > maior["cargaHoraria"]:
            maior = c
    # se tiver mais de um com a mesma carga mais alta, só mostra o primeiro que achou
    imprimir_certificado(maior)

def menu(cont):
    cont = carregar_dados(cont)
    while True:
        print("------Gerenciador de Certificados------")
        print("| 1 - Cadastrar certificado           |")
        print("| 2 - Listar certificados             |")
        print("| 3 - Buscar certificado por id       |")
        print("| 4 - Buscar por instituição          |")
        print("| 5 - Listar certificados concluídos  |")
        print("| 6 - Carga horária total             |")
        print("| 7 - Alterar situação do certificado |")
        print("| 8 - Buscar por carga horária mínima |")
        print("| 9 - Maior carga horária             |")
        print("| 0 - Sair                            |")
        print("_______________________________________")
        opcao = int(input(">>"))
        match opcao:
            case 1:
                print("---Cadastro de Certificado---")
                cont = cadastrar_certificado(cont)
                print("Cadastro efetuado com sucesso!")
                print("---------------------------")
            case 2:
                print("---Lista de Certificados---")
                listar_certificados()
                print("---------------------------")
            case 3:
                print("---Buscando certificado por id---")
                buscado = int(input("Entre com o id do certificado:"))
                busca_por_id(buscado)
                print("---------------------------")
            case 4:
                print("---Buscando certificados por instituição---")
                buscar_por_instituicao()
                print("---------------------------")
            case 5:
                print("---Certificados Concluídos---")
                listar_concluidos()
                print("---------------------------")
            case 6:
                print("---Carga Horária Total---")
                carga_horaria_total()
                print("---------------------------")
            case 7:
                print("---Alterar Situação do Certificado---")
                alterar_situacao()
                print("---------------------------")
            case 8:
                print("---Buscando por carga horária mínima---")
                buscar_por_carga_minima()
                print("---------------------------")
            case 9:
                print("---Certificado com Maior Carga Horária---")
                maior_carga_horaria()
                print("---------------------------")
            case 0:
                print("Saindo da aplicação...")
                break
            case _:
                print("Opção inválida!")

menu(contador)