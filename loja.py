# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py

pedidos = []                      # todos os pedidos da loja: lista solta, global


class Pedido:
    def __init__(self, numero, nome_cliente, cpf_cliente, email_cliente, rua, cidade_cliente, cep, tipo_cliente):
        self.numero = numero            # numero do pedido
        self.nome_cliente = nome_cliente    # os dados do cliente se repetem em CADA pedido dele
        self.cpf_cliente = cpf_cliente
        self.email_cliente = email_cliente
        self.rua = rua
        self.cidade_cliente = cidade_cliente
        self.cep = cep
        self.tipo_cliente = tipo_cliente          # tipo do cliente: "N" normal, "V" vip, "F" funcionario
        self.itens = []       # cada item e uma lista: [produto, qtd, preco]
        self.status = "A"         # A = aberto, P = pago, C = cancelado

    def obter_status(self):
        return self.status

    def definir_status(self, novo_status):
        self.status = novo_status


def validar_dados(email_cliente, cpf_cliente, cep):
    if len(email_cliente) > 0:
        if "@" in email_cliente:
            if len(cpf_cliente) == 11:
                if len(cep) == 8:
                    return "ok"
                else:
                    return "cep invalido"
            else:
                return "cpf invalido"
        else:
            return "email invalido"
    else:
        return "email vazio"


def criar_pedido(numero, nome_cliente, cpf_cliente, email_cliente, rua, cidade_cliente, cep, tipo_cliente):
    resultado_validacao = validar_dados(email_cliente, cpf_cliente, cep)
    if resultado_validacao != "ok":
        print("pedido", numero, "recusado:", resultado_validacao)
        return None
    else:
        pedido = Pedido(numero, nome_cliente, cpf_cliente, email_cliente, rua, cidade_cliente, cep, tipo_cliente)
        pedidos.append(pedido)
        return pedido


def adicionar_item(pedido, nome_produto, quantidade, valor_unitario):
    pedido.itens.append([nome_produto, quantidade, valor_unitario])


def calcular_total(pedido):
    valor_total = 0
    for item in pedido.itens:
        valor_total = valor_total + item[1] * item[2]
    return valor_total


def calcular_desconto(tipo_cliente, valor_total):
    if tipo_cliente == "V":
        d = valor_total * 0.10
    elif tipo_cliente == "F":
        d = valor_total * 0.20
    else:
        d = 0
    return d


def calcular_valor_a_pagar(pedido):
    return calcular_total(pedido) - calcular_desconto(pedido.tipo_cliente, calcular_total(pedido))


def pagar(pedido):
    if pedido.obter_status() == "A":
        if len(pedido.itens) > 0:
            pedido.definir_status("P")
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.obter_status() == "A":
        pedido.definir_status("C")
        return True
    else:
        return False


def descricao_status(s):
    if s == "A":
        return "aberto"
    elif s == "P":
        return "pago"
    else:
        return "cancelado"


def exibir_relatorio():
    for pedido in pedidos:
        print("Pedido", pedido.numero, "-", pedido.nome_cliente, "-", pedido.cidade_cliente)
        print("  status:", descricao_status(pedido.obter_status()))
        for item in pedido.itens:
            print("  ", item[1], "x", item[0], "= R$ %.2f" % (item[1] * item[2]))
        if len(pedido.itens) > 0:
            print("  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f" % (calcular_total(pedido), calcular_desconto(pedido.tipo_cliente, calcular_total(pedido)), calcular_valor_a_pagar(pedido)))


def calcular_arrecadado():
    valor_total = 0
    for pedido in pedidos:
        if pedido.obter_status() == "P":
            valor_total = valor_total + calcular_valor_a_pagar(pedido)
    return valor_total


def quantidade_pedidos_abertos():
    quantidade_abertos = 0
    for pedido in pedidos:
        if pedido.obter_status() == "A":
            quantidade_abertos = quantidade_abertos + 1
    return quantidade_abertos


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
primeiro_pedido = criar_pedido(1, "Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
adicionar_item(primeiro_pedido, "Caderno", 2, 15.5)
adicionar_item(primeiro_pedido, "Caneta", 5, 2.5)

criar_pedido(2, "Bruno Lima", "123", "bruno@mail.com", "Av. Central, 200", "Votorantim", "18110000", "N")

terceiro_pedido = criar_pedido(3, "Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
adicionar_item(terceiro_pedido, "Livro", 1, 89.5)

criar_pedido(4, "Carla Dias", "98765432100", "carla.mail.com", "Rua do Sol, 55", "Sorocaba", "18020000", "F")

quinto_pedido = criar_pedido(5, "Diego Rocha", "11122233344", "diego@mail.com", "Rua Nova, 7", "Itu", "13300000", "N")

sexto_pedido = criar_pedido(6, "Eva Nunes", "55566677788", "eva@mail.com", "Alameda Azul, 1", "Itu", "13300001", "F")
adicionar_item(sexto_pedido, "Fone", 1, 60.0)

criar_pedido(7, "Fabio Costa", "99988877766", "fabio@mail.com", "Rua Velha, 3", "Itu", "123", "N")

oitavo_pedido = criar_pedido(8, "Gil Alves", "44455566677", "gil@mail.com", "Rua do Meio, 9", "Sorocaba", "18030000", "N")
adicionar_item(oitavo_pedido, "Fone", 2, 60.0)

print("pagar 1:", pagar(primeiro_pedido))
print("pagar 3:", pagar(terceiro_pedido))
print("pagar 5:", pagar(quinto_pedido))
print("pagar 6:", pagar(sexto_pedido))
print("cancelar 5:", cancelar(quinto_pedido))
print("cancelar 1:", cancelar(primeiro_pedido))

exibir_relatorio()
print("arrecadado: R$ %.2f" % calcular_arrecadado())
print("abertos:", quantidade_pedidos_abertos())
