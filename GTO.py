from flask import Flask, render_template, request, redirect, url_for, session
import matplotlib.pyplot as plt
import os
import random

app = Flask(__name__)
app.secret_key = 'tajny_klic'  # nastav pro session

@app.route('/')
def index():
    session.clear()
    session['score_1'] = 0
    session['score_2'] = 0
    session['tah'] = 0
    session['prubeh_1'] = []
    session['prubeh_2'] = []
    session['log'] = []
    session['zaznamy'] = {
        'spoluprace': 0,
        'uspesna_zrada_hrace_1': 0,
        'uspesna_zrada_hrace_2': 0,
        'nespoluprace': 0,
        'zrada_1': 0,
        'zrada_2': 0,
        'spoluprace_1': 0,
        'spoluprace_2': 0
    }
    session['volba_2'] = 'S'
    return render_template('index.html')

@app.route('/tah', methods=['POST'])
def tah():
    if session['tah'] >= 10:
        return redirect(url_for('vysledek'))

    volba_1 = request.form.get('volba')
    if volba_1 not in ['S', 'Z']:
        return redirect(url_for('index'))

    tah = session['tah']
    volba_2 = session['volba_2']
    if tah > 0:
        if random.random() < 0.1:
            volba_2 = 'Z' if session['volba_2'] == 'S' else 'S'
        else:
            volba_2 = volba_1
    session['volba_2'] = volba_2

    s = session['zaznamy']

    if volba_1 == 'S' and volba_2 == 'S':
        session['score_1'] += 3
        session['score_2'] += 3
        s['spoluprace'] += 1
        s['zrada_2'] += 1
        s['spoluprace_1'] += 1
        s['spoluprace_2'] += 1
        zprava = "Oba spolupracovali."
    elif volba_1 == 'S' and volba_2 == 'Z':
        session['score_2'] += 5
        s['uspesna_zrada_hrace_2'] += 1
        s['zrada_2'] += 1
        s['spoluprace_1'] += 1
        zprava = "Hráč 2 tě zradil."
    elif volba_1 == 'Z' and volba_2 == 'S':
        session['score_1'] += 5
        s['uspesna_zrada_hrace_1'] += 1
        s['zrada_1'] += 1
        s['spoluprace_2'] += 1
        zprava = "Zradil jsi hráče 2."
    else:
        session['score_1'] += 1
        session['score_2'] += 1
        s['nespoluprace'] += 1
        s['zrada_1'] += 1
        s['zrada_2'] += 1
        zprava = "Oba zradili."

    session['prubeh_1'].append(session['score_1'])
    session['prubeh_2'].append(session['score_2'])
    session['log'].append((tah + 1, volba_1, volba_2, zprava))
    session['tah'] += 1

    return redirect(url_for('index'))

@app.route('/vysledek')
def vysledek():
    tahy = 10
    s = session['zaznamy']

    def pct(x): return round(x / tahy * 100)

    fig, ax = plt.subplots()
    ax.plot(session['prubeh_1'], label="Hráč 1", color="blue")
    ax.plot(session['prubeh_2'], label="Hráč 2", color="red")
    ax.set_xlabel("Tah")
    ax.set_ylabel("Skóre")
    ax.set_title("Vývoj skóre")
    ax.legend()
    ax.grid(True)

    path = os.path.join('static', 'graf.png')
    fig.savefig(path)
    plt.close()

    return render_template('vysledek.html', zaznamy=s, tahy=tahy, path=path,
                           score_1=session['score_1'], score_2=session['score_2'])

if __name__ == '__main__':
    app.run(debug=True)
