from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "omnitrix.db"
TRANSLATIONS = BASE_DIR / "translations"

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_KEY"

THEMES = {
    "classic": {"name": "Ben 10 Classic", "primary": "#9cff00", "secondary": "#163800"},
    "ben23": {"name": "Ben 23", "primary": "#28a9ff", "secondary": "#06263b"},
    "benirado": {"name": "Ben Irado", "primary": "#ff8c00", "secondary": "#3b1a03"},
    "fantasmatico": {"name": "Fantasmático", "primary": "#b85cff", "secondary": "#170820"},
}

ALIEN_COLLECTIONS = (
    {"slug": "classic", "series": "Ben 10 (Classic)", "title_key": "classic_aliens", "description_key": "classic_aliens_description"},
    {"slug": "alien-force", "series": "Ben 10: Alien Force", "title_key": "alien_force_aliens", "description_key": "alien_force_aliens_description"},
    {"slug": "ultimate-alien", "series": "Ben 10: Ultimate Alien", "title_key": "ultimate_alien_aliens", "description_key": "ultimate_alien_aliens_description"},
    {"slug": "omniverse", "series": "Ben 10: Omniverse", "title_key": "omniverse_aliens", "description_key": "omniverse_aliens_description"},
)

ADDITIONAL_ALIENS = (
    {
        "slug": "humungousaur", "name": "Humungousaur", "species": "Vaxasaurian", "homeworld": "Terradino",
        "series": "Ben 10: Alien Force", "first_appearance": "Ben 10 Returns: Part 1", "image": None,
        "description_pt": "Um Vaxassauriano capaz de aumentar de tamanho e força durante o combate.",
        "description_en": "A Vaxasaurian able to grow in size and strength during combat.",
        "description_es": "Un Vaxasauriano capaz de aumentar su tamaño y fuerza durante el combate.",
        "description_fr": "Un Vaxasaurien capable d'augmenter sa taille et sa force au combat.",
        "abilities_pt": "Superforça|Crescimento corporal|Resistência|Golpes poderosos",
        "abilities_en": "Super strength|Body growth|Durability|Powerful strikes",
        "abilities_es": "Superfuerza|Crecimiento corporal|Resistencia|Golpes poderosos",
        "abilities_fr": "Super-force|Croissance corporelle|Résistance|Coups puissants",
        "weaknesses_pt": "Menor agilidade quando gigante|Alvos pequenos podem ser difíceis de acertar",
        "weaknesses_en": "Less agile when gigantic|Small targets can be difficult to hit",
        "weaknesses_es": "Menor agilidad cuando es gigante|Los objetivos pequeños pueden ser difíciles de golpear",
        "weaknesses_fr": "Moins agile lorsqu'il est géant|Les petites cibles peuvent être difficiles à atteindre",
    },
    {
        "slug": "rath", "name": "Rath", "species": "Appoplexian", "homeworld": "Appoplexia",
        "series": "Ben 10: Alien Force", "first_appearance": "Con of Rath", "image": None,
        "description_pt": "Um Appoplexiano felino extremamente forte, agressivo e especialista em combate corpo a corpo.",
        "description_en": "An exceptionally strong and aggressive feline Appoplexian who excels at hand-to-hand combat.",
        "description_es": "Un Appoplexiano felino extremadamente fuerte y agresivo, experto en combate cuerpo a cuerpo.",
        "description_fr": "Un Appoplexien félin extrêmement fort et agressif, expert du combat au corps à corps.",
        "abilities_pt": "Eu vou te mandar a real|Superforça|Garras afiadas|Agilidade|Combate corpo a corpo",
        "abilities_en": "Let me tell you something|Super strength|Sharp claws|Agility|Hand-to-hand combat",
        "abilities_es": "Déjame decirte algo|Superfuerza|Garras afiladas|Agilidad|Combate cuerpo a cuerpo",
        "abilities_fr": "Laissez-moi vous dire quelque chose|Super-force|Griffes acérées|Agilité|Combat au corps à corps",
        "weaknesses_pt": "Impulsividade|Pode agir sem estratégia",
        "weaknesses_en": "Impulsiveness|Can act without a strategy",
        "weaknesses_es": "Impulsividad|Puede actuar sin estrategia",
        "weaknesses_fr": "Impulsivité|Peut agir sans stratégie",
    },
)

