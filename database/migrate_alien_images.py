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
}


def main():
    conn = sqlite3.connect(DB_PATH)
    columns = {row[1] for row in conn.execute("PRAGMA table_info(aliens)")}

    if "selection_image" not in columns:
        conn.execute("ALTER TABLE aliens ADD COLUMN selection_image TEXT")

    for slug, (selection_image, detail_image) in IMAGE_PAIRS.items():
        conn.execute(
            "UPDATE aliens SET selection_image = ?, image = ? WHERE slug = ?",
            (selection_image, detail_image, slug),
        )

    conn.commit()

    print("Migração concluída.")
    for row in conn.execute(
        "SELECT slug, selection_image, image FROM aliens WHERE slug IN ({}) ORDER BY id".format(
            ",".join("?" for _ in IMAGE_PAIRS)
        ),
        tuple(IMAGE_PAIRS),
    ):
        print(f"{row[0]}: {row[1]} -> {row[2]}")

    conn.close()


if __name__ == "__main__":
    main()
