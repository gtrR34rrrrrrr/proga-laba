# Алгоритмическая обработка числовых рядов (`num_series`)

Модульное консольное приложение на Python для генерации и загрузки числовых рядов, расчёта базовых статистических показателей и сглаживания методами скользящей средней (SMA, CMA, EMA).

# Примеры запуска

```bash
# генерация синусоиды и расчёт показателей
python main.py --kind sine --n 20 --window 3 --alpha 0.3 --seed 7

#генерация случайного ряда и сохранение в json
python main.py --kind random --n 50 --save data/random.json

#загрузка ряда из JSON или CSV и анализ
python main.py --load data/random.json --window 5

#экспорт сгенерированного ряда в csv
python main.py --kind trend --n 30 --export out.csv