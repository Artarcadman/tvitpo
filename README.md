# 1. Установка зависимостей
pip install -r requirements.txt

# 2. Запуск тестов
pytest

# 3. Проверка покрытия кода
coverage run -m pytest \
coverage report

# 4. Запуск основной программы
python main.py