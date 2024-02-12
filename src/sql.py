import sqlite3
import json


def table_exists(cur, table_name):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cur.fetchone() is not None

def connect():
    conn = sqlite3.connect("foooxus.db")
    cur = conn.cursor()

    if table_exists(cur, "work"):
        return True

    # Create tables if they don't exist
    cur.execute("CREATE TABLE IF NOT EXISTS work  (uid TEXT PRIMARY KEY, idBatch KEY INT, image TEXT, metadata TEXT, dtGenerated TEXT, elapsedTime FLOAT)")
    cur.execute("CREATE TABLE IF NOT EXISTS batch (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, metadata TEXT, variations TEXT, dtCreated TEXT)")

    # Add some series   
    metadata = {
                    "Prompt":"Portrait of a web programmer man in an office",
                    "Negative Prompt":"",
                    "Styles":"[]",
                    "Performance":"Quality",
                    "Resolution":"(1024, 1024)",
                    "Guidance Scale":"4",
                    "Sharpness":"2",
                    "ADM Guidance":"(1.5, 0.8, 0.3)",
                    "Base Model":"juggernautXL_v8Rundiffusion.safetensors",
                    "Refiner Model":"None",
                    "Refiner Switch":"0.5",
                    "Sampler":"dpmpp_2m_sde_gpu",
                    "Scheduler":"karras",
                    "Seed":"314159"
                } 
    cur.execute("INSERT INTO batch VALUES (1, ?, ?, ?, datetime('now'))", ("Portrait", json.dumps(metadata), "" ))

    metadata = {
                    "Prompt":"Landscape with forest, hills, moutains and river",
                    "Negative Prompt":"",
                    "Styles":"[]",
                    "Performance":"Quality",
                    "Resolution":"(1024, 1024)",
                    "Guidance Scale":"4",
                    "Sharpness":"2",
                    "ADM Guidance":"(1.5, 0.8, 0.3)",
                    "Base Model":"juggernautXL_v8Rundiffusion.safetensors",
                    "Refiner Model":"None",
                    "Refiner Switch":"0.5",
                    "Sampler":"dpmpp_2m_sde_gpu",
                    "Scheduler":"karras",
                    "Seed":"314159"
                } 
    cur.execute("INSERT INTO batch VALUES (2, ?, ?, ?, datetime('now'))", ("Landscape", json.dumps(metadata), "" ))

    conn.commit()
    conn.close()

