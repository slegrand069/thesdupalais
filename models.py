from supabase import create_client

url = "https://ptcsqnskkybxmnsdsdxg.supabase.co"
#anon public
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB0Y3NxbnNra3lieG1uc2RzZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc2Nzc4MzYsImV4cCI6MjA5MzI1MzgzNn0.jcwmddYOVL2DNNPCUEjb3c3l3RWUTLTzagtLDqbTpvw"

supabase = create_client(url, key)


# ---------------- ADD ----------------
def add_tea(data, user_id):

    supabase.table("teas").insert({
        "name": data[0],
        "origin": data[1],
        "color": data[2],
        "description": data[3],
        "aromas": data[4],
        "smell_rating": data[5],
        "taste_rating": data[6],
        "temperature": data[7],
        "duration": data[8],
        "container": data[9],
        "keywords": data[10],
        "technical": data[11],
        "personal_notes": data[12],
        "status": data[13],
        "badges": data[14],
        "user_id": user_id,
        "moment": data[15]
    }).execute()


# ---------------- GET ALL ----------------
def get_teas(user_id):
    response = supabase.table("teas").select("*").eq("user_id", user_id).execute()
    return response.data


# ---------------- GET ONE ----------------
def get_tea_by_id(tea_id, user_id):
    response = supabase.table("teas").select("*").eq("id", tea_id).eq("user_id", user_id).execute()
    return response.data[0] if response.data else None


# ---------------- UPDATE ----------------
def update_tea(tea_id, data, user_id):
    supabase.table("teas").update({
        "name": data[0],
        "origin": data[1],
        "color": data[2],
        "description": data[3],
        "aromas": data[4],
        "smell_rating": data[5],
        "taste_rating": data[6],
        "temperature": data[7],
        "duration": data[8],
        "container": data[9],
        "keywords": data[10],
        "technical": data[11],
        "personal_notes": data[12],
        "status": data[13],
        "badges": data[14],
        "moment": data[15]  
    }).eq("id", tea_id).eq("user_id", user_id).execute()


# ---------------- DELETE ----------------
def delete_tea(tea_id, user_id):
    supabase.table("teas").delete().eq("id", tea_id).eq("user_id", user_id).execute()

# ---------------- CONFIG VALUES ----------------
def get_config_values(config_type):

    response = (
        supabase.table("app_config")
        .select("*")
        .eq("type", config_type)
        .eq("active", True)
        .order("sort_order")
        .execute()
    )

    return response.data

# ---------------- ADD CONFIG VALUE ----------------
def add_config(type_, value):

    return (
        supabase.table("app_config")
        .insert({
            "type": type_,
            "value": value
        })
        .execute()
    )

# ---------------- UPDATE CONFIG VALUE ----------------
def update_config(id_, data):

    return (
        supabase.table("app_config")
        .update(data)
        .eq("id", id_)
        .execute()
    )