ULTIMATE_FORMS = {
    "humungousaur": {
        "names": {"pt_BR": "Enormossauro Supremo", "en_US": "Ultimate Humungousaur", "es_ES": "Humungosaurio Supremo", "fr_FR": "Enormosaure Suprême"},
        "species": {"pt_BR": "Vaxassauriano Evoluído", "en_US": "Evolved Vaxasaurian", "es_ES": "Vaxasauriano Evolucionado", "fr_FR": "Vaxasaurien évolué"},
        "descriptions": {
            "pt_BR": "Uma evolução de combate do Enormossauro, coberta por armadura pesada e capaz de transformar as mãos em canhões.",
            "en_US": "A combat evolution of Humungousaur, covered in heavy armor and able to turn its hands into cannons.",
            "es_ES": "Una evolución de combate de Humungosaurio, cubierta de armadura pesada y capaz de convertir sus manos en cañones.",
            "fr_FR": "Une évolution de combat d'Enormosaure, couverte d'une armure lourde et capable de transformer ses mains en canons.",
        },
        "abilities": {
            "pt_BR": "Superforça ampliada|Canhões nas mãos|Mísseis de fragmentos ósseos|Armadura reforçada|Cauda com maça",
            "en_US": "Enhanced super strength|Hand cannons|Unstable bone-fragment missiles|Reinforced armor|Mace tail",
            "es_ES": "Superfuerza mejorada|Cañones en las manos|Misiles de fragmentos óseos|Armadura reforzada|Cola con maza",
            "fr_FR": "Super-force accrue|Canons dans les mains|Missiles de fragments osseux|Armure renforcée|Queue en massue",
        },
        "weaknesses": {
            "pt_BR": "Não pode aumentar de tamanho|Menor mobilidade devido à armadura",
            "en_US": "Cannot grow in size|Reduced mobility because of its armor",
            "es_ES": "No puede aumentar de tamaño|Movilidad reducida por su armadura",
            "fr_FR": "Ne peut pas grandir|Mobilité réduite à cause de son armure",
        },
        "series": {
            "pt_BR": "Ben 10: Supremacia Alienígena",
            "en_US": "Ben 10: Ultimate Alien",
            "es_ES": "Ben 10: Supremacía Alienígena",
            "fr_FR": "Ben 10 : Ultimate Alien",
        },
        "first_appearances": {"pt_BR": "A Batalha Final — Parte 1", "en_US": "The Final Battle: Part 1", "es_ES": "La Batalla Final: Parte 1", "fr_FR": "La Bataille Finale : Partie 1"},
        "scenarios": {
            "pt_BR": "A Ultimatrix submeteu o DNA Vaxassauriano a milhões de anos teóricos de batalhas e condições extremas, favorecendo armadura, armas biológicas e força de combate.",
            "en_US": "The Ultimatrix subjected Vaxasaurian DNA to millions of theoretical years of battle and extreme conditions, favoring armor, biological weapons, and combat strength.",
            "es_ES": "La Ultimatrix sometió el ADN Vaxasauriano a millones de años teóricos de batallas y condiciones extremas, favoreciendo armadura, armas biológicas y fuerza de combate.",
            "fr_FR": "L'Ultimatrix a soumis l'ADN vaxasaurien à des millions d'années théoriques de batailles et de conditions extrêmes, favorisant l'armure, les armes biologiques et la force de combat.",
        },
    }
}

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS aliens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        species TEXT NOT NULL,
        homeworld TEXT NOT NULL,
        series TEXT NOT NULL,
        first_appearance TEXT NOT NULL,
        image TEXT,
        description_pt TEXT,
        description_en TEXT,
        description_es TEXT,
        description_fr TEXT,
        abilities_pt TEXT,
        abilities_en TEXT,
        abilities_es TEXT,
        abilities_fr TEXT,
        weaknesses_pt TEXT,
        weaknesses_en TEXT,
        weaknesses_es TEXT,
        weaknesses_fr TEXT
    );
    """)

    count = conn.execute("SELECT COUNT(*) FROM aliens").fetchone()[0]
    if count == 0:
        aliens = [
            {
                "slug":"heatblast","name":"Heatblast","species":"Pyronite","homeworld":"Pyros",
                "series":"Ben 10 (Classic)","first_appearance":"And Then There Were 10",
                "image":"heatblast.svg",
                "description_pt":"Um Pyronite capaz de gerar e controlar fogo e calor.",
                "description_en":"A Pyronite capable of generating and controlling fire and heat.",
                "description_es":"Un Pyronite capaz de generar y controlar fuego y calor.",
                "description_fr":"Un Pyronite capable de générer et contrôler le feu et la chaleur.",
                "abilities_pt":"Pirocinese|Geração de fogo|Manipulação de calor|Projéteis de fogo",
                "abilities_en":"Pyrokinesis|Fire generation|Heat manipulation|Fire projectiles",
                "abilities_es":"Piroquinesis|Generación de fuego|Manipulación del calor|Proyectiles de fuego",
                "abilities_fr":"Pyrokinésie|Génération de feu|Manipulation de la chaleur|Projectiles de feu",
                "weaknesses_pt":"Água|Frio extremo",
                "weaknesses_en":"Water|Extreme cold",
                "weaknesses_es":"Agua|Frío extremo",
                "weaknesses_fr":"Eau|Froid extrême",
            },
            {
                "slug":"four-arms","name":"Four Arms","species":"Tetramand","homeworld":"Khoros",
                "series":"Ben 10 (Classic)","first_appearance":"And Then There Were 10",
                "image":"four-arms.svg",
                "description_pt":"Um Tetramand extremamente forte, com quatro braços e grande resistência física.",
                "description_en":"An extremely strong Tetramand with four arms and great physical endurance.",
                "description_es":"Un Tetramand extremadamente fuerte con cuatro brazos y gran resistencia física.",
                "description_fr":"Un Tetramand extrêmement puissant avec quatre bras et une grande endurance physique.",
                "abilities_pt":"Superforça|Super-resistência|Saltos poderosos|Combate corpo a corpo",
                "abilities_en":"Super strength|Super durability|Powerful jumps|Hand-to-hand combat",
                "abilities_es":"Superfuerza|Superresistencia|Saltos potentes|Combate cuerpo a cuerpo",
                "abilities_fr":"Superforce|Super-résistance|Sauts puissants|Combat au corps à corps",
                "weaknesses_pt":"Menor velocidade|Ataques à distância podem dificultar o combate",
                "weaknesses_en":"Lower speed|Ranged attacks can make combat difficult",
                "weaknesses_es":"Menor velocidad|Los ataques a distancia pueden dificultar el combate",
                "weaknesses_fr":"Vitesse réduite|Les attaques à distance peuvent compliquer le combat",
            },
            {
                "slug":"diamondhead","name":"Diamondhead","species":"Petrosapien","homeworld":"Petropia",
                "series":"Ben 10 (Classic)","first_appearance":"And Then There Were 10",
                "image":"diamondhead.svg",
                "description_pt":"Um Petrosapien capaz de criar e controlar estruturas cristalinas extremamente resistentes.",
                "description_en":"A Petrosapien capable of creating and controlling extremely durable crystal structures.",
                "description_es":"Un Petrosapien capaz de crear y controlar estructuras cristalinas extremadamente resistentes.",
                "description_fr":"Un Petrosapien capable de créer et contrôler des structures cristallines extrêmement résistantes.",
                "abilities_pt":"Construção de cristais|Projéteis cristalinos|Regeneração parcial|Reflexão de energia",
                "abilities_en":"Crystal construction|Crystal projectiles|Partial regeneration|Energy reflection",
                "abilities_es":"Construcción de cristales|Proyectiles cristalinos|Regeneración parcial|Reflexión de energía",
                "abilities_fr":"Création de cristaux|Projectiles cristallins|Régénération partielle|Réflexion d'énergie",
                "weaknesses_pt":"Vibrações e frequências específicas podem afetar estruturas cristalinas",
                "weaknesses_en":"Certain vibrations and frequencies can affect crystal structures",
                "weaknesses_es":"Ciertas vibraciones y frecuencias pueden afectar las estructuras cristalinas",
                "weaknesses_fr":"Certaines vibrations et fréquences peuvent affecter les structures cristallines",
            },
            {
                "slug":"xlr8","name":"XLR8","species":"Kineceleran","homeworld":"Kinet",
                "series":"Ben 10 (Classic)","first_appearance":"And Then There Were 10",
                "image":"xlr8.svg",
                "description_pt":"Um Kineceleran cuja velocidade permite correr em velocidades extraordinárias.",
                "description_en":"A Kineceleran whose speed allows it to move at extraordinary velocities.",
                "description_es":"Un Kineceleran cuya velocidad le permite moverse a velocidades extraordinarias.",
                "description_fr":"Un Kineceleran dont la vitesse lui permet de se déplacer à des vitesses extraordinaires.",
                "abilities_pt":"Supervelocidade|Reflexos acelerados|Movimento em alta velocidade|Redução de atrito",
                "abilities_en":"Super speed|Accelerated reflexes|High-speed movement|Friction reduction",
                "abilities_es":"Supervelocidad|Reflejos acelerados|Movimiento a alta velocidad|Reducción de fricción",
                "abilities_fr":"Super-vitesse|Réflexes accélérés|Déplacement à grande vitesse|Réduction des frottements",
                "weaknesses_pt":"Pode perder vantagem em espaços muito confinados",
                "weaknesses_en":"Can lose its advantage in very confined spaces",
                "weaknesses_es":"Puede perder ventaja en espacios muy reducidos",
                "weaknesses_fr":"Peut perdre son avantage dans les espaces très confinés",
            },
            {
                "slug":"ghostfreak","name":"Ghostfreak","species":"Ectonurite","homeworld":"Anur Phaetos",
                "series":"Ben 10 (Classic)","first_appearance":"Permanent Retirement",
                "image":"ghostfreak.svg",
                "description_pt":"Um Ectonurite capaz de atravessar matéria, ficar invisível e possuir seres vivos.",
                "description_en":"An Ectonurite capable of phasing through matter, becoming invisible, and possessing living beings.",
                "description_es":"Un Ectonurite capaz de atravesar materia, volverse invisible y poseer seres vivos.",
                "description_fr":"Un Ectonurite capable de traverser la matière, devenir invisible et posséder des êtres vivants.",
                "abilities_pt":"Intangibilidade|Invisibilidade|Possessão|Tentáculos|Camuflagem",
                "abilities_en":"Intangibility|Invisibility|Possession|Tentacles|Camouflage",
                "abilities_es":"Intangibilidad|Invisibilidad|Posesión|Tentáculos|Camuflaje",
                "abilities_fr":"Intangibilité|Invisibilité|Possession|Tentacules|Camouflage",
                "weaknesses_pt":"Vulnerabilidade a certas frequências e ao fogo",
                "weaknesses_en":"Vulnerability to certain frequencies and fire",
                "weaknesses_es":"Vulnerabilidad a ciertas frecuencias y al fuego",
                "weaknesses_fr":"Vulnérabilité à certaines fréquences et au feu",
            },
            {
                "slug":"upgrade","name":"Upgrade","species":"Galvanic Mechamorph","homeworld":"Galvan B",
                "series":"Ben 10 (Classic)","first_appearance":"Permanent Retirement",
                "image":"upgrade.svg",
                "description_pt":"Um organismo tecno-orgânico capaz de se fundir e aprimorar máquinas.",
                "description_en":"A techno-organic being capable of merging with and enhancing machines.",
                "description_es":"Un ser tecno-orgánico capaz de fusionarse con máquinas y mejorarlas.",
                "description_fr":"Un être techno-organique capable de fusionner avec des machines et de les améliorer.",
                "abilities_pt":"Tecnoformação|Fusão com tecnologia|Aprimoramento de máquinas|Manipulação tecnológica",
                "abilities_en":"Technokinesis|Technology merging|Machine enhancement|Technological manipulation",
                "abilities_es":"Tecnoquinesis|Fusión tecnológica|Mejora de máquinas|Manipulación tecnológica",
                "abilities_fr":"Technokinésie|Fusion technologique|Amélioration des machines|Manipulation technologique",
                "weaknesses_pt":"Tecnologias incompatíveis ou certos campos de energia",
                "weaknesses_en":"Incompatible technologies or certain energy fields",
                "weaknesses_es":"Tecnologías incompatibles o ciertos campos de energía",
                "weaknesses_fr":"Technologies incompatibles ou certains champs d'énergie",
            },
        ]
        for a in aliens:
            cols = ", ".join(a.keys())
            placeholders = ", ".join(["?"] * len(a))
            conn.execute(f"INSERT INTO aliens ({cols}) VALUES ({placeholders})", tuple(a.values()))
    for alien in ADDITIONAL_ALIENS:
        cols = ", ".join(alien.keys())
        placeholders = ", ".join(["?"] * len(alien))
        conn.execute(
            f"INSERT OR IGNORE INTO aliens ({cols}) VALUES ({placeholders})", tuple(alien.values())
        )
    rath = next(alien for alien in ADDITIONAL_ALIENS if alien["slug"] == "rath")
    conn.execute(
        """UPDATE aliens
        SET abilities_pt = ?, abilities_en = ?, abilities_es = ?, abilities_fr = ?
        WHERE slug = 'rath'""",
        (rath["abilities_pt"], rath["abilities_en"], rath["abilities_es"], rath["abilities_fr"]),
    )
    conn.commit()
    conn.close()

def load_translations(lang):
    path = TRANSLATIONS / f"{lang}.json"
    if not path.exists():
        path = TRANSLATIONS / "pt_BR.json"
    return json.loads(path.read_text(encoding="utf-8"))

@app.context_processor
def inject_globals():
    lang = session.get("lang", "pt_BR")
    theme = session.get("theme", "classic")
    if theme not in THEMES:
        theme = "classic"
    return {
        "t": load_translations(lang),
        "lang": lang,
        "theme": theme,
        "themes": THEMES,
        "user": session.get("username")
    }

@app.route("/")
def index():
    return redirect(url_for("dashboard" if "username" in session else "login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        conn = db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password"], password):
            session["username"] = username
            return redirect(url_for("dashboard"))
        error = "invalid_credentials"
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if len(username) < 3 or len(password) < 4:
            error = "invalid_register"
        else:
            try:
                conn = db()
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                             (username, generate_password_hash(password)))
                conn.commit()
                conn.close()
                session["username"] = username
                return redirect(url_for("dashboard"))
            except sqlite3.IntegrityError:
                error = "user_exists"
    return render_template("register.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    conn = db()
    recent = conn.execute("SELECT * FROM aliens ORDER BY id LIMIT 6").fetchall()
    conn.close()
    return render_template("dashboard.html", recent=recent)

@app.route("/aliens")
def aliens():
    if "username" not in session:
        return redirect(url_for("login"))
    q = request.args.get("q", "").strip()
    if not q:
        conn = db()
        collections = []
        for collection in ALIEN_COLLECTIONS:
            count = conn.execute(
                "SELECT COUNT(*) FROM aliens WHERE series = ?", (collection["series"],)
            ).fetchone()[0]
            collections.append({**collection, "count": count})
        conn.close()
        return render_template("alien_collections.html", collections=collections)

    conn = db()
    rows = conn.execute("""
        SELECT * FROM aliens
        WHERE name LIKE ? OR species LIKE ? OR homeworld LIKE ? OR series LIKE ?
        ORDER BY name
    """, tuple([f"%{q}%"] * 4)).fetchall()
    conn.close()
    return render_template("aliens.html", aliens=rows, q=q, collection=None)

@app.route("/aliens/<collection_slug>")
def aliens_by_collection(collection_slug):
    if "username" not in session:
        return redirect(url_for("login"))

    collection = next((item for item in ALIEN_COLLECTIONS if item["slug"] == collection_slug), None)
    if not collection:
        return "Collection not found", 404

    q = request.args.get("q", "").strip()
    conn = db()
    if q:
        rows = conn.execute("""
            SELECT * FROM aliens
            WHERE series = ? AND (name LIKE ? OR species LIKE ? OR homeworld LIKE ?)
            ORDER BY name
        """, (collection["series"], *([f"%{q}%"] * 3))).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM aliens WHERE series = ? ORDER BY name", (collection["series"],)
        ).fetchall()
    conn.close()
    return render_template("aliens.html", aliens=rows, q=q, collection=collection)

@app.route("/alien/<slug>")
def alien_detail(slug):
    if "username" not in session:
        return redirect(url_for("login"))
    conn = db()
    alien = conn.execute("SELECT * FROM aliens WHERE slug = ?", (slug,)).fetchone()
    conn.close()
    if not alien:
        return "Alien not found", 404
    ultimate_form = ULTIMATE_FORMS.get(slug) if request.args.get("form") == "ultimate" else None
    return render_template("alien.html", alien=alien, ultimate_form=ultimate_form)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        lang = request.form.get("lang", "pt_BR")
        theme = request.form.get("theme", "classic")
        if lang in {"pt_BR", "en_US", "es_ES", "fr_FR"}:
            session["lang"] = lang
        if theme in THEMES:
            session["theme"] = theme
        return redirect(request.referrer or url_for("dashboard"))
    return render_template("settings.html")

@app.route("/api/aliens")
def api_aliens():
    q = request.args.get("q", "").strip()
    conn = db()
    if q:
        rows = conn.execute("SELECT slug, name, species FROM aliens WHERE name LIKE ? OR species LIKE ?",
                            (f"%{q}%", f"%{q}%")).fetchall()
    else:
        rows = conn.execute("SELECT slug, name, species FROM aliens ORDER BY name").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
