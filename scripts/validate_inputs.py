#!/usr/bin/env python3
"""Проверка скачанных списков CIDR и фиксация их происхождения.

Пишет <dir>/sources.json — перечень источников без временных меток, чтобы файл
менялся только вместе с содержимым и его можно было публиковать в release.
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import sys
from pathlib import Path

DEFAULT_MIN_LINES = 10
DEFAULT_MIN_VALID_RATIO = 0.99


def scan(path: Path) -> tuple[int, int]:
    """Возвращает количество значимых строк и количество валидных CIDR."""
    lines = valid = 0
    with path.open(encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            lines += 1
            try:
                ipaddress.ip_network(line, strict=False)
                valid += 1
            except ValueError:
                continue
    return lines, valid


def parse_source(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError(f"ожидается NAME=URL, получено: {value}")
    name, url = value.split("=", 1)
    return name, url


def parse_min_lines(values: list[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in values:
        name, _, threshold = item.partition("=")
        try:
            result[name] = int(threshold)
        except ValueError:
            raise argparse.ArgumentTypeError(f"ожидается NAME=N, получено: {item}") from None
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dir", type=Path, help="каталог со скачанными списками и config.json")
    parser.add_argument("sources", nargs="+", type=parse_source, metavar="NAME=URL")
    parser.add_argument(
        "--min-lines",
        action="append",
        default=[],
        metavar="NAME=N",
        help=f"минимум значимых строк для источника (по умолчанию {DEFAULT_MIN_LINES})",
    )
    parser.add_argument("--min-valid-ratio", type=float, default=DEFAULT_MIN_VALID_RATIO)
    args = parser.parse_args()

    min_lines = parse_min_lines(args.min_lines)

    config_path = args.dir / "config.json"
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"::error::не удалось прочитать {config_path}: {exc}")
        return 1
    if not config.get("input") or not config.get("output"):
        print("::error::config.json: отсутствует input или output")
        return 1

    errors: list[str] = []
    entries: list[dict[str, object]] = []

    for name, url in args.sources:
        path = args.dir / name
        if not path.is_file():
            errors.append(f"{name}: файл не найден")
            continue

        data = path.read_bytes()
        lines, valid = scan(path)
        ratio = valid / lines if lines else 0.0
        threshold = min_lines.get(name, DEFAULT_MIN_LINES)

        print(f"{name}: строк={lines}, валидных CIDR={valid} ({ratio:.1%}), байт={len(data)}")
        if lines < threshold:
            errors.append(f"{name}: значимых строк {lines} < минимума {threshold}")
        if ratio < args.min_valid_ratio:
            errors.append(f"{name}: доля валидных CIDR {ratio:.1%} < {args.min_valid_ratio:.0%}")

        entries.append(
            {
                "file": name,
                "url": url,
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
                "cidr_count": valid,
            }
        )

    out_path = args.dir / "sources.json"
    out_path.write_text(
        json.dumps({"schema": 1, "sources": entries}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    for message in errors:
        print(f"::error::{message}")
    if errors:
        return 1

    print(f"✅ входные списки прошли проверку, происхождение записано в {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
