from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "omnitrix.db"

IMAGE_PAIRS = {
    "heatblast": ("chamantes.jpg", "chamadepois.jpg"),
    "four-arms": ("quatroantes.jpg", "quatrobraçosdepois.jpg"),
    "diamondhead": ("diamante.jpg", "diamantedepois.jpg"),
    "xlr8": ("xlantes.jpg", "xlr8depois.jpg"),
    "ghostfreak": ("fantasmaticoantes.jpg", "fantasmaticodepois.jpg"),
    "upgrade": ("ultrantes.jpg", "ultratdepois.jpg"),
    "humungousaur": ("enormoantes.jpg", "enormossaurodepois.jpeg"),
    "rath": ("rathantes.jpg", "rathdepois.jpeg"),
    "wildmutt": ("bestantes.jpg", "bestadepois.jpg"),
    "stinkfly": ("insectoideantes.jpg", "insectoidepois.jpg"),
    "ripjaws": ("aquaticoantes.jpg", "aquaticodepois.jpg"),
    "grey-matter": ("massantes.jpg", "massadepois.jpg"),
}

CLASSIC_ALIENS = [
    {
        "slug": "wildmutt", "name": "Wildmutt", "species": "Vulpimancer", "homeworld": "Vulpin",
        "series": "Ben 10 (Classic)", "first_appearance": "And Then There Were 10", "image": None,
        "description_pt": "Um Vulpimancer quadrúpede que possui sentidos extremamente aguçados e grande capacidade física.",
        "description_en": "A quadrupedal Vulpimancer with extremely sharp senses and great physical ability.",
        "description_es": "Un Vulpimancer cuadrúpedo con sentidos extremadamente agudos y gran capacidad física.",
        "description_fr": "Un Vulpimancer quadrupède doté de sens extrêmement développés et de grandes capacités physiques.",
        "abilities_pt": "Sentidos aguçados|Agilidade|Força|Rastreamento|Garras e presas",
        "abilities_en": "Enhanced senses|Agility|Strength|Tracking|Claws and fangs",
        "abilities_es": "Sentidos agudos|Agilidad|Fuerza|Rastreo|Garras y colmillos",
        "abilities_fr": "Sens aiguisés|Agilité|Force|Pistage|Griffes et crocs",
        "weaknesses_pt": "Não possui visão tradicional|Pode ser afetado por estímulos sensoriais intensos",
        "weaknesses_en": "Lacks conventional eyesight|Can be overwhelmed by intense sensory stimuli",
        "weaknesses_es": "Carece de visión convencional|Puede verse afectado por estímulos sensoriales intensos",
        "weaknesses_fr": "N'a pas de vision conventionnelle|Peut être affecté par des stimuli sensoriels intenses",
    },
    {
        "slug": "grey-matter", "name": "Grey Matter", "species": "Galvan", "homeworld": "Galvan Prime",
        "series": "Ben 10 (Classic)", "first_appearance": "And Then There Were 10", "image": None,
        "description_pt": "Um Galvan pequeno e extremamente inteligente, capaz de analisar e compreender tecnologia complexa.",
        "description_en": "A small and exceptionally intelligent Galvan capable of analyzing and understanding complex technology.",
        "description_es": "Un Galvan pequeño y excepcionalmente inteligente capaz de analizar y comprender tecnología compleja.",
        "description_fr": "Un petit Galvan exceptionnellement intelligent, capable d'analyser et comprendre des technologies complexes.",
        "abilities_pt": "Superinteligência|Análise tecnológica|Agilidade|Escalada|Hackeamento",
        "abilities_en": "Super intelligence|Technological analysis|Agility|Climbing|Hacking",
        "abilities_es": "Superinteligencia|Análisis tecnológico|Agilidad|Escalada|Hackeo",
        "abilities_fr": "Super-intelligence|Analyse technologique|Agilité|Escalade|Piratage",
        "weaknesses_pt": "Baixa força física|Pequeno alcance|Vulnerável a ataques diretos",
        "weaknesses_en": "Low physical strength|Short reach|Vulnerable to direct attacks",
        "weaknesses_es": "Baja fuerza física|Alcance corto|Vulnerable a ataques directos",
        "weaknesses_fr": "Faible force physique|Courte portée|Vulnérable aux attaques directes",
    },
    {
        "slug": "stinkfly", "name": "Stinkfly", "species": "Lepidopterran", "homeworld": "Lepidopterra",
        "series": "Ben 10 (Classic)", "first_appearance": "Permanent Retirement", "image": None,
        "description_pt": "Um Lepidopterran voador que dispara substâncias pegajosas e pode voar em alta velocidade.",
        "description_en": "A flying Lepidopterran that fires sticky substances and can fly at high speed.",
        "description_es": "Un Lepidopterran volador que dispara sustancias pegajosas y puede volar a gran velocidad.",
        "description_fr": "Un Lepidopterran volant qui projette des substances collantes et peut voler à grande vitesse.",
        "abilities_pt": "Voo|Ácido|Jatos de gosma|Agilidade aérea|Força física",
        "abilities_en": "Flight|Acid|Goo jets|Aerial agility|Physical strength",
        "abilities_es": "Vuelo|Ácido|Chorros de baba|Agilidad aérea|Fuerza física",
        "abilities_fr": "Vol|Acide|Jets de bave|Agilité aérienne|Force physique",
        "weaknesses_pt": "Vulnerável a ambientes muito frios|Asas podem ser danificadas",
        "weaknesses_en": "Vulnerable to very cold environments|Wings can be damaged",
        "weaknesses_es": "Vulnerable a ambientes muy fríos|Las alas pueden dañarse",
        "weaknesses_fr": "Vulnérable aux environnements très froids|Les ailes peuvent être endommagées",
    },
    {
        "slug": "ripjaws", "name": "Ripjaws", "species": "Piscciss Volann", "homeworld": "Piscciss",
        "series": "Ben 10 (Classic)", "first_appearance": "And Then There Were 10", "image": None,
        "description_pt": "Um anfíbio predador extremamente adaptado à água, com mandíbulas poderosas e grande velocidade aquática.",
        "description_en": "An amphibious predator highly adapted to water, with powerful jaws and great aquatic speed.",
        "description_es": "Un depredador anfibio muy adaptado al agua, con mandíbulas poderosas y gran velocidad acuática.",
        "description_fr": "Un prédateur amphibie très adapté à l'eau, doté de mâchoires puissantes et d'une grande vitesse aquatique.",
        "abilities_pt": "Respiração aquática|Natação veloz|Mandíbulas poderosas|Mordida|Força",
        "abilities_en": "Aquatic breathing|Fast swimming|Powerful jaws|Bite|Strength",
        "abilities_es": "Respiración acuática|Natación rápida|Mandíbulas poderosas|Mordida|Fuerza",
        "abilities_fr": "Respiration aquatique|Nage rapide|Mâchoires puissantes|Morsure|Force",
        "weaknesses_pt": "Pode desidratar em terra|Menor mobilidade fora da água",
        "weaknesses_en": "Can dehydrate on land|Reduced mobility outside water",
        "weaknesses_es": "Puede deshidratarse en tierra|Menor movilidad fuera del agua",
        "weaknesses_fr": "Peut se déshydrater sur terre|Mobilité réduite hors de l'eau",
    },
]


