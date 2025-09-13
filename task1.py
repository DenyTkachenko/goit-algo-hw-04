from __future__ import annotations

import argparse
import shutil
from pathlib import Path

def iter_files_recursive(root: Path):
    for entry in root.iterdir():
        try:
            is_dir = entry.is_dir()
        except OSError:
            continue
        if is_dir:
            yield from iter_files_recursive(entry)
        else:
            yield entry

def ext_folder_name(p: Path) -> str:
    ext = p.suffix.lower().lstrip(".")
    return ext if ext else "_no_ext"

def sort_copy(src: Path, dst: Path, dry_run: bool = False, verbose: bool = False) -> int:
    if not src.exists() or not src.is_dir():
        raise ValueError(f"Вихідна директорія не існує або не є папкою: {src}")
    dst_resolved = dst.resolve()
    copied = 0
    for f in iter_files_recursive(src):
        try:
            try:
                if dst_resolved in f.resolve().parents:
                    if verbose:
                        print(f"[SKIP ] {f} (знаходиться у DEST)")
                    continue
            except OSError:
                if verbose:
                    print(f"[WARN ] Не вдалося resolve(): {f}")
                continue
            folder = ext_folder_name(f)
            target_dir = dst / folder
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / f.name
            if verbose or dry_run:
                print(f"[COPY ] {f} -> {target}")
            if not dry_run:
                shutil.copy2(f, target)
                copied += 1
        except (PermissionError, OSError, shutil.SameFileError) as e:
            print(f"[ERROR] {f}: {e}")
            continue
    return copied

def main():
    parser = argparse.ArgumentParser(description="Рекурсивне сортування файлів за розширенням (копіювання у DEST).")
    parser.add_argument("src", type=Path, help="Вихідна директорія (SRC)")
    parser.add_argument("dst", type=Path, nargs="?", help="Директорія призначення (DEST). Типово SRC/../dist")
    parser.add_argument("--dry-run", action="store_true", help="Лише показати дії без копіювання")
    parser.add_argument("--verbose", action="store_true", help="Докладний вивід")
    args = parser.parse_args()
    src: Path = args.src
    dst: Path = args.dst if args.dst else (src.parent / "dist")
    print(f"SRC: {src}")
    print(f"DEST: {dst}")
    try:
        copied = sort_copy(src, dst, dry_run=args.dry_run, verbose=args.verbose)
        print(f"Готово. Скопійовано файлів: {copied}")
    except ValueError as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    main()
