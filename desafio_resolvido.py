import sqlite3
# Banco como exemplo....
# Cria (ou abre) o banco de dados no arquivo 'Banco.db'
conn = sqlite3.connect('Banco.db')
cursor = conn.cursor()

# Criação da tabela Login
cursor.execute('''
CREATE TABLE IF NOT EXISTS Agencia (
    agencia INTEGER NOT NULL,
    PRIMARY KEY (agencia)    
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Conta (
    conta INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    agencia INTEGER NOT NULL,
    FOREIGN KEY (agencia) REFERENCES Agencia(agencia)
)
''')

# Criação da tabela Cliente
cursor.execute('''
CREATE TABLE IF NOT EXISTS Cliente (
    CPF TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    sobre_nome TEXT NOT NULL,
    agencia INTEGER NOT NULL,
    conta INTEGER NOT NULL,
    PRIMARY KEY (CPF),
    FOREIGN KEY (agencia) REFERENCES Agencia(agencia),
    FOREIGN KEY (conta) REFERENCES Conta(conta)
)
''')

# Criação da tabela Financiamento
cursor.execute('''
CREATE TABLE IF NOT EXISTS Financiamento (
    Financiamento INTEGER NOT NULL UNIQUE,
    CPF TEXT NOT NULL,
    agencia INTEGER NOT NULL,
    FOREIGN KEY (CPF) REFERENCES Cliente(CPF),
    FOREIGN KEY (agencia) REFERENCES Agencia(agencia)
)
''')

# Dados de 1 cliente comum
beta_cliente = ('789754679', 'Jango', 'Globo', 3, 36)

# Comando INSERT INTO
cursor.execute('''
    INSERT INTO Cliente (CPF, nome, sobre_nome, agencia, conta)
    VALUES (?, ?, ?, ?, ?)
''', beta_cliente)

# Salvando e fechando

conn.commit()
conn.close()

agencia = int(input("Informe sua agencia: "))
conta = int(input("Informe sua conta: "))
print("Agência:", agencia, "| Conta:", conta)

