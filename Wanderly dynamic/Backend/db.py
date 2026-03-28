import psycopg2

def get_connection():
    connection = psycopg2.connect(
        "postgresql://postgres.tlnfyknlctwxlzfqmddm:Wanderly%405398@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres"
    )
    return connection
    