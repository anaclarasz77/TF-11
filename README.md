TF-11 — Object Calisthenics
1. Normalização
Normalizar é guardar cada informação em um único lugar e fazer os outros objetos referenciarem esse cadastro. Na loja, Ana é criada uma vez e seus pedidos 1 e 3 usam o mesmo objeto Cliente, evitando repetir seus dados em cada pedido.
2. Obsessão por tipos primitivos
O CPF virou uma classe para validar o tamanho no momento da criação e impedir que um valor inválido circule pelo programa. O Dinheiro guarda centavos inteiros porque operações com float podem gerar imprecisões; assim, os cálculos monetários ficam exatos.
3. Diga, não pergunte
Antes, o código precisava consultar o status e decidir fora do pedido se poderia pagar ou cancelar. Agora, chamamos pagar() ou cancelar() e o próprio Pedido aplica as regras, mantendo a decisão junto dos dados que ela protege.
4. Fail first
O hadouken aparecia na validação dos dados do pedido, com várias condições aninhadas. As validações agora ficam nos construtores dos tipos de valor e os métodos de comportamento retornam cedo quando não podem executar a ação; o desconto é resolvido por polimorfismo, sem uma sequência de if/elif/else.
5. Modularização
- Cpf: valida e representa um CPF.
- Email: valida e representa um email.
- Cep: valida e representa um CEP.
- Dinheiro: realiza operações monetárias usando centavos.
- Status: representa e altera o estado do pedido.
- TipoNormal: calcula o desconto de cliente normal.
- TipoVip: calcula o desconto de cliente VIP.
- TipoFuncionario: calcula o desconto de funcionário.
- Pessoa: reúne nome, CPF e email.
- Endereco: reúne rua, cidade e CEP.
- Cliente: associa pessoa, endereço e tipo de desconto.
- Produto: guarda nome e preço do produto.
- ItemDoPedido: associa produto e quantidade.
- ItensDoPedido: administra os itens e calcula seu total.
- Pedido: aplica as regras de pagamento e cancelamento e apresenta o pedido.
- Pedidos: administra os pedidos e gera os totais do relatório.
6. Dívida técnica
A validação de CPF e CEP verifica somente o tamanho, conforme o enunciado, e não os dígitos verificadores ou o formato numérico. Isso mantém o escopo da atividade, mas não seria suficiente em uma loja real; eu pagaria essa dívida antes de usar os cadastros em produção.