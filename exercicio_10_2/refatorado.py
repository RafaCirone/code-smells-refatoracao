"""
Exercício 10.2 — Code Smells & Refatoração

Code smells identificados no código original
--------------------------------------------
- Data Clumps: (rua, numero, bairro, cidade, estado, cep) e (ddd, telefone_numero)
  sempre aparecem juntos — são conceitos que merecem classes próprias.
- Long Parameter List: o construtor recebe 11 parâmetros, o que facilita
  passar argumentos na ordem errada.
- Primitive Obsession: endereço e telefone são representados por strings soltas.
- Large Class: Funcionario guarda e formata dados que não são dele
  (formatação de endereço e de telefone).

Refatorações aplicadas
----------------------
- Extract Class / Introduce Parameter Object: Endereco e Telefone.
- Move Method: cada classe sabe se formatar (__str__).
- Funcionario passa a receber 5 parâmetros coesos.
"""
from dataclasses import dataclass


@dataclass
class Endereco:
    rua: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str

    def __str__(self):
        return (
            f"{self.rua}, {self.numero} - {self.bairro}, "
            f"{self.cidade}/{self.estado} - CEP: {self.cep}"
        )


@dataclass
class Telefone:
    ddd: str
    numero: str

    def __str__(self):
        return f"({self.ddd}) {self.numero}"


class Funcionario:
    def __init__(self, nome, cargo, salario, endereco: Endereco, telefone: Telefone):
        self.nome = nome
        self.cargo = cargo
        self.salario = salario
        self.endereco = endereco
        self.telefone = telefone

    def exibir_dados(self):
        print(f"Funcionario: {self.nome} - {self.cargo}")
        print(f"Contato: {self.telefone}")
        print(f"Endereço: {self.endereco}")


if __name__ == "__main__":
    endereco = Endereco("Av. Paulista", "1000", "Bela Vista", "São Paulo", "SP", "01310-100")
    telefone = Telefone("11", "99999-0000")
    Funcionario("João", "Analista", 5000.0, endereco, telefone).exibir_dados()
