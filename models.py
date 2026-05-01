from db import get_connection

def add_tea(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO teas (
        name, origin, color, description, aromas,
        smell_rating, taste_rating, temperature, duration,
        container, keywords, technical, personal_notes, status, badges
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


def get_all_teas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teas")
    teas = cursor.fetchall()

    conn.close()
    return teas


def get_tea_by_id(tea_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teas WHERE id=?", (tea_id,))
    tea = cursor.fetchone()

    conn.close()
    return tea


def delete_tea(tea_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM teas WHERE id=?", (tea_id,))
    conn.commit()
    conn.close()

def update_tea(tea_id, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE teas SET
        name=?, origin=?, color=?, description=?, aromas=?,
        smell_rating=?, taste_rating=?, temperature=?, duration=?,
        container=?, keywords=?, technical=?, personal_notes=?, status=?, badges=?
    WHERE id=?
    """, data + (tea_id,))

    conn.commit()
    conn.close()

import random

def smart_random_tea_advanced(query=""):
    teas = get_all_teas()

    query = query.lower()

    results = []

    for tea in teas:
        score = 0

        name = str(tea[1]).lower()
        origin = str(tea[2]).lower()
        color = str(tea[3]).lower()
        aromas = str(tea[5]).lower()
        keywords = str(tea[11]).lower()
        badges = str(tea[15]).lower()

        taste = tea[7]
        smell = tea[8]
        temp = tea[10]

        # --- MATCH TEXTE ---
        if query in name:
            score += 5
        if query in keywords:
            score += 4
        if query in aromas:
            score += 3
        if query in color:
            score += 3

        # --- INTERPRÉTATION INTELLIGENTE ---

        # doux
        if "doux" in query:
            if taste <= 4:
                score += 4

        # corsé / fort
        if "corsé" in query or "fort" in query:
            if taste >= 7:
                score += 4

        # aromatique
        if "aromatique" in query or "parfumé" in query:
            if smell >= 7:
                score += 3

        # léger
        if "léger" in query:
            if taste <= 3:
                score += 3

        # chaud
        if "chaud" in query:
            if temp >= 85:
                score += 2

        # frais
        if "frais" in query:
            if temp <= 75:
                score += 2

        # fruité
        if "fruit" in query:
            if "fruit" in keywords or "fruit" in aromas:
                score += 5

        if score > 0:
            results.append((tea, score))

    if not results:
        return random.choice(teas) if teas else None

    # tri par score
    results.sort(key=lambda x: x[1], reverse=True)

    # top résultats
    best = [t[0] for t in results[:5]]

    return random.choice(best)    