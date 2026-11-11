# Etapa 4: criação de tipos específicos para os dados da loja.


class Cpf:
    # Representa um CPF e valida seu tamanho.
    def __init__(self, valor):
        if len(valor) != 11:
            raise ValueError("cpf invalido")
        self.valor = valor

    def __str__(self):
        return self.valor


class Email:
    # Representa um email e valida seu conteúdo básico.
    def __init__(self, valor):
        if not valor:
            raise ValueError("email vazio")
        if "@" not in valor:
            raise ValueError("email invalido")
        self.valor = valor

    def __str__(self):
        return self.valor


class Cep:
    # Representa um CEP com oito caracteres.
    def __init__(self, valor):
        if len(valor) != 8:
            raise ValueError("cep invalido")
        self.valor = valor

    def __str__(self):
        return self.valor


class Dinheiro:
    # Armazena dinheiro em centavos inteiros.
    def __init__(self, centavos):
        self.centavos = int(centavos)

    def somar(self, outro):
        return Dinheiro(self.centavos + outro.centavos)

    def subtrair(self, outro):
        return Dinheiro(self.centavos - outro.centavos)

    def multiplicar(self, quantidade):
        return Dinheiro(self.centavos * quantidade)

    def percentual(self, porcentagem):
        centavos = (self.centavos * porcentagem + 50) // 100
        return Dinheiro(centavos)

    def __str__(self):
        reais = self.centavos // 100
        centavos = self.centavos % 100
        return f"R$ {reais}.{centavos:02d}"


class Status:
    # Representa o estado de um pedido.
    def __init__(self, codigo):
        if codigo not in ("A", "P", "C"):
            raise ValueError("status invalido")
        self.codigo = codigo

    def descricao(self):
        return {
            "A": "aberto",
            "P": "pago",
            "C": "cancelado"
        }[self.codigo]

    def esta_aberto(self):
        return self.codigo == "A"

    def pagar(self):
        self.codigo = "P"

    def cancelar(self):
        self.codigo = "C"


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
        return self.produto.preco.multiplicar(self.quantidade)


class Pedido:
    # Reúne o número, o cliente, os itens e o status do pedido.
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.itens = []
        self.status = Status("A")

    def obter_status(self):
        return self.status.codigo

    def definir_status(self, novo_status):
        self.status.codigo = novo_status


pedidos = []


def validar_dados(email, cpf, cep):
    try:
        Email(email)
        Cpf(cpf)
        Cep(cep)
        return "ok"
    except ValueError as erro:
        return str(erro)


def criar_cliente(nome, cpf, email, rua, cidade, cep, tipo):
    return Cliente(
        nome, Cpf(cpf), Email(email), rua, cidade, Cep(cep), tipo
    )


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
    valor_total = Dinheiro(0)
    for item in pedido.itens:
        valor_total = valor_total.somar(item.calcular_total())
    return valor_total


def calcular_desconto(tipo, valor_total):
    if tipo == "V":
        return valor_total.percentual(10)
    if tipo == "F":
        return valor_total.percentual(20)
    return valor_total.percentual(0)


def calcular_valor_a_pagar(pedido):
    total = calcular_total(pedido)
    desconto = calcular_desconto(pedido.cliente.tipo, total)
    return total.subtrair(desconto)


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
    return Status(status).descricao()


def exibir_relatorio():
    for pedido in pedidos:
        cliente = pedido.cliente
        print("Pedido", pedido.numero, "-", cliente.nome, "-", cliente.cidade)
        print("  status:", pedido.status.descricao())

        for item in pedido.itens:
            print(
                "  ",
                item.quantidade,
                "x",
                item.produto.nome,
                "= %s" % item.calcular_total()
            )

        if len(pedido.itens) > 0:
            total = calcular_total(pedido)
            desconto = calcular_desconto(cliente.tipo, total)
            valor_a_pagar = calcular_valor_a_pagar(pedido)
            print(
                "  total: %s | desconto: %s | a pagar: %s"
                % (total, desconto, valor_a_pagar)
            )


def calcular_arrecadado():
    valor_total = Dinheiro(0)
    for pedido in pedidos:
        if pedido.obter_status() == "P":
            valor_total = valor_total.somar(calcular_valor_a_pagar(pedido))
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
caderno = Produto("Caderno", Dinheiro(1550))
caneta = Produto("Caneta", Dinheiro(250))
livro = Produto("Livro", Dinheiro(8950))
fone = Produto("Fone", Dinheiro(6000))

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
print("arrecadado:", calcular_arrecadado())
print("abertos:", quantidade_pedidos_abertos())
