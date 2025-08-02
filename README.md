# pma-http-scraper

## Для запуска

1) Установите uv (poetry также пойдет) в свой глобальный path

```bash
pip install uv
```

или для poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2) Создайте и активируйте venv (uv имеет встроенный, в отличии от poetry 2.0+)

Для uv:

```bash
uv venv create
uv venv activate
```

3) Установите зависимости в зависимости от вашего пакетного менеджера

```bash
uv install
```

или для poetry:

```bash
poetry install
```

4) Запустите файл script.py

```bash
python script.py
```
