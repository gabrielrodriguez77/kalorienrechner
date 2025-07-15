from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = '''
<!doctype html>
<html lang="{{ lang }}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <title>{{ 'Kalorien- & BMI-Rechner für Ernährung & Gesundheit' if lang == 'de' else 'Calorie & BMI Calculator for Nutrition & Health' }}</title>

  <meta name="description" content="{{ 'Kostenloser Kalorienrechner mit BMI-Berechnung und Makronährstoffen. Ideal für Diät, Fitness oder Muskelaufbau – jetzt ausprobieren!' if lang == 'de' else 'Free calorie calculator with BMI and macronutrient calculation. Perfect for diet, fitness or muscle gain – try now!' }}" />
  <meta name="keywords" content="{{ 'Kalorienrechner, BMI Rechner, Ernährung, Diät, Makronährstoffe, Gesundheit, Gewicht verlieren, Fitness' if lang == 'de' else 'calorie calculator, BMI calculator, nutrition, diet, macronutrients, health, weight loss, fitness' }}" />
  <meta name="author" content="Gabriel Rodriguez" />
  <meta name="robots" content="index, follow" />

  <!-- Open Graph / Facebook -->
  <meta property="og:title" content="{{ 'Kalorienrechner & BMI-Tool' if lang == 'de' else 'Calorie & BMI Tool' }}" />
  <meta property="og:description" content="{{ 'Berechne deinen täglichen Kalorienbedarf, BMI und Makronährstoffe. Unterstützt Deutsch & Englisch, Dark/Light Mode & responsives Design.' if lang == 'de' else 'Calculate your daily calories, BMI & macros. Supports English & German, dark/light mode & responsive design.' }}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://kalorienrechner.onrender.com" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{{ 'Kalorienrechner & BMI-Tool' if lang == 'de' else 'Calorie & BMI Tool' }}" />
  <meta name="twitter:description" content="{{ 'Berechne Kalorien, BMI und Makros – einfach & schnell!' if lang == 'de' else 'Calculate calories, BMI and macros – fast & easy!' }}" />

  <!-- Sprache -->
  <meta http-equiv="Content-Language" content="{{ 'de' if lang == 'de' else 'en' }}" />

  <!-- Favicon -->
  <link rel="icon" href="/favicon.ico" type="image/x-icon" />

  <style>
    /* Styles wie oben, responsiv & dark/light Modus */
    :root {
      --bg-light: #f0f4f8;
      --text-light: #333;
      --container-light: #fff;
      --btn-bg-light: #007bff;
      --btn-bg-hover-light: #0056b3;

      --bg-dark: #121212;
      --text-dark: #eee;
      --container-dark: #1e1e1e;
      --btn-bg-dark: #2196f3;
      --btn-bg-hover-dark: #1769aa;
    }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: var(--bg-light);
      color: var(--text-light);
      margin: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      transition: background 0.3s, color 0.3s;
      padding: 10px;
    }
    body.dark {
      background: var(--bg-dark);
      color: var(--text-dark);
    }
    .container {
      background: var(--container-light);
      padding: 30px 40px;
      border-radius: 12px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.1);
      max-width: 400px;
      width: 100%;
      text-align: center;
      transition: background 0.3s, color 0.3s;
    }
    body.dark .container {
      background: var(--container-dark);
    }
    h1 {
      margin-bottom: 20px;
      font-size: 1.8rem;
    }
    label {
      display: block;
      text-align: left;
      margin: 12px 0 6px;
      font-weight: 600;
    }
    input[type="number"], select {
      width: 100%;
      padding: 10px;
      font-size: 1em;
      margin-bottom: 15px;
      border-radius: 6px;
      border: 1px solid #ccc;
      transition: border-color 0.3s;
      box-sizing: border-box;
    }
    input[type="number"]:focus, select:focus {
      outline: none;
      border-color: var(--btn-bg-light);
    }
    body.dark input[type="number"], body.dark select {
      background: #2b2b2b;
      border-color: #555;
      color: var(--text-dark);
    }
    input[type="submit"] {
      background-color: var(--btn-bg-light);
      color: white;
      font-weight: 700;
      padding: 12px 20px;
      font-size: 1.1em;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      width: 100%;
      transition: background-color 0.3s;
      margin-top: 10px;
    }
    input[type="submit"]:hover {
      background-color: var(--btn-bg-hover-light);
    }
    body.dark input[type="submit"] {
      background-color: var(--btn-bg-dark);
    }
    body.dark input[type="submit"]:hover {
      background-color: var(--btn-bg-hover-dark);
    }
    .result {
      margin-top: 25px;
      font-size: 1.3em;
      font-weight: 700;
      color: var(--btn-bg-light);
      word-wrap: break-word;
    }
    body.dark .result {
      color: var(--btn-bg-dark);
    }
    .top-bar {
      position: absolute;
      top: 10px;
      right: 10px;
      display: flex;
      gap: 12px;
      font-weight: 600;
      flex-wrap: wrap;
    }
    .top-bar form {
      margin: 0;
    }
    .top-bar button {
      padding: 6px 12px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      background: var(--btn-bg-light);
      color: white;
      transition: background-color 0.3s;
      font-size: 0.9rem;
    }
    .top-bar button:hover {
      background: var(--btn-bg-hover-light);
    }
    body.dark .top-bar button {
      background: var(--btn-bg-dark);
    }
    body.dark .top-bar button:hover {
      background: var(--btn-bg-hover-dark);
    }
    @media (max-width: 480px) {
      .container {
        padding: 20px 25px;
        max-width: 100%;
      }
      h1 {
        font-size: 1.5rem;
      }
      input[type="number"], select, input[type="submit"] {
        font-size: 1rem;
        padding: 10px;
      }
      .top-bar {
        position: static;
        justify-content: center;
        margin-bottom: 15px;
      }
    }
  </style>
</head>
<body class="{{ 'dark' if theme == 'dark' else '' }}">
  <div class="top-bar">
    <form method="POST" style="display:inline;">
      <input type="hidden" name="theme" value="{{ 'light' if theme == 'dark' else 'dark' }}">
      <input type="hidden" name="lang" value="{{ lang }}">
      <button type="submit">{{ 'Light Mode' if theme == 'dark' else 'Dark Mode' }}</button>
    </form>
    <form method="POST" style="display:inline;">
      <input type="hidden" name="lang" value="{{ 'en' if lang == 'de' else 'de' }}">
      <input type="hidden" name="theme" value="{{ theme }}">
      <button type="submit">{{ 'Deutsch' if lang == 'en' else 'English' }}</button>
    </form>
  </div>
  <div class="container">
    <h1>{{ 'Kalorien- & BMI-Rechner' if lang == 'de' else 'Calorie & BMI Calculator' }}</h1>
    <form method="POST">
      <input type="hidden" name="theme" value="{{ theme }}">
      <input type="hidden" name="lang" value="{{ lang }}">
      <label for="geschlecht">{{ 'Geschlecht' if lang == 'de' else 'Gender' }}</label>
      <select id="geschlecht" name="geschlecht" required>
        <option value="m" {% if form.geschlecht == 'm' %}selected{% endif %}>{{ 'Männlich' if lang == 'de' else 'Male' }}</option>
        <option value="w" {% if form.geschlecht == 'w' %}selected{% endif %}>{{ 'Weiblich' if lang == 'de' else 'Female' }}</option>
        <option value="d" {% if form.geschlecht == 'd' %}selected{% endif %}>{{ 'Divers' if lang == 'de' else 'Other' }}</option>
      </select>

      <label for="alter">{{ 'Alter (Jahre)' if lang == 'de' else 'Age (years)' }}</label>
      <input type="number" id="alter" name="alter" min="10" max="120" required value="{{ form.alter or '' }}">

      <label for="gewicht">{{ 'Gewicht (kg)' if lang == 'de' else 'Weight (kg)' }}</label>
      <input type="number" id="gewicht" name="gewicht" min="20" max="300" step="0.1" required value="{{ form.gewicht or '' }}">

      <label for="groesse">{{ 'Größe (cm)' if lang == 'de' else 'Height (cm)' }}</label>
      <input type="number" id="groesse" name="groesse" min="100" max="250" step="1" required value="{{ form.groesse or '' }}">

      <label for="aktivitaet">{{ 'Aktivität' if lang == 'de' else 'Activity Level' }}</label>
      <select id="aktivitaet" name="aktivitaet" required>
        <option value="1.2" {% if form.aktivitaet == '1.2' %}selected{% endif %}>{{ 'Wenig Bewegung' if lang == 'de' else 'Sedentary' }}</option>
        <option value="1.55" {% if form.aktivitaet == '1.55' %}selected{% endif %}>{{ 'Normal aktiv' if lang == 'de' else 'Moderately active' }}</option>
        <option value="1.9" {% if form.aktivitaet == '1.9' %}selected{% endif %}>{{ 'Sehr aktiv' if lang == 'de' else 'Very active' }}</option>
      </select>

      <label for="ziel">{{ 'Ziel' if lang == 'de' else 'Goal' }}</label>
      <select id="ziel" name="ziel" required>
        <option value="abnehmen" {% if form.ziel == 'abnehmen' %}selected{% endif %}>{{ 'Abnehmen (-300 kcal)' if lang == 'de' else 'Lose weight (-300 kcal)' }}</option>
        <option value="halten" {% if form.ziel == 'halten' %}selected{% endif %}>{{ 'Gewicht halten' if lang == 'de' else 'Maintain weight' }}</option>
        <option value="zunehmen" {% if form.ziel == 'zunehmen' %}selected{% endif %}>{{ 'Zunehmen (+300 kcal)' if lang == 'de' else 'Gain weight (+300 kcal)' }}</option>
      </select>

      <input type="submit" value="{{ 'Berechnen' if lang == 'de' else 'Calculate' }}">
    </form>

    {% if kalorien %}
      <div class="result">
        {{ 'Dein täglicher Kalorienbedarf:' if lang == 'de' else 'Your daily calorie need:' }} {{ kalorien }} kcal
      </div>
      <div class="result">
        {{ 'Dein BMI:' if lang == 'de' else 'Your BMI:' }} {{ bmi }}
      </div>
      <div class="result">
        {{ 'Makronährstoffe (g/Tag):' if lang == 'de' else 'Macronutrients (g/day):' }}
        <br />
        {{ 'Protein:' if lang == 'de' else 'Protein:' }} {{ protein }}g,  
        {{ 'Fett:' if lang == 'de' else 'Fat:' }} {{ fett }}g,  
        {{ 'Kohlenhydrate:' if lang == 'de' else 'Carbohydrates:' }} {{ kohlenhydrate }}g
      </div>
    {% endif %}
  </div>
</body>
</html>
'''

