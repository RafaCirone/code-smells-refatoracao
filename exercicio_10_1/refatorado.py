"""
Exercício 10.1 — Code Smells & Refatoração

Code smells identificados no código original
--------------------------------------------
- Long Method / God Method: `processar_venda_e_gerar_relatorio` calcula o total,
  aplica desconto, cobra o pagamento, grava o relatório e imprime mensagens.
  O próprio nome com "e" denuncia várias responsabilidades (viola o SRP).
- Comentários usados como separadores ("# Lógica de cálculo", "# Lógica de
  desconto"...): sinal de que cada bloco deveria ser um método/classe próprio.
- Magic numbers / strings: 0.90, 'VIP', 'CARTAO', 'BOLETO', "relatorio_vendas.txt".
- Switch Statements (if/elif) sobre o método de pagamento: cada novo método
  exige alterar a classe (viola o Princípio Aberto/Fechado).
- Falha silenciosa: um método de pagamento desconhecido era ignorado e a venda
  era registrada mesmo assim.

Refatorações aplicadas
----------------------
- Extract Method / Extract Class: CalculadoraDeTotal e GeradorDeRelatorio.
- Replace Conditional with Polymorphism (Strategy): PagamentoCartao e PagamentoBoleto.
- Replace Magic Number with Symbolic Constant.
- GerenciadorDeVendas passa apenas a orquestrar o fluxo e recebe as
  dependências por injeção, o que facilita testes e extensões.
"""
from abc import ABC, abstractmethod

TIPO_CLIENTE_VIP = "VIP"
DESCONTO_VIP = 0.10
ARQUIVO_RELATORIO = "relatorio_vendas.txt"


class CalculadoraDeTotal:
    """Responsável apenas pelo cálculo do valor da venda."""

    def calcular(self, itens, cliente):
        subtotal = self._calcular_subtotal(itens)
        return self._aplicar_desconto(subtotal, cliente)

    @staticmethod
    def _calcular_subtotal(itens):
        return sum(item["preco"] * item["quantidade"] for item in itens)

    @staticmethod
    def _aplicar_desconto(valor, cliente):
        if cliente["tipo"] == TIPO_CLIENTE_VIP:
            return valor * (1 - DESCONTO_VIP)
        return valor


class MetodoDePagamento(ABC):
    """Estratégia de pagamento: novos métodos são novas classes."""

    @abstractmethod
    def cobrar(self, total):
        ...


class PagamentoCartao(MetodoDePagamento):
    def cobrar(self, total):
        print(f"Cobrando R$ {total:.2f} no cartão de crédito...")


class PagamentoBoleto(MetodoDePagamento):
    def cobrar(self, total):
        print(f"Gerando boleto no valor de R$ {total:.2f}...")


class GeradorDeRelatorio:
    """Responsável apenas por montar e persistir o relatório."""

    def __init__(self, caminho_arquivo=ARQUIVO_RELATORIO):
        self.caminho_arquivo = caminho_arquivo

    def gerar(self, cliente, total):
        relatorio = self._montar(cliente, total)
        with open(self.caminho_arquivo, "a", encoding="utf-8") as arquivo:
            arquivo.write(relatorio)

    @staticmethod
    def _montar(cliente, total):
        return (
            "--- Relatório de Venda ---\n"
            f"Cliente: {cliente['nome']}\n"
            f"Total: R$ {total:.2f}\n"
        )


class GerenciadorDeVendas:
    """Apenas orquestra as etapas da venda."""

    def __init__(self, calculadora=None, gerador_relatorio=None, metodos_pagamento=None):
        self.calculadora = calculadora or CalculadoraDeTotal()
        self.gerador_relatorio = gerador_relatorio or GeradorDeRelatorio()
        self.metodos_pagamento = metodos_pagamento or {
            "CARTAO": PagamentoCartao(),
            "BOLETO": PagamentoBoleto(),
        }

    def processar_venda(self, itens, cliente, metodo_pagamento):
        pagamento = self._obter_metodo_pagamento(metodo_pagamento)
        total = self.calculadora.calcular(itens, cliente)
        pagamento.cobrar(total)
        self.gerador_relatorio.gerar(cliente, total)
        print("Venda processada com sucesso.")
        return total

    def _obter_metodo_pagamento(self, codigo):
        try:
            return self.metodos_pagamento[codigo]
        except KeyError:
            raise ValueError(f"Método de pagamento desconhecido: {codigo}") from None


if __name__ == "__main__":
    itens = [
        {"preco": 50.0, "quantidade": 2},
        {"preco": 30.0, "quantidade": 1},
    ]
    cliente = {"nome": "Maria", "tipo": "VIP"}
    GerenciadorDeVendas().processar_venda(itens, cliente, "CARTAO")
