"""
Exercício 10.7 — Code Smells & Refatoração

Code smells identificados no código original
--------------------------------------------
- Message Chains: pedido.cliente.endereco.estado.pais.nome — o código cliente
  navega por cinco objetos para obter um dado.
- Violação da Lei de Deméter ("fale só com seus vizinhos imediatos"): a função
  conhece toda a estrutura interna de Pedido, Cliente, Endereco e Estado.
  Qualquer mudança nesse caminho quebra quem consome.
- Magic string: "Brasil".

Refatorações aplicadas
----------------------
- Hide Delegate: cada classe expõe um método que delega ao vizinho imediato
  (Pedido -> Cliente -> Endereco -> Estado -> Pais).
- Move Method: a decisão "é internacional?" vai para Pedido, que é quem tem
  o contexto; o código cliente apenas pergunta.
- Replace Magic String with Symbolic Constant: PAIS_ORIGEM.
"""

PAIS_ORIGEM = "Brasil"


class Pais:
    def __init__(self, nome):
        self.nome = nome


class Estado:
    def __init__(self, nome, pais):
        self.nome = nome
        self.pais = pais

    def nome_pais(self):
        return self.pais.nome


class Endereco:
    def __init__(self, rua, estado):
        self.rua = rua
        self.estado = estado

    def nome_pais(self):
        return self.estado.nome_pais()


class Cliente:
    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco

    def pais_de_residencia(self):
        return self.endereco.nome_pais()


class Pedido:
    def __init__(self, cliente, valor):
        self.cliente = cliente
        self.valor = valor

    def pais_destino(self):
        return self.cliente.pais_de_residencia()

    def eh_internacional(self):
        return self.pais_destino() != PAIS_ORIGEM


def verificar_frete_internacional(pedido):
    if pedido.eh_internacional():
        print("Sujeito a taxa de importação.")
    else:
        print("Frete nacional padrão.")


if __name__ == "__main__":
    brasil = Pais("Brasil")
    portugal = Pais("Portugal")

    pedido_nacional = Pedido(
        Cliente("Carlos", Endereco("Rua A", Estado("SP", brasil))), 100.0
    )
    pedido_internacional = Pedido(
        Cliente("Inês", Endereco("Rua B", Estado("Lisboa", portugal))), 250.0
    )

    verificar_frete_internacional(pedido_nacional)
    verificar_frete_internacional(pedido_internacional)
