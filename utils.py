import re
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.180 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:117.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/117.0.2045.55",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.93 Safari/537.36",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:116.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6015.42 Safari/537.36",
]


def parse_proxy(proxy_str: str) -> dict:
    # Формат: ip:port@login:pass, например "192.168.1.1:8080@user1:pass1"
    # Используем регулярное выражение для извлечения данных
    pattern = r'([^@]+)@([^:]+):(.+)'
    match = re.match(pattern, proxy_str.strip())

    if match:
        server, username, password = match.groups()
        # Добавляем протокол http:// к server, если его нет
        if not server.startswith('http'):
            server = f'http://{server}'
        return {
            'server': server,
            'username': username,
            'password': password
        }
    else:
        # Если строка не соответствует формату, возвращаем пустой объект
        print(f"Неверный формат прокси: {proxy_str}")
        return {
            'server': '',
            'username': '',
            'password': ''
        }