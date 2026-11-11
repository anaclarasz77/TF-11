# Etapa 4: criação de tipos específicos para os dados da loja.


class Cpf:
    # Representa um CPF e valida seu tamanho.
    def __init__(self, valor):
        if len(valor) != 11:
            raise ValueError("cpf invalido")
        self._valor = valor

    def __str__(self):
        return self._valor


class Email:
    # Representa um email e valida seu conteúdo básico.
    def __init__(self, valor):
        if not valor:
            raise ValueError("email vazio")
        if "@" not in valor:
            raise ValueError("email invalido")
        self._valor = valor

    def __str__(self):
        return self._valor


class Cep:
    # Representa um CEP com oito caracteres.
    def __init__(self, valor):
        if len(valor) != 8:
            raise ValueError("cep invalido")
        self._valor = valor

    def __str__(self):
        return self._valor


class Dinheiro:
    # Armazena dinheiro em centavos inteiros.
    def __init__(self, centavos):
        self._centavos = int(centavos)

    def somar(self, outro):
        return Dinheiro(self._centavos + outro._centavos)

    def subtrair(self, outro):
        return Dinheiro(self._centavos - outro._centavos)

    def multiplicar(self, quantidade):
        return Dinheiro(self._centavos * quantidade)

    def percentual(self, porcentagem):
        centavos = (self._centavos * porcentagem + 50) // 100
        return Dinheiro(centavos)

    def __str__(self):
        reais = self._centavos // 100
        centavos = self._centavos % 100
        return f"R$ {reais}.{centavos:02d}"


class Status:
    # Representa e controla o estado de um pedido.
    def __init__(self, codigo):
        if codigo not in ("A", "P", "C"):
            raise ValueError("status invalido")
        self._codigo = codigo

    def descricao(self):
        return {
            "A": "aberto",
            "P": "pago",
            "C": "cancelado"
        }[self._codigo]

    def esta_aberto(self):
        return self._codigo == "A"

    def esta_pago(self):
        return self._codigo == "P"

    def pagar(self):
        self._codigo = "P"

    def cancelar(self):
        self._codigo = "C"


class Pessoa:
    # Reúne os dados pessoais de um cliente.
    def __init__(self, nome, cpf, email):
        self._nome = nome
        self._cpf = cpf
        self._email = email

    def nome_para_relatorio(self):
        return self._nome


class Endereco:
    # Reúne os dados de localização de um cliente.
    def __init__(self, rua, cidade, cep):
        self._rua = rua
        self._cidade = cidade
        self._cep = cep

    def cidade_para_relatorio(self):
        return self._cidade


class Cliente:
    # Associa dados pessoais, endereço e tipo.
    def __init__(self, pessoa, endereco, tipo):
        self._pessoa = pessoa
        self._endereco = endereco
        self._tipo = tipo

    def nome_para_relatorio(self):
        return self._pessoa.nome_para_relatorio()

    def cidade_para_relatorio(self):
        return self._endereco.cidade_para_relatorio()

    def calcular_desconto(self, total):
        return calcular_desconto(self._tipo, total)


class Produto:
    # Representa um produto e seu preço unitário.
    def __init__(self, nome, preco):
        self._nome = nome
        self._preco = preco

    def calcular_total(self, quantidade):
        return self._preco.multiplicar(quantidade)

    def nome_para_relatorio(self):
        return self._nome


class ItemDoPedido:
    # Associa um produto à quantidade comprada.
    def __init__(self, produto, quantidade):
        self._produto = produto
        self._quantidade = quantidade

    def calcular_total(self):
        return self._produto.calcular_total(self._quantidade)

    def imprimir(self):
        print(
            "  ",
            self._quantidade,
            "x",
            self._produto.nome_para_relatorio(),
            "= %s" % self.calcular_total()
        )


class ItensDoPedido:
    # Administra os itens sem expor sua lista interna.
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
            item.imprimir()


class Pedido:
    # Controla o cliente, os itens e o próprio status.
    def __init__(self, cliente):
        self._cliente = cliente
        self._itens = ItensDoPedido()
        self._status = Status("A")

    def adicionar_item(self, produto, quantidade):
        self._itens.adicionar(produto, quantidade)

    def calcular_total(self):
        return self._itens.calcular_total()

    def esta_aberto(self):
        return self._status.esta_aberto()

    def esta_pago(self):
        return self._status.esta_pago()

    def descricao_status(self):
        return self._status.descricao()

    def pagar(self):
        if not self._status.esta_aberto():
            return False
        if not self._itens.tem_itens():
            return False
        self._status.pagar()
        return True

    def cancelar(self):
        if not self._status.esta_aberto():
            return False
        self._status.cancelar()
        return True

    def valor_a_pagar(self):
        total = self.calcular_total()
        desconto = self._cliente.calcular_desconto(total)
        return total.subtrair(desconto)

    def imprimir(self, numero):
        print(
            "Pedido", numero, "-",
            self._cliente.nome_para_relatorio(), "-",
            self._cliente.cidade_para_relatorio()
        )
        print("  status:", self.descricao_status())
        self._itens.imprimir()

        if self._itens.tem_itens():
            total = self.calcular_total()
            desconto = self._cliente.calcular_desconto(total)
            print(
                "  total: %s | desconto: %s | a pagar: %s"
                % (total, desconto, self.valor_a_pagar())
            )


class Pedidos:
    # Administra os pedidos identificados por seus números.
    def __init__(self):
        self._pedidos = {}

    def adicionar(self, numero, pedido):
        self._pedidos[numero] = pedido

    def pagar(self, numero):
        pedido = self._pedidos[numero]
        return pedido.pagar()

    def cancelar(self, numero):
        pedido = self._pedidos[numero]
        return pedido.cancelar()

    def imprimir_relatorio(self):
        for numero, pedido in self._pedidos.items():
            pedido.imprimir(numero)

    def calcular_arrecadado(self):
        valor_total = Dinheiro(0)
        for pedido in self._pedidos.values():
            if pedido.esta_pago():
                valor_total = valor_total.somar(pedido.valor_a_pagar())
        return valor_total

    def quantidade_abertos(self):
        quantidade = 0
        for pedido in self._pedidos.values():
            if pedido.esta_aberto():
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
    pessoa = Pessoa(nome, Cpf(cpf), Email(email))
    endereco = Endereco(rua, cidade, Cep(cep))
    return Cliente(pessoa, endereco, tipo)


def criar_pedido(numero, cliente):
    pedido = Pedido(cliente)
    pedidos.adicionar(numero, pedido)
    return pedido


def recusar_pedido(numero, nome, cpf, email, rua, cidade, cep, tipo):
    resultado = validar_dados(email, cpf, cep)
    if resultado != "ok":
        print("pedido", numero, "recusado:", resultado)


def adicionar_item(pedido, produto, quantidade):
    pedido.adicionar_item(produto, quantidade)


def calcular_total(pedido):
    return pedido.calcular_total()


def calcular_desconto(tipo, valor_total):
    if tipo == "V":
        return valor_total.percentual(10)
    if tipo == "F":
        return valor_total.percentual(20)
    return valor_total.percentual(0)


def calcular_valor_a_pagar(pedido):
    return pedido.valor_a_pagar()


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
