import textwrap


def menu():
    menu = """

    [d] DEPOSITAR
    [s] SACAR 
    [e] EXTRATO
    [nc] NOVA CONTA
    [lc] LISTAR CONTAS
    [nu] NOVO USUÁRIO
    [q] SAIR

    => """
    return str(input(textwrap.dedent(menu)))


def criar_usuario(usuarios):
    cpf = input("Informe o cpf (somente os números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Erro, já existe um usuário com essa informação")
        return
    
    nome = input("informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    usuarios.append({"nome": nome, 
                     "data_nascimento": data_nascimento, 
                     "cpf": cpf, 
                     "endereço": endereco})
    
    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("informe o cpf do usuário (só numeros): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("=== CONTA CRIADA COM SUCESSO! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("Erro, não foi possível criar a conta. Usuário não encontrado!")
    return None


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R${valor:.2f}\n"
        print("Operação realizada com sucesso!")
    else:
        print("Operação falhou por valor inválido!")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    
    excerdeu_saldo = valor > saldo
    excerdeu_limite = valor > limite
    excerdeu_saques = numero_saques > limite_saques

    if excerdeu_saldo:
        print("Operação falhou! Não há saldo suficiente.")
    elif excerdeu_limite:
        print("Operação falhou! O valor é maior que o limite.")
    elif excerdeu_saques:
        print("Operação falhou! não há mais saques disponíveis por hoje.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R${valor:.2f}\n"
        numero_saques += 1    
        print("Saque realizado com sucesso!")

    return saldo, extrato

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência: \t{conta['agencia']}
            C/C: \t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)    
        print(textwrap.dedent(linha))

def exibir_extrato(saldo,/,*,extrato):
    print("\n", "=" *8, " EXTRATO ", "=" *8 )
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo = R${saldo:.2f}")
    print("=" * 27)

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    LIMITE_SAQUES = 3
    AGENCIA = "0001"


    while True:

        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor de saque: "))
            
            
            saldo, extrato =  sacar(
                saldo = saldo,
                valor= valor,
                extrato= extrato,
                limite = limite,
                numero_saques= numero_saques,
                limite_saques= LIMITE_SAQUES,
            )
            


        elif opcao == "e":
            exibir_extrato(saldo, extrato= extrato)


        elif opcao == "nu":
            criar_usuario(usuarios)


        elif opcao == "nc":
            numero_conta = len(contas) + 1 
            conta = criar_conta (AGENCIA, numero_conta, usuarios)


            if conta:
                contas.append(conta) 


        elif opcao == 'lc':
            listar_contas(contas)


        elif opcao == "q":
            break


        else:
            print("Opção inválida! por favor tente novamente!")


main()