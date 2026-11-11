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


class ItensDoPedido:
    # Administra os itens de um pedido sem expor sua lista interna.
    def __init__(self):
        self._itens = []

    def adicionar(self, produto, quantidade):
        self._itens.append(ItemDoPedido(produto, quantidade))

    def calcular_total(self):
        total = Dinheiro(0)
        for item in self._itens:
            total = total.somar(item.calcular_total())
        return total

    def tem_itens(self):
        return len(self._itens) > 0

    def imprimir(self):
        for item in self._itens:
            print(
                "  ",
                item.quantidade,
                "x",
                item.produto.nome,
                "= %s" % item.calcular_total()
            )


class Pedido:
    # Reúne o cliente, os itens e o status, sem guardar seu número.
    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = ItensDoPedido()
        self.status = Status("A")

    def obter_status(self):
        return self.status.codigo

    def definir_status(self, novo_status):
        self.status.codigo = novo_status


class Pedidos:
    # Administra os pedidos identificados por seus números.
    def __init__(self):
        self._pedidos = {}

    def adicionar(self, numero, pedido):
        self._pedidos[numero] = pedido

    def obter(self, numero):
        return self._pedidos[numero]

    def pagar(self, numero):
        return pagar(self.obter(numero))

    def cancelar(self, numero):
        return cancelar(self.obter(numero))

    def imprimir_relatorio(self):
        for numero, pedido in self._pedidos.items():
            cliente = pedido.cliente
            print("Pedido", numero, "-", cliente.nome, "-", cliente.cidade)
            print("  status:", pedido.status.descricao())
            pedido.itens.imprimir()

            if pedido.itens.tem_itens():
                total = pedido.itens.calcular_total()
                desconto = calcular_desconto(cliente.tipo, total)
                valor_a_pagar = total.subtrair(desconto)
                print(
                    "  total: %s | desconto: %s | a pagar: %s"
                    % (total, desconto, valor_a_pagar)
                )

    def calcular_arrecadado(self):
        valor_total = Dinheiro(0)
        for pedido in self._pedidos.values():
            if pedido.obter_status() == "P":
                total = pedido.itens.calcular_total()
                desconto = calcular_desconto(pedido.cliente.tipo, total)
                valor_total = valor_total.somar(total.subtrair(desconto))
        return valor_total

    def quantidade_abertos(self):
        quantidade = 0
        for pedido in self._pedidos.values():
            if pedido.obter_status() == "A":
                quantidade += 1
        return quantidade


pedidos = Pedidos()


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
    pedido = Pedido(cliente)
    pedidos.adicionar(numero, pedido)
    return pedido


def recusar_pedido(numero, nome, cpf, email, rua, cidade, cep, tipo):
    resultado = validar_dados(email, cpf, cep)
    if resultado != "ok":
        print("pedido", numero, "recusado:", resultado)


def adicionar_item(pedido, produto, quantidade):
    pedido.itens.adicionar(produto, quantidade)


def calcular_total(pedido):
    return pedido.itens.calcular_total()


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
    if pedido.obter_status() != "A":
        return False
    if not pedido.itens.tem_itens():
        return False
    pedido.definir_status("P")
    return True


def cancelar(pedido):
    if pedido.obter_status() != "A":
        return False
    pedido.definir_status("C")
    return True


def descricao_status(status):
    return Status(status).descricao()


def exibir_relatorio():
    pedidos.imprimir_relatorio()


def calcular_arrecadado():
    return pedidos.calcular_arrecadado()


def quantidade_pedidos_abertos():
    return pedidos.quantidade_abertos()


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
print("pagar 1:", pedidos.pagar(1))
print("pagar 3:", pedidos.pagar(3))
print("pagar 5:", pedidos.pagar(5))
print("pagar 6:", pedidos.pagar(6))
print("cancelar 5:", pedidos.cancelar(5))
print("cancelar 1:", pedidos.cancelar(1))

exibir_relatorio()
print("arrecadado:", calcular_arrecadado())
print("abertos:", quantidade_pedidos_abertos())