if agencia == 1 and conta == 1:
    print("Bem vindo Administrador:")
    while True:
        menu_admin = """
              [N]Novo Cliente
              [A]Alterar Cliente
              [E]Exibir Clientes
              [Nv.Ag]Nova Agencia
              [M]Metas
              [q]Sair 
        => """
        opcao = input(menu_admin)
        if opcao == "N" or opcao == "n":
            print("Cadastra Novo cliente")
            cpf_novo_cadastro = int(9)
            agencia_novo_cadastro = int(input("\n Escolha a Agencia: "))
            cpf_novo_cadastro = int(input("\n Informe o CPF para ser cadastrado: ")) 
            nome_novo_cad = str(input("\n Informe nome para ser cadastrado: ")) 
            sobre_nome_cad = str(input("\n Informe o sobrenome para ser cadastrado: "))
            nova_conta = conta + 1

            novo_cliente = (cpf_novo_cadastro, nome_novo_cad, sobre_nome_cad, agencia_novo_cadastro, nova_conta)

            # Conecta ao banco
            conn = sqlite3.connect('Banco.db')
            cursor = conn.cursor()
            # Executa o INSERT
            cursor.execute('''
            INSERT INTO Cliente (CPF, nome, sobre_nome, agencia, conta)
            VALUES (?, ?, ?, ?, ?)
            ''', novo_cliente)

            conn.commit()
            conn.close()

        elif opcao == "A" or opcao == "A":
            print("Altera Cadastro de Cliente")
        elif opcao == "E" or opcao == "e":
            print("Carregando exibicao:")
            conn = sqlite3.connect('Banco.db')
            cursor = conn.cursor()
            # Executa o select
            cursor.execute("SELECT * FROM Cliente")
            # Faz a consulta
            consulta_clientes = cursor.fetchall()
            # Exibe os dados
            for cliente in consulta_clientes:
                print("CPF:", cliente[0])
                print("Nome:", cliente[1])
                print("Sobrenome:", cliente[2])
                print("Agência:", cliente[3])
                print("Conta:", cliente[4])
                print("---")

            conn.commit()
            conn.close()
        elif opcao == "Nv.Ag" or opcao == "nv.ag":
            print("Cadastra Nova Agencia")
        elif opcao == "M" or opcao == "m":
            print("Exibe as metas")
        elif opcao == "q" or opcao == "Q":
            print("Saindo")
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
elif agencia > 0 and conta > 1:
    extrato = ""
    saldo = float()
    limite = 500
    taxa_juros = 15
    score = 900
    numero_saques = 0
    salario = float()
    LIMITE_SAQUES = 3
    LIMITE_EM_MESES = 72
    while True:    
        print("Aguarde estamos verificando sua conta!")
        print("Aguarde carregando....")
        #Exemplo tosco de conexão com o banco
        conn = sqlite3.connect('Banco.db')
        cursor = conn.cursor()
        #Consulta com placeholder exemplo tosco
        cursor.execute("SELECT * FROM Agencia where agencia = ?", (agencia,))
        encontrado = cursor.fetchone()
    
        #if encontrado is not None:
        print("Bem vindo ao Banco Santander, Internet Banking versão 2005")
    
        if conn is not None:
            menu = """
                [d] Depositar
                [s] Sacar
                [c] Credito 
                [e] Extrato
                [q] Sair
               => """
            opcao = input(menu)
            if opcao == "d":
                valor = float(input("Informe o valor do depósito: \n"))
                if valor > 0:
                    saldo += valor
                    extrato += f"Depósito: R$ {valor:.2f}\n"
                    print(f"\t Depósito realizado no valor de: R$ {valor:.2f}\n")
                else:
                    print("\t Operação falhou! O valor informado é inválido.\n")
            elif opcao == "s":
                valor = float(input("Informe o valor do saque: \n"))
                excedeu_saldo = valor > saldo
                excedeu_limite = valor > limite
                excedeu_saques = numero_saques >= LIMITE_SAQUES
                if excedeu_saldo:
                    print("Operação falhou! Você não tem saldo suficiente.")
                elif excedeu_limite:
                    print("Operação falhou! O valor do saque excede o limite.")
                elif excedeu_saques:
                    print("Operação falhou! Número máximo de saques excedido.")
                elif valor > 0:
                    saldo -= valor
                    extrato += f"Saque: R$ {valor:.2f}\n"
                    print(f"\t Saque realizado no valor de: R$ {valor:.2f}\n")
                    numero_saques += 1
                else:
                    print("Operação falhou! O valor informado é inválido.")
            elif opcao == "c":
                salario = float(input(f"Informe o seu salario: "))
                MARGEM_FINANCIAMENTO = (salario * 60) * 0.30 
                if salario >= 1545:
                    print("Analisando perfil, por favor aguarde.....")
                    score = 900
                    if saldo >= 500:
                        if numero_saques == 0:
                            calculadora_perfil = score * LIMITE_SAQUES
                            if calculadora_perfil >= 2700:
                                MARGEM_FINANCIAMENTO_CLIENTE = MARGEM_FINANCIAMENTO
                                print(f"Sua Margem é:{MARGEM_FINANCIAMENTO_CLIENTE}")
                                menu= """
                                    [S] Simular
                                    [P] Parar
                                => """
                                opcao = input(menu)
                                if opcao == "S":
                                    print(f"A taxa de juros selic anual é:\n{taxa_juros}")
                                    valor_em = float(input("Informe o valor do empréstimo: "))
                                    prazo_pagamento = float(input("Informe em quantos meses deseja pagar (limite 72): "))
                                    if valor_em > 0 and valor_em <= MARGEM_FINANCIAMENTO_CLIENTE and prazo_pagamento <= LIMITE_EM_MESES:
                                        valor_parcelas = (valor_em * ((((prazo_pagamento / 12) * taxa_juros) / 100) + 1)) / prazo_pagamento
                                        VALOR_COMPROMETIDO_SALARIO = salario / 2
                                        if valor_parcelas <= VALOR_COMPROMETIDO_SALARIO:
                                            valor_parcelas_cliente = valor_parcelas
                                            print(f"O emprestimo de: {valor_em} foi aprovado, com {prazo_pagamento} parcelas de R$ {valor_parcelas_cliente}")
                                            if valor_em > 0 and prazo_pagamento > 0 and valor_parcelas_cliente > 0:
                                                menu = """
                                                    [C] Confirmar emprestimo!
                                                    [D] Deixar para depois!
                                                    => """ 
                                                opcao = input(menu)
                                                if opcao == "C":
                                                    print(f"Voce fez o emprestimo de R$ {valor_em} as parcelas de R$ {valor_parcelas_cliente} seram automaticamente recolhidas mes a mes somente aguardar o deposito do valor {valor_em}")
                                                elif opcao == "D":
                                                    print(f"Certo deixar para depois!")
                                                    break
                                            else: 
                                                print("Ocorreu um erro inesperado tente novamente!")                                               
                                        elif valor_parcelas > VALOR_COMPROMETIDO_SALARIO:
                                            adequando_parcelas = (valor_parcelas / VALOR_COMPROMETIDO_SALARIO)
                                            prazo_pagamento_adequacao = (prazo_pagamento * adequando_parcelas)
                                            if prazo_pagamento_adequacao <= LIMITE_EM_MESES:
                                                valor_parcelas = (valor_em * ((((prazo_pagamento_adequacao / 12) * taxa_juros) / 100) + 1)) / prazo_pagamento_adequacao
                                                print(f"O emprestimo de: {valor_em} foi aprovado, com {prazo_pagamento_adequacao} com parcelas de R$ {valor_parcelas}")
                                                if valor_em > 0 and prazo_pagamento > 0 and valor_parcelas_cliente > 0:
                                                    menu = """
                                                    [C] Confirmar emprestimo!
                                                    [D] Deixar para depois!
                                                    => """ 
                                                opcao = input(menu)
                                                if opcao == "C":
                                                    print(f"Voce fez o emprestimo de R$ {valor_em} as parcelas de R$ {valor_parcelas_cliente} seram automaticamente recolhidas mes a mes somente aguardar o deposito do valor {valor_em}")
                                                elif opcao == "D":
                                                    print(f"Certo deixar para depois!")
                                                    break
                                                else: 
                                                    print("Ocorreu um erro inesperado tente novamente!") 
                                                    break  
                                            elif prazo_pagamento_adequacao > LIMITE_EM_MESES:
                                                print("Infelizmente não foi possível emprestimo nestas condições por favor verificar o valor de cada parcela, não pode ultrapassar metade do seu salário;")
                                        else:
                                            print("Não sabemos o que ocorreu, por favor tente novamente!")      
                                    else:
                                        print("Você deve informar um valor para o empréstimo")
                                elif opcao == "P":
                                    print("Voce escolheu sair, saindo do aplicativo!")
                                    break
                                else:
                                    print("Voce deve escolher um opcao")
                                    break
                                            
                            elif calculadora_perfil >= 1350:
                                MARGEM_FINANCIAMENTO_CLIENTE = MARGEM_FINANCIAMENTO * 0.75
                                print(f"Sua Margem é:{MARGEM_FINANCIAMENTO_CLIENTE}")
                                menu= """
                                    [S] Simular
                                    [P] Parar
                                => """
                                opcao = input(menu)
                                if opcao == "S":
                                    print(f"A taxa de juros selic anual é:\n{taxa_juros}")
                                    valor_em = float(input("Informe o valor do empréstimo: "))
                                    prazo_pagamento = float(input("Informe em quantos meses deseja pagar: "))
                                    if valor_em > 0 and valor_em <= MARGEM_FINANCIAMENTO_CLIENTE and prazo_pagamento <= LIMITE_EM_MESES:
                                        valor_parcelas = (valor_em * ((((prazo_pagamento / 12) * taxa_juros) / 100) + 1)) / prazo_pagamento
                                        VALOR_COMPROMETIDO_SALARIO = salario / 2
                                        if valor_parcelas <= VALOR_COMPROMETIDO_SALARIO:
                                            valor_parcelas_cliente = valor_parcelas
                                            print(f"O emprestimo de: {valor_em} foi aprovado, com {prazo_pagamento} parcelas de R$ {valor_parcelas_cliente}")
                                            if valor_em > 0 and prazo_pagamento > 0 and valor_parcelas_cliente > 0:
                                                menu = """
                                                    [C] Confirmar emprestimo!
                                                    [D] Deixar para depois!
                                                    => """ 
                                                opcao = input(menu)
                                                if opcao == "C":
                                                    print(f"Voce fez o emprestimo de R$ {valor_em} as parcelas de R$ {valor_parcelas_cliente} seram automaticamente recolhidas mes a mes somente aguardar o deposito do valor {valor_em}")
                                                elif opcao == "D":
                                                    print(f"Certo deixar para depois!")
                                                    break
                                            else: 
                                                print("Ocorreu um erro inesperado tente novamente!")   
                                        elif valor_parcelas > VALOR_COMPROMETIDO_SALARIO:
                                            adequando_parcelas = (valor_parcelas / VALOR_COMPROMETIDO_SALARIO)
                                            prazo_pagamento_adequacao = (prazo_pagamento * adequando_parcelas)
                                            if prazo_pagamento_adequacao <= LIMITE_EM_MESES:
                                                valor_parcelas = (valor_em * ((((prazo_pagamento_adequacao / 12) * taxa_juros) / 100) + 1)) / prazo_pagamento_adequacao
                                                print(f"O emprestimo de: {valor_em} foi aprovado, com {prazo_pagamento_adequacao} com parcelas de R$ {valor_parcelas}")
                                                if valor_em > 0 and prazo_pagamento > 0 and valor_parcelas_cliente > 0:
                                                    menu = """
                                                    [C] Confirmar emprestimo!
                                                    [D] Deixar para depois!
                                                    => """ 
                                                    opcao = input(menu)
                                                    if opcao == "C":
                                                       print(f"Voce fez o emprestimo de R$ {valor_em} as parcelas de R$ {valor_parcelas_cliente} seram automaticamente recolhidas mes a mes somente aguardar o deposito do valor {valor_em}")
                                                    elif opcao == "D":
                                                       print(f"Certo deixar para depois!")
                                                       break
                                                    else:
                                                        print("Voce deve escolher uma opcao")
                                                        break
                                                else: 
                                                    print("Ocorreu um erro inesperado tente novamente!") 
                                            elif prazo_pagamento_adequacao > LIMITE_EM_MESES:
                                                print("Infelizmente não foi possível emprestimo nestas condições por favor verificar o valor de cada parcela, não pode ultrapassar metade do seu salário;")
                                        else:
                                            print("Não sabemos o que ocorreu, por favor tente novamente!")      
                                    else:
                                        print("Você deve informar um valor para o empréstimo")
                                if opcao == "P":
                                    print("Voce escolheu sair, saindo do aplicativo!")
                                break
    
                            elif calculadora_perfil < 1350:
                                print(f"Infelizmente você não tem margem")
                        elif numero_saques >1:    
                            calculadora_perfil = (score / numero_saques) * LIMITE_SAQUES
                            if calculadora_perfil >= 2700:
                                MARGEM_FINANCIAMENTO_CLIENTE = (1.25 * MARGEM_FINANCIAMENTO)
                                print(f"Sua Margem é:{MARGEM_FINANCIAMENTO_CLIENTE}")
                                menu= """
                                    [S] Simular
                                    [P] Parar
                                => """
                                opcao = input(menu)
                                if opcao == "S":
                                    print(f"A taxa de juros selic anual é:\n{taxa_juros}")
                                            
                                    valor_em = float(input("Informe o valor do empréstimo: "))
                                    prazo_pagamento = float(input("Informe em quantos meses deseja pagar: "))
                                    if valor_em > 0 and valor_em <= MARGEM_FINANCIAMENTO_CLIENTE and prazo_pagamento <= LIMITE_EM_MESES:
                                        valor_parcelas = (valor_em * ((((prazo_pagamento / 12) * taxa_juros) / 100) + 1)) / prazo_pagamento
                                        VALOR_COMPROMETIDO_SALARIO = salario / 2
                                        if valor_parcelas <= VALOR_COMPROMETIDO_SALARIO:
                                            valor_parcelas_cliente = valor_parcelas
                                            print(f"O emprestimo de: {valor_em} foi aprovado, com {prazo_pagamento} parcelas de R$ {valor_parcelas_cliente}")
                                            if valor_em > 0 and prazo_pagamento > 0 and valor_parcelas_cliente > 0:
                                                menu = """
                                                [C] Confirmar emprestimo!
                                                [D] Deixar para depois!
                                                => """ 
                                                opcao = input(menu)
                                                if opcao == "C":
                                                    print(f"Voce fez o emprestimo de R$ {valor_em} as parcelas de R$ {valor_parcelas_cliente} seram automaticamente recolhidas mes a mes somente aguardar o deposito do valor {valor_em}")
                                                elif opcao == "D":
                                                    print(f"Certo deixar para depois!")
                                                    break
                                                else:
                                                        print("Voce deve escolher uma opcao")
                                                        break 
                                            else: 
                                                print("Ocorreu um erro inesperado tente novamente!")                                              
                                        elif valor_parcelas > VALOR_COMPROMETIDO_SALARIO:
                                            adequando_parcelas = (valor_parcelas / VALOR_COMPROMETIDO_SALARIO)
                                            prazo_pagamento_adequacao = (prazo_pagamento * adequando_parcelas)
                                            if prazo_pagamento_adequacao <= LIMITE_EM_MESES:
                                                valor_parcelas = (valor_em * ((((prazo_pagamento_adequacao / 12) * taxa_juros) / 100) + 1)) / prazo_pagamento_adequacao
                                                print(f"O emprestimo de: {valor_em} foi aprovado, com {prazo_pagamento_adequacao} com parcelas de R$ {valor_parcelas}")
                                                if valor_em > 0 and prazo_pagamento > 0 and valor_parcelas_cliente > 0:
                                                    menu = """
                                                    [C] Confirmar emprestimo!
                                                    [D] Deixar para depois!
                                                    => """ 
                                                    opcao = input(menu)
                                                    if opcao == "C":
                                                        print(f"Voce fez o emprestimo de R$ {valor_em} as parcelas de R$ {valor_parcelas_cliente} seram automaticamente recolhidas mes a mes somente aguardar o deposito do valor {valor_em}")
                                                    elif opcao == "D":
                                                        print(f"Certo deixar para depois!")
                                                        break
                                                    else:
                                                        print("Voce deve escolher uma opcao")
                                                        break 
                                                else: 
                                                    print("Ocorreu um erro inesperado tente novamente!") 
                                            elif prazo_pagamento_adequacao > LIMITE_EM_MESES:
                                                print("Infelizmente não foi possível emprestimo nestas condições por favor verificar o valor de cada parcela, não pode ultrapassar metade do seu salário;")
                                        else:
                                            print("Não sabemos o que ocorreu, por favor tente novamente!")      
                                    else:
                                        print("Você deve informar um valor para o empréstimo")
                                elif opcao == "P":
                                    print("Voce escolheu sair, saindo do aplicativo!")
                                    break
                                else:
                                    print("Voce deve escolher um opcao")
                                    break
                                            
                            elif calculadora_perfil >= 1350:
                                MARGEM_FINANCIAMENTO_CLIENTE = MARGEM_FINANCIAMENTO * 0.75
                                print(f"Sua Margem é:{MARGEM_FINANCIAMENTO_CLIENTE}")
                                menu= """
                                    [S] Simular
                                    [P] Parar
                                => """
                                opcao = input(menu)
                                if opcao == "S":
                                    print(f"A taxa de juros selic anual é:\n{taxa_juros}")
                                    valor_em = float(input("Informe o valor do empréstimo: "))
                                    prazo_pagamento = float(input("Informe em quantos meses deseja pagar: "))
                                    if valor_em > 0 and valor_em <= MARGEM_FINANCIAMENTO_CLIENTE and prazo_pagamento <= LIMITE_EM_MESES:
                                        valor_parcelas = (valor_em * ((((prazo_pagamento / 12) * taxa_juros) / 100) + 1)) / prazo_pagamento
                                        VALOR_COMPROMETIDO_SALARIO = salario / 2
                                        if valor_parcelas <= VALOR_COMPROMETIDO_SALARIO:
                                            valor_parcelas_cliente = valor_parcelas
                                            print(f"O emprestimo de: {valor_em} foi aprovado, com {prazo_pagamento} parcelas de R$ {valor_parcelas_cliente}")
                                            if valor_em > 0 and prazo_pagamento > 0 and valor_parcelas_cliente > 0:
                                                menu = """
                                                [C] Confirmar emprestimo!
                                                [D] Deixar para depois!
                                                => """ 
                                                opcao = input(menu)
                                                if opcao == "C":
                                                    print(f"Voce fez o emprestimo de R$ {valor_em} as parcelas de R$ {valor_parcelas_cliente} seram automaticamente recolhidas mes a mes somente aguardar o deposito do valor {valor_em}")
                                                elif opcao == "D":
                                                    print(f"Certo deixar para depois!")
                                                    break
                                                else:
                                                    print("Voce deve escolher uma opcao")
                                                    break 
                                            else: 
                                                print("Ocorreu um erro inesperado tente novamente!")
                                        elif valor_parcelas > VALOR_COMPROMETIDO_SALARIO:
                                            adequando_parcelas = (valor_parcelas / VALOR_COMPROMETIDO_SALARIO)
                                            prazo_pagamento_adequacao = (prazo_pagamento * adequando_parcelas)
                                            if prazo_pagamento_adequacao <= LIMITE_EM_MESES:
                                                valor_parcelas = (valor_em * ((((prazo_pagamento_adequacao / 12) * taxa_juros) / 100) + 1)) / prazo_pagamento_adequacao
                                                print(f"O emprestimo de: {valor_em} foi aprovado, com {prazo_pagamento_adequacao} com parcelas de R$ {valor_parcelas}")
                                                if valor_em > 0 and prazo_pagamento > 0 and valor_parcelas_cliente > 0:
                                                    menu = """
                                                    [C] Confirmar emprestimo!
                                                    [D] Deixar para depois!
                                                    => """ 
                                                    opcao = input(menu)
                                                    if opcao == "C":
                                                        print(f"Voce fez o emprestimo de R$ {valor_em} as parcelas de R$ {valor_parcelas_cliente} seram automaticamente recolhidas mes a mes somente aguardar o deposito do valor {valor_em}")
                                                    elif opcao == "D":
                                                        print(f"Certo deixar para depois!")
                                                        break
                                                    else:
                                                        print("Voce deve escolher uma opcao")
                                                        break 
                                                else: 
                                                    print("Ocorreu um erro inesperado tente novamente!")
                                            elif prazo_pagamento_adequacao > LIMITE_EM_MESES:
                                                print("Infelizmente não foi possível emprestimo nestas condições por favor verificar o valor de cada parcela, não pode ultrapassar metade do seu salário;")
                                        else:
                                            print("Não sabemos o que ocorreu, por favor tente novamente!")      
                                    else:
                                        print("Você deve informar um valor para o empréstimo")
                                if opcao == "P":
                                    print("Voce escolheu sair, saindo do aplicativo!")
                                break
                            elif calculadora_perfil < 1350:
                                print(f"Infelizmente você não tem margem")
                        else:
                            print(f"Algo inesperado aconteceu! Tente Novamente!")
                    else:
                        print("Voce não tem score!")
                else:
                    print("Você não tem margem alguma, precisa comprovar renda!")
    
            elif opcao == "e":
                print("\n================ EXTRATO ================")
                print("Não foram realizadas movimentações." if not extrato else extrato)
                print(f"\nSaldo: R$ {saldo:.2f}")
                print("==========================================")
    
            elif opcao == "q":
                break
    
            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")
    
        else:
            print("Esta conta não existe!")   
else:
    print("Agencia não cadastrada!")