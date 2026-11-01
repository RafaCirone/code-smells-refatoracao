"""
Exercício 10.3 — Code Smells & Refatoração

Code smells identificados no código original
--------------------------------------------
- Long Parameter List: `criar_reserva` recebe 9 parâmetros.
- Data Clumps: dados do hóspede (nome, cpf, email), do quarto (numero, tipo,
  valor_diaria) e do período (checkin, checkout) sempre andam juntos.
- Mistura de responsabilidades: a mesma função calcula o valor e imprime na tela.
- Magic number: 50 (valor diário do café da manhã).
- Parâmetro não utilizado: email_hospede era recebido e nunca usado
  (mantido em Hospede, onde faz sentido como dado do hóspede).

Refatorações aplicadas
----------------------
- Introduce Parameter Object: Hospede, Quarto e Periodo.
- Extract Class: Reserva, que concentra a regra de cálculo.
- Separate Query from Modifier: cálculo (calcular_total) separado da exibição.
- Replace Magic Number with Symbolic Constant: VALOR_DIARIO_CAFE_DA_MANHA.
"""
from dataclasses import dataclass
from datetime import date

VALOR_DIARIO_CAFE_DA_MANHA = 50.0


@dataclass
class Hospede:
    nome: str
    cpf: str
    email: str


@dataclass
class Quarto:
    numero: int
    tipo: str
    valor_diaria: float


@dataclass
class Periodo:
    checkin: date
    checkout: date

    @property
    def total_dias(self):
        return (self.checkout - self.checkin).days


@dataclass
class Reserva:
    hospede: Hospede
    quarto: Quarto
    periodo: Periodo
    possui_cafe_da_manha: bool = False

    def calcular_total(self):
        dias = self.periodo.total_dias
        total = dias * self.quarto.valor_diaria
        if self.possui_cafe_da_manha:
            total += VALOR_DIARIO_CAFE_DA_MANHA * dias
        return total

    def exibir_resumo(self):
        print(f"Reserva criada para {self.hospede.nome} (CPF: {self.hospede.cpf})")
        print(f"Quarto {self.quarto.numero} ({self.quarto.tipo})")
        print(f"De {self.periodo.checkin} até {self.periodo.checkout}")
        print(f"Total a pagar: R$ {self.calcular_total():.2f}")


def criar_reserva(hospede, quarto, periodo, possui_cafe_da_manha=False):
    reserva = Reserva(hospede, quarto, periodo, possui_cafe_da_manha)
    reserva.exibir_resumo()
    return reserva


if __name__ == "__main__":
    criar_reserva(
        Hospede("Ana", "123.456.789-00", "ana@email.com"),
        Quarto(101, "Luxo", 300.0),
        Periodo(date(2026, 11, 10), date(2026, 11, 13)),
        possui_cafe_da_manha=True,
    )
