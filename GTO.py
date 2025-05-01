from flask import Flask, render_template, request
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hra():
    vysledky_text = ""
    matice_text = ""
    img_data = ""

    if request.method == "POST":
        score_hrace_1 = 0
        score_hrace_2 = 0
        spoluprace = 0
        uspesna_zrada_hrace_1 = 0
        uspesna_zrada_hrace_2 = 0
        nespoluprace = 0
        zrada_1 = 0
        zrada_2 = 0
        spoluprace_1 = 0
        spoluprace_2 = 0
        tahy = 10
        prubeh_1 = []
        prubeh_2 = []
        volba_hrace_2 = "S"

        for tah in range(tahy):
            volba_hrace_1 = random.choice(["S", "Z"])
            minula_volba_hrace_1 = volba_hrace_1
            if tah > 0:
                volba_hrace_2 = minula_volba_hrace_1
                if random.random() < 0.1:
                    volba_hrace_2 = "S" if volba_hrace_1 == "Z" else "Z"

            if volba_hrace_1 == "S" and volba_hrace_2 == "S":
                score_hrace_1 += 3
                score_hrace_2 += 3
                spoluprace += 1
                zrada_2 += 1
                spoluprace_1 += 1
            elif volba_hrace_1 == "S" and volba_hrace_2 == "Z":
                score_hrace_2 += 5
                uspesna_zrada_hrace_2 += 1
                zrada_2 += 1
                spoluprace_1 += 1
            elif volba_hrace_1 == "Z" and volba_hrace_2 == "S":
                score_hrace_1 += 5
                uspesna_zrada_hrace_1 += 1
                zrada_1 += 1
                spoluprace_2 += 1
            else:
                score_hrace_1 += 1
                score_hrace_2 += 1
                nespoluprace += 1
                zrada_1 += 1
                zrada_2 += 1

            prubeh_1.append(score_hrace_1)
            prubeh_2.append(score_hrace_2)

        def pct(x): return f"{round(x / tahy * 100)} %"

        vysledky_text = (
            f"Skóre po {tahy} tazích:<br><br>"
            f"Hráč 1: {score_hrace_1} bodů<br>"
            f"Hráč 2: {score_hrace_2} bodů<br>"
            f"Suma bodů: {score_hrace_1 + score_hrace_2}<br><br>"
        )
        if score_hrace_1 > score_hrace_2:
            vysledky_text += "Hráč 1 vyhrál!<br>"
        elif score_hrace_1 < score_hrace_2:
            vysledky_text += "Hráč 2 vyhrál!<br>"
        else:
            vysledky_text += "Je to remíza!<br>"

        matice_text = (
            f"<pre>{'':15}| {'Hráč 2: S':>10} | {'Hráč 2: Z':>10} | {'Součet':>10}\n"
            f"{'-'*52}\n"
            f"{'Hráč 1: S':15}| {pct(spoluprace):>10} | {pct(uspesna_zrada_hrace_2):>10} | {pct(spoluprace_1):>10}\n"
            f"{'Hráč 1: Z':15}| {pct(uspesna_zrada_hrace_1):>10} | {pct(nespoluprace):>10} | {pct(zrada_1):>10}\n"
            f"{'-'*52}\n"
            f"{'Součet':15}| {pct(spoluprace_2):>10} | {pct(zrada_2):>10} | {'100 %':>10}</pre>"
        )

        fig, ax = plt.subplots(figsize=(9, 4))
        ax.plot(prubeh_1, label="Hráč 1", color="blue")
        ax.plot(prubeh_2, label="Hráč 2", color="red")
        ax.set_xlabel("Tah")
        ax.set_ylabel("Skóre")
        ax.set_title("Vývoj skóre hráčů")
        ax.legend()
        ax.grid(True)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_data = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

    return render_template("index.html", vysledky=vysledky_text, matice=matice_text, graf=img_data)

if __name__ == "__main__":
    app.run(debug=True)
