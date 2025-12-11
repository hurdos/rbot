# Инвестиционные скрипты

Набор CLI-утилит для работы с Тинькофф Инвестициями: просмотр облигаций, позиций, операций и сохранение данных в SQLite.

## Установка
- Требования: Python 3.9+, `pip`.
- (Опционально) создать окружение: `python3 -m venv .venv && source .venv/bin/activate`.
- Установить зависимости: `pip install -r requirements.txt`.
- Скопировать `env.sample` в `.env` и прописать переменные:
  - `TOKEN` — токен Тинькофф Инвестиций.
  - `ACCOUNT_ID` — идентификатор счёта (можно переопределять аргументами CLI).

## Быстрый старт
- Показать портфель по счёту:  
  `python portfolio.py -a <ACCOUNT_ID>`
- Выгрузить и сохранить облигации из портфеля в SQLite, либо удалить:  
  `python bonds.py -U -a <ACCOUNT_ID>`  
  `python bonds.py -D <FIGI>`
- Показать прибыль/купонный поток или вывести CSV:  
  `python bonds.py`  
  `python bonds.py -C`
- Получить операции по инструменту (или сумму операций):  
  `python operations.py -i <FIGI|UID>`  
  `python operations.py -i <FIGI|UID> -S`

