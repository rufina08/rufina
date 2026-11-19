"""Точка входа CLI: обработка числовых рядов (Вариант 2)."""
from __future__ import annotations

import argparse
import csv
import sys
from typing import List, Optional, Tuple

from num_series import (
    gauss_series,
    constant_series,
    random_series,
    summarize,
    simple_moving_average,
    simple_moving_average_deque,
    weighted_moving_average,
    benchmark_moving_average,
    save_series_json,
    load_series_auto,
)


def build_series(kind: str, n: int, seed: int) -> List[float]:
    """Генерирует ряд заданного типа."""
    if kind == "gauss":
        return gauss_series(n=n, mu=50.0, sigma=10.0, seed=seed)
    if kind == "constant":
        return constant_series(n=n, value=50.0)
    if kind == "random":
        return random_series(n=n, low=0.0, high=100.0, seed=seed)
    raise ValueError(f"Неизвестный тип ряда: {kind!r}")


def obtain_series(args: argparse.Namespace) -> Tuple[List[float], str]:
    """Возвращает (ряд, описание источника)."""
    if args.load:
        data = load_series_auto(args.load)
        return data, f"файл: {args.load}"
    data = build_series(args.kind, args.n, args.seed)
    return data, f"сгенерирован ({args.kind}, n={args.n}, seed={args.seed})"


def export_series_csv(path: str, data: List[float]) -> None:
    """Экспорт ряда в CSV."""
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["i", "value"])
            for i, v in enumerate(data):
                w.writerow([i, v])
    except OSError as err:
        raise ValueError(f"Не удалось записать CSV {path}: {err}") from err


def print_series_preview(title: str, values: List[float], limit: int = 10) -> None:
    """Печатает первые limit элементов ряда."""
    preview = values[:limit]
    formatted = " ".join(f"{v:>8.3f}" for v in preview)
    suffix = " ..." if len(values) > limit else ""
    print(f"\n{title} (n={len(values)}):")
    print(f" {formatted}{suffix}")


def print_stats(stats: dict) -> None:
    modes_str = ", ".join(f"{m:.4f}" for m in stats["mode"][:5])
    if len(stats["mode"]) > 5:
        modes_str += f" ... (всего {len(stats['mode'])})"

    print(f"Среднее арифметическое : {stats['mean']:>10.4f}")
    print(f"Медиана                : {stats['median']:>10.4f}")
    print(f"Размах (max - min)     : {stats['spread']:>10.4f}")
    print(f"СКО (stdev)            : {stats['stdev']:>10.4f}")
    print(f"Мода (Counter)         : [{modes_str}]")
    print(f"min / max              : {stats['min']:>10.4f} / {stats['max']:.4f}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Алгоритмическая обработка числовых рядов (Вариант 2)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--kind",
        choices=["gauss", "constant", "random"],
        default="gauss",
        help="тип генерируемого ряда (constant — краевой кейс)",
    )
    parser.add_argument("--n", type=int, default=1000, help="длина ряда (по умолчанию 1000)")
    parser.add_argument("--window", type=int, default=10, help="размер окна k (по умолчанию 10)")
    parser.add_argument("--seed", type=int, default=42, help="зерно ГПСЧ")
    parser.add_argument("--load", metavar="PATH", help="загрузить ряд из файла")
    parser.add_argument("--save", metavar="PATH", help="сохранить ряд в JSON")
    parser.add_argument("--export", metavar="FILE", help="экспортировать ряд в CSV")
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="замерить время выполнения SMA для list и deque",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        data, source = obtain_series(args)
    except ValueError as err:
        print(f"Ошибка получения ряда: {err}", file=sys.stderr)
        return 1

    if args.save:
        try:
            save_series_json(data, args.save, meta={"source": source})
            print(f"[сохранено] {args.save}")
        except ValueError as err:
            print(f"Ошибка сохранения: {err}", file=sys.stderr)
            return 1

    if args.export:
        try:
            export_series_csv(args.export, data)
            print(f"[экспортировано] {args.export}")
        except ValueError as err:
            print(f"Ошибка экспорта: {err}", file=sys.stderr)
            return 1

    try:
        stats = summarize(data)
        sma_list = simple_moving_average(data, args.window)
        sma_deque = simple_moving_average_deque(data, args.window)
        wma = weighted_moving_average(data, args.window)
    except ValueError as err:
        print(f"Ошибка анализа: {err}", file=sys.stderr)
        return 1

    print("=" * 65)
    print(f"Источник данных: {source}")
    print("-" * 65)
    print_stats(stats)
    print_series_preview("Исходный ряд", data)
    print_series_preview(f"SMA list (window={args.window})", sma_list)
    print_series_preview(f"SMA deque (window={args.window})", sma_deque)
    print_series_preview(f"WMA линейные веса (window={args.window})", wma)

    if args.benchmark:
        print("-" * 65)
        print("Замер времени выполнения SMA (среднее за 1000 повторов):")
        timings = benchmark_moving_average(data, args.window, repeats=1000)
        print(f"  list  : {timings['list']:.8f} с")
        print(f"  deque : {timings['deque']:.8f} с")
        print(f"  отношение (list/deque): {timings['list'] / timings['deque']:.2f}")

    print("=" * 65)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

