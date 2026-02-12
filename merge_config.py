#!/usr/bin/env python3
import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any


def strip_jsonc_comments(text: str) -> str:
    result = []
    in_string = False
    in_line_comment = False
    in_block_comment = False
    escape = False
    i = 0
    length = len(text)

    while i < length:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < length else ""

        if in_line_comment:
            if ch == "\n" or ch == "\r":
                in_line_comment = False
                result.append(ch)
            else:
                result.append(" ")
            i += 1
            continue

        if in_block_comment:
            if ch == "*" and nxt == "/":
                in_block_comment = False
                result.append(" ")
                result.append(" ")
                i += 2
                continue
            if ch == "\n" or ch == "\r":
                result.append(ch)
            else:
                result.append(" ")
            i += 1
            continue

        if in_string:
            result.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == '"':
            in_string = True
            result.append(ch)
            i += 1
            continue

        if ch == "/" and nxt == "/":
            in_line_comment = True
            result.append(" ")
            result.append(" ")
            i += 2
            continue

        if ch == "/" and nxt == "*":
            in_block_comment = True
            result.append(" ")
            result.append(" ")
            i += 2
            continue

        result.append(ch)
        i += 1

    if in_block_comment:
        raise ValueError("Unclosed block comment in JSONC input")

    return "".join(result)


def strip_trailing_commas(text: str) -> str:
    result = []
    in_string = False
    escape = False
    i = 0
    length = len(text)

    while i < length:
        ch = text[i]

        if in_string:
            result.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == '"':
            in_string = True
            result.append(ch)
            i += 1
            continue

        if ch == ",":
            j = i + 1
            while j < length and text[j] in " \t\r\n":
                j += 1
            if j < length and text[j] in "]}":
                i += 1
                continue

        result.append(ch)
        i += 1

    return "".join(result)


def load_jsonc(path: Path) -> Any:
    raw = path.read_text(encoding="utf-8")
    without_comments = strip_jsonc_comments(raw)
    normalized = strip_trailing_commas(without_comments)
    try:
        return json.loads(normalized)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Invalid JSON/JSONC in {} at line {}, column {}: {}".format(
                path, exc.lineno, exc.colno, exc.msg
            )
        )


def deep_merge(base: Any, local: Any, delete_null: bool) -> Any:
    if isinstance(base, dict) and isinstance(local, dict):
        merged = copy.deepcopy(base)
        for key, local_value in local.items():
            if delete_null and local_value is None:
                merged.pop(key, None)
                continue

            if key in merged:
                merged[key] = deep_merge(merged[key], local_value, delete_null)
            else:
                merged[key] = copy.deepcopy(local_value)
        return merged

    if isinstance(base, list) and isinstance(local, list):
        return copy.deepcopy(local)

    return copy.deepcopy(local)


def write_json(path: Path, data: Any, sort_keys: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=sort_keys)
    path.write_text(content + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Merge base/local JSONC config into generated JSON"
    )
    parser.add_argument("--base", type=Path, required=True, help="Path to base JSONC")
    parser.add_argument("--local", type=Path, required=True, help="Path to local JSONC")
    parser.add_argument("--out", type=Path, required=True, help="Path to output JSON")
    parser.add_argument(
        "--missing-local-ok",
        action="store_true",
        help="If local config is missing, generate from base only",
    )
    parser.add_argument(
        "--delete-null",
        action="store_true",
        help="Treat null in local as delete for object keys",
    )
    parser.add_argument(
        "--sort-keys",
        action="store_true",
        help="Sort JSON keys in output",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.base.exists():
        print("Base config not found: {}".format(args.base), file=sys.stderr)
        return 2

    if args.local.exists():
        local_data = load_jsonc(args.local)
    elif args.missing_local_ok:
        local_data = {}
    else:
        print(
            "Local config not found: {} (pass --missing-local-ok to allow)".format(
                args.local
            ),
            file=sys.stderr,
        )
        return 2

    try:
        base_data = load_jsonc(args.base)
        merged = deep_merge(base_data, local_data, delete_null=args.delete_null)
        write_json(args.out, merged, sort_keys=args.sort_keys)
    except Exception as exc:
        print("Merge failed: {}".format(exc), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