def ensure_column(conn, column, definition):
    columns = {row[1] for row in conn.execute("PRAGMA table_info(aliens)")}
    if column not in columns:
        conn.execute(f"ALTER TABLE aliens ADD COLUMN {column} {definition}")


def insert_missing_classic(conn):
    columns = {row[1] for row in conn.execute("PRAGMA table_info(aliens)")}
    for alien in CLASSIC_ALIENS:
        existing = conn.execute("SELECT id FROM aliens WHERE slug = ?", (alien["slug"],)).fetchone()
        if existing:
            continue
        values = {key: value for key, value in alien.items() if key in columns}
        cols = ", ".join(values)
        placeholders = ", ".join("?" for _ in values)
        conn.execute(f"INSERT INTO aliens ({cols}) VALUES ({placeholders})", tuple(values.values()))


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Banco não encontrado: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    ensure_column(conn, "selection_image", "TEXT")
    ensure_column(conn, "supreme_image", "TEXT")
    ensure_column(conn, "supreme_selection_image", "TEXT")

    for slug, (selection_image, detail_image) in IMAGE_PAIRS.items():
        conn.execute("UPDATE aliens SET selection_image = ?, image = ? WHERE slug = ?", (selection_image, detail_image, slug))

    conn.execute("UPDATE aliens SET supreme_image = ? WHERE slug = 'humungousaur'", ("enormosupremo.jpg",))
    conn.execute("UPDATE aliens SET supreme_image = ? WHERE slug = 'wildmutt'", ("bestasupremo.jpg",))
    insert_missing_classic(conn)
    conn.commit()

    print("Migração concluída com sucesso.")
    print("\nImagens atuais:")
    for row in conn.execute("SELECT slug, selection_image, image, supreme_selection_image, supreme_image FROM aliens ORDER BY id"):
        print(f"{row[0]}: {row[1]} -> {row[2]} | supremo: {row[3]} -> {row[4]}")

    classic_count = conn.execute("SELECT COUNT(*) FROM aliens WHERE series = 'Ben 10 (Classic)'").fetchone()[0]
    print(f"\nAliens cadastrados na série clássica: {classic_count}")
    conn.close()


if __name__ == "__main__":
    main()
