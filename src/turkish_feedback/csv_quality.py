"""Validate the structure of feedback CSV files."""

import csv
from pathlib import Path


def validate_csv(path: str | Path) -> None:
    """Raise an exception if the file does not meet the feedback CSV schema."""
    path = Path(path)
    try:
        with path.open(encoding="utf-8-sig", newline="") as source:
            reader = csv.reader(source, delimiter=",", strict=True)
            record_number = 1
            first_line = 1
            try:
                header = next(reader, None)
                if not header:
                    raise ValueError(f"{path}: CSV dosyası boş veya başlık satırı boş.")
                if len(header) != len(set(header)):
                    raise ValueError(f"{path}: CSV başlığında yinelenen sütun adları var.")
                if "feedback_text" not in header:
                    raise ValueError(f"{path}: Zorunlu feedback_text sütunu eksik.")

                while True:
                    record_number += 1
                    first_line = reader.line_num + 1
                    row = next(reader, None)
                    if row is None:
                        break
                    if len(row) != len(header):
                        raise ValueError(
                            f"{path}: CSV kaydı {record_number} "
                            f"(fiziksel satır aralığı {first_line}-{reader.line_num}) "
                            f"için {len(header)} alan bekleniyordu, {len(row)} bulundu."
                        )
            except csv.Error as error:
                raise ValueError(
                    f"{path}: CSV kaydı {record_number} "
                    f"(fiziksel satır aralığı {first_line}-{reader.line_num}) "
                    f"okunamadı. CSV biçimi geçersiz. ({error})"
                ) from error
    except FileNotFoundError as error:
        raise FileNotFoundError(f"{path}: CSV dosyası bulunamadı.") from error
    except UnicodeDecodeError as error:
        raise ValueError(f"{path}: CSV dosyası geçerli UTF-8 içermiyor.") from error
