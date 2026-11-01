"""
Exercício 10.4 — Code Smells & Refatoração

Code smells identificados no código original
--------------------------------------------
- Switch Statements: cadeia de if/elif sobre `tipo_transporte`. Cada novo
  transporte obriga a editar o método (viola o Princípio Aberto/Fechado).
- Magic numbers: 2.0, 3.5, 10.0, 8.0, 50.0, 1.0 espalhados, explicados só
  por comentários.
- Primitive Obsession: o tipo de transporte é uma string livre, sujeita a erros
  de digitação.

Refatorações aplicadas
----------------------
- Replace Conditional with Polymorphism (Strategy): cada transporte é uma
  classe com sua própria tarifa por km e taxa base.
- Replace Magic Number with Symbolic Constant: os valores viram atributos
  nomeados (valor_por_km, taxa_base).
- Registro de transportes em dicionário: incluir um novo transporte não exige
  alterar CalculadoraDeFrete.
"""
from abc import ABC


class Transporte(ABC):
    valor_por_km: float = 0.0
    taxa_base: float = 0.0

    def calcular_frete(self, distancia):
        return distancia * self.valor_por_km + self.taxa_base


class Moto(Transporte):
    valor_por_km = 2.0


class Carro(Transporte):
    valor_por_km = 3.5
    taxa_base = 10.0


class Caminhao(Transporte):
    valor_por_km = 8.0
    taxa_base = 50.0


class Bicicleta(Transporte):
    valor_por_km = 1.0


TRANSPORTES = {
    "MOTO": Moto(),
    "CARRO": Carro(),
    "CAMINHAO": Caminhao(),
    "BICICLETA": Bicicleta(),
}


class CalculadoraDeFrete:
    def __init__(self, transportes=None):
        self.transportes = transportes or TRANSPORTES

    def calcular_frete(self, tipo_transporte, distancia):
        try:
            transporte = self.transportes[tipo_transporte]
        except KeyError:
            raise ValueError("Tipo de transporte desconhecido") from None
        return transporte.calcular_frete(distancia)


if __name__ == "__main__":
    calculadora = CalculadoraDeFrete()
    for tipo in TRANSPORTES:
        print(f"{tipo}: R$ {calculadora.calcular_frete(tipo, 10):.2f}")
