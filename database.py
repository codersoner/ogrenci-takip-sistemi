import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()


def baglanti_olustur():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER")

    if not server or not database or not driver:
        raise ValueError(
            "Veritabanı ayarları bulunamadı. .env dosyasını kontrol edin."
        )

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(connection_string)