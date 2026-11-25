import pytest

from turkish_feedback.csv_quality import validate_csv


@pytest.mark.parametrize("encoding", ["utf-8", "utf-8-sig"])
def test_valid_csv(tmp_path, encoding):
    path = tmp_path / "feedback.csv"
    path.write_text(
        'feedback_text,source\n"İyi, hızlı ve güvenli.\nTeşekkürler!",anket\n',
        encoding=encoding,
    )

    assert validate_csv(path) is None


def test_header_only(tmp_path):
    path = tmp_path / "feedback.csv"
    path.write_text("feedback_text\n", encoding="utf-8")

    assert validate_csv(path) is None


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError, match="CSV dosyası bulunamadı"):
        validate_csv(tmp_path / "missing.csv")


@pytest.mark.parametrize(
    ("content", "message"),
    [
        (b"", "CSV dosyası boş"),
        (b"comment\ntext\n", "feedback_text sütunu eksik"),
        (b"feedback_text,source,source\n", "yinelenen sütun adları"),
        (b"feedback_text\n\xff\n", "geçerli UTF-8"),
        (
            b"feedback_text,source\ntext\n",
            "CSV kaydı 2 .*fiziksel satır aralığı 2-2.*2 alan bekleniyordu, 1 bulundu",
        ),
        (
            b'feedback_text\n"first\nrecord"\n"next\nrecord",extra\n',
            "CSV kaydı 3 .*fiziksel satır aralığı 4-5.*1 alan bekleniyordu, 2 bulundu",
        ),
        (
            b'feedback_text\n"first\nrecord"\n"unclosed\nfield',
            "CSV kaydı 3 .*fiziksel satır aralığı 4-5.*CSV biçimi geçersiz",
        ),
    ],
)
def test_invalid_csv(tmp_path, content, message):
    path = tmp_path / "feedback.csv"
    path.write_bytes(content)

    with pytest.raises(ValueError, match=message):
        validate_csv(path)
