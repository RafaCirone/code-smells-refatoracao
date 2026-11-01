# Lab 10 — Code Smells & Refatoração

Cada pasta contém o arquivo `refatorado.py` de um exercício, com os code smells identificados e as refatorações explicadas no topo do arquivo. Todos os arquivos rodam com `python refatorado.py`.

| Exercício | Code smells principais | Refatoração principal |
|---|---|---|
| [10.1](exercicio_10_1/refatorado.py) | Long Method, violação do SRP, Switch Statements, Magic Numbers | Extract Class + Strategy (pagamento) |
| [10.2](exercicio_10_2/refatorado.py) | Data Clumps, Long Parameter List, Primitive Obsession | Extract Class (`Endereco`, `Telefone`) |
| [10.3](exercicio_10_3/refatorado.py) | Long Parameter List, Data Clumps, Magic Number | Introduce Parameter Object (`Hospede`, `Quarto`, `Periodo`) |
| [10.4](exercicio_10_4/refatorado.py) | Switch Statements, Magic Numbers | Replace Conditional with Polymorphism |
| [10.5](exercicio_10_5/refatorado.py) | Divergent Change (SRP), Magic Number | Extract Class (`ProdutoRepository`, `ProdutoXmlExporter`) |
| [10.6](exercicio_10_6/refatorado.py) | Duplicated Code, Comentários excessivos, Magic Numbers | Extract Method |
| [10.7](exercicio_10_7/refatorado.py) | Message Chains (Lei de Deméter) | Hide Delegate |