def calculate_macros(calories, weight):
    protein = round(weight * 2)
    fett = round(weight * 1)
    rest_kcal = calories - (protein * 4 + fett * 9)
    kohlenhydrate = round(rest_kcal / 4) if rest_kcal > 0 else 0
    return protein, fett, kohlenhydrate

@app.route("/", methods=["GET", "POST"])
def home():
    theme = 'light'
    lang = 'de'
    form = {}
    kalorien = None
    bmi = None
    protein = fett = kohlenhydrate = None

    if request.method == "POST":
        theme = request.form.get('theme', 'light')
        lang = request.form.get('lang', 'de')

        form['geschlecht'] = request.form.get('geschlecht')
        form['alter'] = request.form.get('alter')
        form['gewicht'] = request.form.get('gewicht')
        form['groesse'] = request.form.get('groesse')
        form['aktivitaet'] = request.form.get('aktivitaet')
        form['ziel'] = request.form.get('ziel')

        if all(form.values()):
            try:
                geschlecht = form['geschlecht']
                alter = int(form['alter'])
                gewicht = float(form['gewicht'])
                groesse = float(form['groesse'])
                aktivitaet = float(form['aktivitaet'])
                ziel = form['ziel']

                if geschlecht == 'm':
                    grundumsatz = 66 + (13.7 * gewicht) + (5 * groesse) - (6.8 * alter)
                elif geschlecht == 'w':
                    grundumsatz = 655 + (9.6 * gewicht) + (1.8 * groesse) - (4.7 * alter)
                else:
                    grundumsatz = 1500

                gesamtbedarf = grundumsatz * aktivitaet

                if ziel == 'abnehmen':
                    gesamtbedarf -= 300
                elif ziel == 'zunehmen':
                    gesamtbedarf += 300

                kalorien = round(gesamtbedarf)
                bmi = round(gewicht / ((groesse / 100) ** 2), 1)
                protein, fett, kohlenhydrate = calculate_macros(kalorien, gewicht)
            except Exception:
                pass

    return render_template_string(HTML, theme=theme, lang=lang, form=form, kalorien=kalorien, bmi=bmi, protein=protein, fett=fett, kohlenhydrate=kohlenhydrate)

if __name__ == "__main__":
    app.run(debug=True)

