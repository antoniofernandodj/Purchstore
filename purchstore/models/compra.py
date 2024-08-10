import csv
from datetime import datetime
from typing import List, Optional
from .itens import ItemCompra


class Compra:
    def __init__(
        self,
        mercado: str,
        emissao: str,
        emissao_datetime: datetime,
        serie: str,
        numero: str,
        total: float,
        n_itens: int,
        itens: List[ItemCompra],
        id: Optional[str] = None,
    ):
        self.id = id
        self.mercado = mercado
        self.emissao = emissao
        self.emissao_datetime = emissao_datetime
        self.serie = serie
        self.numero = numero
        self.total = total
        self.n_itens = n_itens
        self.itens = itens

    def get_filename(self):
        return (
            f'compras-{self.emissao_datetime}'
            .replace('/', '-')
            .replace(' ', '_')
        )

    def export_items_to_csv(self, arquivo_csv: str):
        with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Cabeçalhos
            writer.writerow([
                "Código",
                "Nome",
                "Quantidade",
                "Unidade",
                "Valor Unitário",
                "Valor Total"
            ])
            for item in self.itens:
                writer.writerow([
                    item.codigo,
                    item.name,
                    item.quantidade,
                    item.unidade,
                    item.valor_unitario,
                    item.valor_total
                ])

    def __str__(self):
        return (f"Compra(mercado={repr(self.mercado)}, emissao={repr(self.emissao)}, "  # noqa
                f"emissao_datetime={repr(self.emissao_datetime)}, serie={repr(self.serie)}, "  # noqa
                f"numero={repr(self.numero)}, total={repr(self.total)}, "
                f"n_itens={repr(self.n_itens)}, itens={repr(self.itens)}, "
                f"id={repr(self.id)})")

    def __repr__(self):
        return (f"Compra(mercado={repr(self.mercado)}, emissao={repr(self.emissao)}, "  # noqa
                f"emissao_datetime={repr(self.emissao_datetime)}, serie={repr(self.serie)}, "  # noqa
                f"numero={repr(self.numero)}, total={repr(self.total)}, "
                f"n_itens={repr(self.n_itens)}, itens={repr(self.itens)}, "
                f"id={repr(self.id)})")
