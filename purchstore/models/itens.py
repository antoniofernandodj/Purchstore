class ItemCompra:
    def __init__(
        self,
        codigo,
        compra_id,
        name,
        quantidade,
        unidade,
        valor_unitario,
        valor_total,
    ):
        self.codigo = codigo
        self.compra_id = compra_id
        self.name = name
        self.quantidade = quantidade
        self.unidade = unidade
        self.valor_unitario = valor_unitario
        self.valor_total = valor_total

    def __str__(self):
        return (f"ItemCompra(codigo={repr(self.codigo)}, compra_id={repr(self.compra_id)}, "  # noqa
                f"name={repr(self.name)}, quantidade={repr(self.quantidade)}, "  # noqa
                f"unidade={repr(self.unidade)}, valor_unitario={repr(self.valor_unitario)}, "  # noqa
                f"valor_total={repr(self.valor_total)})")

    def __repr__(self):
        return (f"ItemCompra(codigo={repr(self.codigo)}, compra_id={repr(self.compra_id)}, "  # noqa
                f"name={repr(self.name)}, quantidade={repr(self.quantidade)}, "  # noqa
                f"unidade={repr(self.unidade)}, valor_unitario={repr(self.valor_unitario)}, "  # noqa
                f"valor_total={repr(self.valor_total)})")
