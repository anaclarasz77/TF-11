# Etapa 3: normalização de clientes, produtos e itens do pedido.


class Cliente:
    # Reúne os dados de cadastro de um cliente.
    def __init__(self, nome, cpf, email, rua, cidade, cep, tipo):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.tipo = tipo


class Produto:
    # Representa um produto e seu preço unitário.
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


class ItemDoPedido:
    # Associa um produto à quantidade comprada.
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def calcular_total(self):
        return self.quantidade * self.produto.preco


class Pedido:
    # Reúne o número, o cliente, os itens e o status do pedido.
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.itens = []
        self.status = "A"

    def obter_status(self):
        return self.status

    def definir_status(self, novo_status):
        self.status = novo_status


pedidos = []


def validar_dados(email, cpf, cep):
    if len(email) > 0:
        if "@" in email:
            if len(cpf) == 11:
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


def criar_cliente(nome, cpf, email, rua, cidade, cep, tipo):
    return Cliente(nome, cpf, email, rua, cidade, cep, tipo)


def criar_pedido(numero, cliente):
    pedido = Pedido(numero, cliente)
    pedidos.append(pedido)
    return pedido


def recusar_pedido(numero, nome, cpf, email, rua, cidade, cep, tipo):
    resultado = validar_dados(email, cpf, cep)
    if resultado != "ok":
        print("pedido", numero, "recusado:", resultado)


def adicionar_item(pedido, produto, quantidade):
    pedido.itens.append(ItemDoPedido(produto, quantidade))


def calcular_total(pedido):
    valor_total = 0
    for item in pedido.itens:
        valor_total = valor_total + item.calcular_total()
    return valor_total


def calcular_desconto(tipo, valor_total):
    if tipo == "V":
        desconto = valor_total * 0.10
    elif tipo == "F":
        desconto = valor_total * 0.20
    else:
        desconto = 0
    return desconto


def calcular_valor_a_pagar(pedido):
    total = calcular_total(pedido)
    return total - calcular_desconto(pedido.cliente.tipo, total)


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


def descricao_status(status):
    if status == "A":
        return "aberto"
    elif status == "P":
        return "pago"
    else:
        return "cancelado"


def exibir_relatorio():
    for pedido in pedidos:
        cliente = pedido.cliente
        print("Pedido", pedido.numero, "-", cliente.nome, "-", cliente.cidade)
        print("  status:", descricao_status(pedido.obter_status()))

        for item in pedido.itens:
            print(
                "  ",
                item.quantidade,
                "x",
                item.produto.nome,
                "= R$ %.2f" % item.calcular_total()
            )

        if len(pedido.itens) > 0:
            total = calcular_total(pedido)
            desconto = calcular_desconto(cliente.tipo, total)
            valor_a_pagar = calcular_valor_a_pagar(pedido)
            print(
                "  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f"
                % (total, desconto, valor_a_pagar)
            )


def calcular_arrecadado():
    valor_total = 0
    for pedido in pedidos:
        if pedido.obter_status() == "P":
            valor_total = valor_total + calcular_valor_a_pagar(pedido)
    return valor_total


def quantidade_pedidos_abertos():
    quantidade = 0
    for pedido in pedidos:
        if pedido.obter_status() == "A":
            quantidade = quantidade + 1
    return quantidade


# Cadastro dos clientes.
ana = criar_cliente(
    "Ana Souza", "12345678901", "ana@mail.com",
    "Rua das Flores, 10", "Sorocaba", "18010000", "V"
)
diego = criar_cliente(
    "Diego Rocha", "11122233344", "diego@mail.com",
    "Rua Nova, 7", "Itu", "13300000", "N"
)
eva = criar_cliente(
    "Eva Nunes", "55566677788", "eva@mail.com",
    "Alameda Azul, 1", "Itu", "13300001", "F"
)
gil = criar_cliente(
    "Gil Alves", "44455566677", "gil@mail.com",
    "Rua do Meio, 9", "Sorocaba", "18030000", "N"
)

# Cadastro dos produtos.
caderno = Produto("Caderno", 15.5)
caneta = Produto("Caneta", 2.5)
livro = Produto("Livro", 89.5)
fone = Produto("Fone", 60.0)

# Criação dos pedidos.
primeiro_pedido = criar_pedido(1, ana)
adicionar_item(primeiro_pedido, caderno, 2)
adicionar_item(primeiro_pedido, caneta, 5)

recusar_pedido(
    2, "Bruno Lima", "123", "bruno@mail.com",
    "Av. Central, 200", "Votorantim", "18110000", "N"
)

terceiro_pedido = criar_pedido(3, ana)
adicionar_item(terceiro_pedido, livro, 1)

recusar_pedido(
    4, "Carla Dias", "98765432100", "carla.mail.com",
    "Rua do Sol, 55", "Sorocaba", "18020000", "F"
)

quinto_pedido = criar_pedido(5, diego)

sexto_pedido = criar_pedido(6, eva)
adicionar_item(sexto_pedido, fone, 1)

recusar_pedido(
    7, "Fabio Costa", "99988877766", "fabio@mail.com",
    "Rua Velha, 3", "Itu", "123", "N"
)

oitavo_pedido = criar_pedido(8, gil)
adicionar_item(oitavo_pedido, fone, 2)

# Operações da loja.
print("pagar 1:", pagar(primeiro_pedido))
print("pagar 3:", pagar(terceiro_pedido))
print("pagar 5:", pagar(quinto_pedido))
print("pagar 6:", pagar(sexto_pedido))
print("cancelar 5:", cancelar(quinto_pedido))
print("cancelar 1:", cancelar(primeiro_pedido))

exibir_relatorio()
print("arrecadado: R$ %.2f" % calcular_arrecadado())
print("abertos:", quantidade_pedidos_abertos())
