import pyodbc


def baglanti_olustur():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=LAPTOP-T2T6K43U;"
        "DATABASE=OgrenciTakipDB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )