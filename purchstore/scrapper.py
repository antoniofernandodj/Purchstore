from datetime import datetime
from typing import List
import bs4  # type: ignore
import re
import cv2
from pyzbar.pyzbar import decode  # type: ignore
from purchstore.models.compra import Compra
from purchstore.models.itens import ItemCompra
import purchstore.utils as utils
from urllib.parse import parse_qs, urlparse

# import requests
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


class Scrapper:

    def extract_url_from_qr(self, image_path):
        image = cv2.imread(image_path)
        decoded_objects = decode(image)

        for obj in decoded_objects:

            if not obj.type == 'QRCODE':
                raise ValueError

            parsed_url = urlparse(obj.data.decode('utf-8'))
            query_params = parse_qs(parsed_url.query)

            p_value = query_params['p'][0]

            return f"http://www4.fazenda.rj.gov.br/consultaNFCe/QRCode?p={p_value}"
        
        raise ValueError
    
    def parse_codes(self, codes: List[str]):
        from purchstore.database import db

        for code in codes:
            url = f"http://www4.fazenda.rj.gov.br/consultaNFCe/QRCode?p={code}"
            html = self.get_html(url)
            itens_compra = self.coletar_itens_de_compra(html)
            compra = self.coletar_compra_info(html, itens_compra)
            print('\n'*2)
            print('-'*10 + " ITENS " + '-'*10)
            [print(item) for item in itens_compra]
            print('-'*10 + " ITENS " + '-'*10)
            print('\n'*2)
            print('-'*10 + " COMPRA " + '-'*10)
            print(compra)
            print('-'*10 + " COMPRA " + '-'*10)
            db.inserir_compra(compra)
            print('\n\n\n\n----------------------\n\n\n\n')

    def get_html(self, url: str, headless=True):
        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        time.sleep(1)
        while url == driver.current_url:
            time.sleep(1)

        html = driver.page_source
        driver.close()
        return html

    def coletar_itens_de_compra(self, html_content: str):
        soup = bs4.BeautifulSoup(html_content, 'lxml')
        table = soup.find('table')

        if not isinstance(table, bs4.Tag):
            raise ValueError(
                "A tabela não foi encontrada "
                "ou não é um elemento <table>"
            )

        rows = table.find_all('tr')

        data: List[ItemCompra] = []

        row: bs4.Tag
        for row in rows:
            codigo_span = row.find('span', {"class": "RCod"})
            name_span = row.find('span', {"class": "txtTit"})
            qtd_span = row.find('span', {"class": "Rqtd"})
            unid_span = row.find('span', {"class": "RUN"})
            val_unit_span = row.find('span', {"class": "RvlUnit"})
            val_tot_span = row.find('span', {"class": "valor"})

            # Extraindo e limpando dados
            if (
                codigo_span and
                name_span and
                qtd_span and
                unid_span and
                val_unit_span and
                val_tot_span
            ):
                codigo = (
                    codigo_span.text.strip()
                    .replace('\t', '')
                    .replace('\n', '')
                    .replace(":", "")
                    .replace("(", '')
                    .replace(")", '')
                    .replace("Código", "")
                    .strip()
                )
                name = name_span.text.strip()

                self.clear_strong(unid_span)
                self.clear_strong(qtd_span)
                self.clear_strong(val_unit_span)

                qtd = utils.to_float(qtd_span.get_text(strip=True))
                unid = unid_span.get_text(strip=True)
                val_unit = utils.to_float(val_unit_span.get_text(strip=True))
                val_tot = utils.to_float(val_tot_span.get_text(strip=True))

                item = ItemCompra(
                    compra_id='',
                    codigo=codigo,
                    name=name,
                    quantidade=qtd,
                    unidade=unid,
                    valor_unitario=val_unit,
                    valor_total=val_tot
                )

                data.append(item)

        return data

    def coletar_compra_info(
        self,
        html_content: str,
        itens_compra: List[ItemCompra]
    ):
        soup = bs4.BeautifulSoup(html_content, 'lxml')

        values = utils.find_by_xpath(
            html_content,
            '//*[@id="infos"]/div[1]/div/ul/li/text()'
        )
        if values is None:
            raise

        values = [
            v.replace('\t', '').replace('\n', ' ')
            for v in values if v != '\n'
        ]

        mercado_soup = soup.find('div', {'class': "txtTopo"})
        if mercado_soup is None:
            raise ValueError

        datetime_str = values[2]
        match = re.match(
            r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})',
            datetime_str
        )
        if not match:
            raise ValueError(
                "Formato de data/hora não encontrado em 'emissao'"
            )

        emissao_datetime = datetime.strptime(
            match.group(1), '%d/%m/%Y %H:%M:%S'
        )

        compra = Compra(
            id='',
            numero=values[0],
            mercado=mercado_soup.text,
            emissao=values[2],
            emissao_datetime=emissao_datetime,
            serie=values[1],
            total=sum([item.valor_total for item in itens_compra]),
            n_itens=len(itens_compra),
            itens=itens_compra
        )

        return compra

    def clear_strong(self, tag):
        strong = tag.find('strong')
        if strong:
            strong.decompose()

    def parse_images(self, image_dir):
        from purchstore.database import db
        from os import listdir, path

        images = listdir(image_dir)
        for i, image in enumerate(images):
            if image.startswith('_'):
                continue

            print("--------------", image, "--------------")
            image_path = path.join(image_dir, image)

            try:
                url = self.extract_url_from_qr(image_path)
            except ValueError:
                continue

            # from content import html
            html = self.get_html(url)

            itens_compra = self.coletar_itens_de_compra(html)

            compra = self.coletar_compra_info(html, itens_compra)

            print('\n'*2)
            print('-'*10 + " ITENS " + '-'*10)
            [print(item) for item in itens_compra]
            print('-'*10 + " ITENS " + '-'*10)

            print('\n'*2)
            print('-'*10 + " COMPRA " + '-'*10)
            print(compra)
            print('-'*10 + " COMPRA " + '-'*10)

            db.criar_banco_de_dados()
            db.inserir_compra(compra)

            print('\n\n\n\n----------------------\n\n\n\n')
