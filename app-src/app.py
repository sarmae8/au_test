from flask import Flask, render_template, request

app = Flask(__name__)

PORT = 5000


def oblicz_rate_annuitetowa(kwota, lata, oprocentowanie_roczne):
    """Rata stała (annuitetowa)."""
    n = int(lata * 12)  # liczba miesięcy
    r = oprocentowanie_roczne / 100.0 / 12.0  # miesięczna stopa

    if n == 0:
        return None

    if r == 0:  # kredyt 0% ;)
        return kwota / n

    rata = kwota * r * (1 + r) ** n / ((1 + r) ** n - 1)
    return rata


@app.route("/", methods=["GET", "POST"])
def index():
    wynik = None
    błąd = None

    dane_wej = {
        "kwota": "",
        "okres_lat": "",
        "oprocentowanie": ""
    }

    if request.method == "POST":
        try:
            kwota = float(request.form.get("kwota", "0").replace(" ", "").replace(",", "."))
            okres_lat = float(request.form.get("okres_lat", "0").replace(",", "."))
            oprocentowanie = float(request.form.get("oprocentowanie", "0").replace(",", "."))

            dane_wej["kwota"] = kwota
            dane_wej["okres_lat"] = okres_lat
            dane_wej["oprocentowanie"] = oprocentowanie

            rata = oblicz_rate_annuitetowa(kwota, okres_lat, oprocentowanie)

            if rata is None:
                błąd = "Okres kredytowania musi być większy od 0."
            else:
                liczba_rat = int(okres_lat * 12)
                suma_splat = rata * liczba_rat
                odsetki = suma_splat - kwota

                wynik = {
                    "rata_miesieczna": rata,
                    "liczba_rat": liczba_rat,
                    "suma_splat": suma_splat,
                    "odsetki": odsetki,
                    "oprocentowanie": oprocentowanie
                }

        except ValueError:
            błąd = "Nieprawidłowe dane wejściowe."

    return render_template("index.html", wynik=wynik, błąd=błąd, dane=dane_wej)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)
