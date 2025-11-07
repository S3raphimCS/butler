import os
import re

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from loguru import logger
from django.core.files.base import ContentFile

from butler_core import celery_app
from butler_core.apps.periodic_tasks.helpers import check_vpn_config
from butler_core.apps.vpn_configs.models import VpnConfig


@celery_app.app.task
def parse_configs():
    try:
        base_url = "http://78.142.193.246:33304/en/"
        download_url = "http://78.142.193.246:33304"
        filename_regex = r"[a-zA-Z0-9.-]+.opengw.net"
        filepath = settings.MEDIA_ROOT
        payload = {"C_OpenVPN": "on"}
        main_page = requests.get(base_url, params=payload)
        main_page.raise_for_status()
    except requests.RequestException as err:
        logger.error(err)
        exit()

    soup = BeautifulSoup(main_page.text, 'lxml')
    table_rows = soup.select("table#vg_hosts_table_id tr")
    for row in table_rows:
        try:
            country = row.select("td")[0].text
            if "Country" in country or "vpn" in country.lower() or country.isdigit():
                continue
            name = row.select("td")[1].text
            name_match = re.search(filename_regex, name).group(0)
            vpn_configs_links = row.find_all("a", )
            for config_link in vpn_configs_links:
                if "openvpn" in config_link.text.lower():
                    link = config_link["href"]

            # Получение ссылки на конфиг с DDNS
            config_page = requests.get(base_url + link)
            config_page.raise_for_status()
            config_page_soup = BeautifulSoup(config_page.text, 'lxml')
            link_tag = config_page_soup.select_one('a[href$=".ovpn"]')["href"]
            download_link = download_url + link_tag
            logger.info(country, name_match, download_link)

            response = requests.get(download_link, timeout=20)
            response.raise_for_status()
            file = ContentFile(response.content, name=name_match+".ovpn")
            if not VpnConfig.objects.filter(name__icontains=name_match).exists():
                VpnConfig.objects.get_or_create(country=country, name=name_match+".ovpn", file=file)
            # command = ["curl", "--output", f"configs/{name_match}.ovpn", download_link]
            # logger.info((command)
            logger.success(f"Файл {name_match} успешно сохранен.")

        except Exception as err:
            logger.error(f"Ошибка при парсинге: {err}")
    logger.info("Работа с конфигами завершена.")


@celery_app.app.task
def check_unchecked_configs():
    configs = VpnConfig.objects.filter(is_checked=False)
    for config in configs:
        try:
            if check_vpn_config(config.file.path):
                config.is_working = True
            else:
                config.is_working = False
            config.is_checked = True
            config.save(update_fields=["is_working", "is_checked"])
        except Exception as err:
            logger.error(err)
    logger.info("Проверка новых конфигов завершена.")


@celery_app.app.task
def recheck_working_configs():
    configs = VpnConfig.objects.filter(is_working=True)
    for config in configs:
        try:
            if not check_vpn_config(config.file.path):
                config.is_working = False
                config.save(update_fields=["is_working"])
        except Exception as err:
            logger.error(err)

    logger.info("Перепроверка работающих конфигов завершена.")
