"""Точка входа CLI-приложения для анализа числовых рядов (Лабораторная работа 5.1, Вариант 9)."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import List

from num_series import (
    benchmark_moving_average,
    centered_moving_average,
    exponential_moving_average,
    load_series_auto,
    random_series,
    save_series_json,
    simple_moving_average,
    simple_moving_average_deque,
    sine_series,
    squared_random_series,
    summarize,
    trend_series,
    weighted_moving_average,
)


def build_parser() -> argparse.ArgumentParser:
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Анализ числовых рядов: статистика, скользящие средние и бенчмарк."
    )

    # Источник данных: генерация или загрузка из файла
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument(
        "--kind",
        choices=["random", "sine", "trend", "squared"],
        default="squared",
        help="тип генерируемого ряда (по умолчанию: squared — Вариант 9)",
    )
    source_group.add_argument(
        "--load",
        type=str,
        help="путь к файлу (.json, .txt, .csv) для загрузки ряда",
    )

    # Параметры генерации (по умолчанию n = 1000 согласно методичке)
    parser.add_argument(
        "--n",
        type=int,
        default=1000,
        help="длина генерируемого ряда (по умолчанию: 1000)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="seed генератора случайных чисел для воспроизводимости",
    )

    # Параметры скользящих средних (по умолчанию k = window = 10 согласно методичке)
    parser.add_argument(
        "--window",
        "-k",
        type=int,
        default=10,
        help="размер окна скользящей средней k (по умолчанию: 10)",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=None,
        help="коэффициент сглаживания EMA в (0, 1] (по умолчанию: 2 / (k + 1))",
    )

    # Экспорт и сохранение
    parser.add_argument(
        "--save",
        type=str,
        help="сохранить исходный ряд в JSON-файл",
    )
    parser.add_argument(
        "--export",
        type=str,
        help="экспортировать исходный ряд и скользящие средние в CSV-файл",
    )

    # Бенчмарк (ЛР 5.1)
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="замерить время выполнения SMA для list и deque",
    )

    return parser


def _generate_or_load(args: argparse.Namespace) -> List[float]:
    """Загружает ряд из файла или генерирует новый по выбранному типу."""
    if args.load:
        return load_series_auto(args.load)

    if args.kind == "squared":
        return squared_random_series(n=args.n, seed=args.seed)
    if args.kind == "random":
        return random_series(n=args.n, seed=args.seed)
    if args.kind == "sine":
        return sine_series(n=args.n, noise=0.1, seed=args.seed)
    if args.kind == "trend":
        return trend_series(n=args.n, noise=0.5, seed=args.seed)

    raise ValueError(f"Неизвестный тип ряда: {args.kind}")


def _export_csv(
    path: str,
    data: List[float],
    sma: List[float],
    wma: List[float],
    ema: List[float],
    window: int,
) -> None:
    """Сохраняет исходный ряд и скользящие средние в CSV."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    offset = window - 1

    with file_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "value", "sma", "wma", "ema"])
        for i, val in enumerate(data):
            sma_val = f"{sma[i - offset]:.6f}" if i >= offset else ""
            wma_val = f"{wma[i - offset]:.6f}" if i >= offset else ""
            ema_val = f"{ema[i]:.6f}"
            writer.writerow([i, f"{val:.6f}", sma_val, wma_val, ema_val])


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        data = _generate_or_load(args)
        n = len(data)
        window = args.window
        alpha = args.alpha if args.alpha is not None else 2.0 / (window + 1)

        # 1. Статистическая сводка (включает skewness_pearson из Варианта 9)
        stats = summarize(data)

        print("=" * 60)
        source_label = f"файл '{args.load}'" if args.load else f"генератор '{args.kind}'"
        print(f"Анализ числового ряда ({source_label}, n = {n}, k = {window})")
        print("-" * 60)
        for key, value in stats.items():
            if isinstance(value, int):
                print(f"  {key:<20}: {value}")
            else:
                print(f"  {key:<20}: {value:.6f}")

        # 2. Расчёт скользящих средних (SMA, WMA, EMA)
        sma_list = simple_moving_average(data, window)
        sma_deque = simple_moving_average_deque(data, window)
        wma = weighted_moving_average(data, window)
        ema = exponential_moving_average(data, alpha)

        print("-" * 60)
        print(f"Скользящие средние (окно k = {window}, alpha = {alpha:.4f}):")
        print(f"  SMA (list)  [len={len(sma_list)}]: первые 5 -> {[round(x, 4) for x in sma_list[:5]]}")
        print(f"  SMA (deque) [len={len(sma_deque)}]: первые 5 -> {[round(x, 4) for x in sma_deque[:5]]}")
        print(f"  WMA         [len={len(wma)}]: первые 5 -> {[round(x, 4) for x in wma[:5]]}")
        print(f"  EMA         [len={len(ema)}]: первые 5 -> {[round(x, 4) for x in ema[:5]]}")

        if window == n:
            print(f"  [Краевой кейс k == n]: SMA выродилась в одно число = {sma_list[0]:.6f}")

        if window % 2 == 1:
            cma = centered_moving_average(data, window)
            print(f"  CMA         [len={len(cma)}]: первые 5 -> {[round(x, 4) for x in cma[:5]]}")

        # 3. Сохранение / Экспорт при наличии флагов
        if args.save:
            save_series_json(data, args.save, meta={"kind": args.kind, "seed": args.seed})
            print("-" * 60)
            print(f"Ряд сохранён в JSON: {args.save}")

        if args.export:
            _export_csv(args.export, data, sma_list, wma, ema, window)
            print("-" * 60)
            print(f"Результаты экспортированы в CSV: {args.export}")

        # 4. Замер производительности (ЛР 5.1)
        if args.benchmark:
            print("-" * 60)
            print("Замер времени выполнения SMA (среднее за 1000 повторов):")
            timings = benchmark_moving_average(data, window, repeats=1000)
            print(f"  list  : {timings['list']:.8f} с")
            print(f"  deque : {timings['deque']:.8f} с")
            if timings["deque"] > 0:
                print(f"  отношение (list/deque): {timings['list'] / timings['deque']:.2f}")

        print("=" * 60)

    except ValueError as err:
        print(f"Ошибка: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()