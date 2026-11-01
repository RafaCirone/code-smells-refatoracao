"""
Exercício 10.5 — Code Smells & Refatoração

Code smells identificados no código original
--------------------------------------------
- Divergent Change / violação do SRP: a classe Produto muda por motivos
  diferentes — regra de negócio (imposto), persistência (SQL) e
  serialização (XML).
- Magic number: 1.15 (alíquota de imposto).
- Bônus: o SQL era montado por interpolação de strings, abrindo espaço para
  SQL Injection; o XML não escapava caracteres especiais.

Refatorações aplicadas
----------------------
- Extract Class: ProdutoRepository (persistência) e ProdutoXmlExporter
  (exportação). Produto fica só com dados e regras de negócio.
- Replace Magic Number with Symbolic Constant: ALIQUOTA_IMPOSTO.
- SQL parametrizado e XML gerado com xml.etree, que escapa os valores.
"""
import xml.etree.ElementTree as ET

ALIQUOTA_IMPOSTO = 0.15


class Produto:
    """Entidade de domínio: dados e regras de negócio."""

    def __init__(self, id_produto, nome, preco):
        self.id_produto = id_produto
        self.nome = nome
        self.preco = preco

    def calcular_preco_com_imposto(self):
        return self.preco * (1 + ALIQUOTA_IMPOSTO)


class ProdutoRepository:
    """Responsável pela persistência de produtos."""

    SQL_INSERT = "INSERT INTO produtos (id, nome, preco) VALUES (?, ?, ?);"

    def __init__(self, conexao=None):
        self.conexao = conexao

    def salvar(self, produto):
        parametros = (produto.id_produto, produto.nome, produto.preco)
        if self.conexao is None:
            # Sem banco configurado: apenas mostra o comando (comportamento original).
            print(self.SQL_INSERT, parametros)
            return
        self.conexao.execute(self.SQL_INSERT, parametros)
        self.conexao.commit()


class ProdutoXmlExporter:
    """Responsável por serializar produtos em XML."""

    def exportar(self, produto):
        raiz = ET.Element("produto")
        ET.SubElement(raiz, "id").text = str(produto.id_produto)
        ET.SubElement(raiz, "nome").text = produto.nome
        ET.SubElement(raiz, "preco").text = str(produto.preco)
        return ET.tostring(raiz, encoding="unicode")


if __name__ == "__main__":
    produto = Produto(1, "Teclado", 200.0)
    print(f"Preço com imposto: R$ {produto.calcular_preco_com_imposto():.2f}")
    ProdutoRepository().salvar(produto)
    print(ProdutoXmlExporter().exportar(produto))
