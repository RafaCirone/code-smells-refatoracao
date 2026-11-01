"""
Exercício 10.6 — Code Smells & Refatoração

Code smells identificados no código original
--------------------------------------------
- Duplicated Code: processar_pagamento_credito e processar_pagamento_debito
  são idênticos, mudando apenas a taxa e o rótulo.
- Comentários excessivos/redundantes: "# Imprime o valor na tela" logo acima de
  um print apenas repete o código. Um deles ainda é enganoso ("Retorna erro se
  for menor que zero"): o código não retorna erro e também rejeita o zero.
- Magic numbers: 0.05 e 0.02.
- Tratamento de erro inadequado: valor inválido apenas imprime uma mensagem,
  e quem chama não tem como saber que falhou.

Refatorações aplicadas
----------------------
- Extract Method: lógica comum em `_processar_pagamento`.
- Replace Magic Number with Symbolic Constant: TAXA_CREDITO, TAXA_DEBITO.
- Remoção de comentários redundantes; nomes claros tornam o código autoexplicativo.
- Valor inválido levanta ValueError e o valor final é retornado.
- Os métodos públicos foram mantidos para não quebrar quem já os usa.
"""

TAXA_CREDITO = 0.05
TAXA_DEBITO = 0.02


class ProcessadorFinanceiro:
    def processar_pagamento_credito(self, valor):
        return self._processar_pagamento(valor, TAXA_CREDITO, "crédito")

    def processar_pagamento_debito(self, valor):
        return self._processar_pagamento(valor, TAXA_DEBITO, "débito")

    def _processar_pagamento(self, valor, taxa, modalidade):
        self._validar_valor(valor)
        valor_com_taxa = valor * (1 + taxa)
        print(f"Processando {modalidade}: R$ {valor_com_taxa:.2f}")
        return valor_com_taxa

    @staticmethod
    def _validar_valor(valor):
        if valor <= 0:
            raise ValueError("Valor inválido: deve ser maior que zero")


if __name__ == "__main__":
    processador = ProcessadorFinanceiro()
    processador.processar_pagamento_credito(100)
    processador.processar_pagamento_debito(100)
    try:
        processador.processar_pagamento_debito(0)
    except ValueError as erro:
        print(erro)
