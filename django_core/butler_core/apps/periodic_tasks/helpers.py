import subprocess
import time
from loguru import logger

import requests


def get_public_ip():
    """Отправляет запрос на получение публичного IP-адреса."""
    api_url = "http://ip-api.com/json/?fields=61439"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data.get("query")
    except requests.RequestException as e:
        logger.error(f"Ошибка при получении публичного IP-адреса: {e}")


def check_vpn_config(config_path):
    """
    Проверяет работоспособность конфига openvpn
    :param config_path: Путь к файлу .ovpn
    :return: True, если VPN работает, иначе False.
    """

    original_ip = get_public_ip()
    if not original_ip:
        logger.error("Не удалось определить исходный IP. Проверка невозможна.")
        return False
    logger.info(f"Ваш реальный IP: {original_ip}")

    allowed_ciphers = "AES-256-GCM:AES-128-GCM:CHACHA20-POLY1305:AES-128-CBC"
    command = ["openvpn", "--config", config_path, "--data-ciphers", allowed_ciphers]

    process = None
    try:
        logger.info("Попытка подключиться к VPN, используя конфигурацию:", config_path)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8",
                                   errors="replace")

        connection_timeout = 20
        logger.info(f"Ждем {connection_timeout} секунд до установки соединения...")
        time.sleep(connection_timeout)

        if process.poll() is not None:
            logger.error("Процесс OpenVPN завершился преждевременно. Вероятно, ошибка в конфиге или с подключением.")
            return False

        new_ip = get_public_ip()
        logger.info(f"IP после подключения: {new_ip}")
        if new_ip and new_ip != original_ip:
            logger.success(f"✅ Успех! IP-адрес изменился. {config_path} - рабочий.")
            return True
        else:
            logger.error(f"❌ Неудача. IP-адрес не изменился или отсутствует интернет. {config_path} - нерабочий.")
            return False

    except Exception as error:
        logger.error(f"Произошла ошибка: {error}")

    finally:
        if process:
            logger.info("Закрываем процесс OpenVPN...")
            process.terminate()
            try:
                stdout_output, stderr_output = process.communicate(timeout=5)
                logger.info("-------OPENVPN STDOUT-------")
                logger.info(stdout_output)
                logger.info("----OPENVPN STDOUT END----")

                logger.info("-------OPENVPN STDERR-------")
                logger.info(stderr_output)
                logger.info("----OPENVPN STDERR END----")
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning("Процесс не завершился за отведенное время. Принудительно завершаем...")
                process.kill()
            logger.info("Соединение разорвано.")
