import socket, psycopg2

pwd = "jpsKrXhC1V7Fn20P"
refs = ["kxyxhmkcktqkjhcdofki", "sumhxcjrwfjsjnojslrp"]

# Solo probar us-east-1 para rapidez (todos resuelven)
host = "aws-0-us-east-1.pooler.supabase.com"

for ref in refs:
    for port in [6543, 5432]:
        label = "Session" if port == 6543 else "Transaction"
        url = f"postgresql://postgres.{ref}:{pwd}@{host}:{port}/postgres?sslmode=require&connect_timeout=5"
        try:
            conn = psycopg2.connect(url)
            print(f"CONECTADO [{label}:{port}] ref={ref} host={host}")
            conn.close()
        except psycopg2.OperationalError as e:
            print(f"FAIL [{label}:{port}] ref={ref}: {str(e).strip()[:150]}")

# Tambien probar formato antiguo (sin ref en usuario) con direct host conocido
print("\n=== Verificando API REST de Supabase ===")
import urllib.request, json
for ref2 in refs:
    try:
        url2 = f"https://{ref2}.supabase.co/rest/v1/"
        req = urllib.request.Request(url2, headers={"apikey": "anon"})
        with urllib.request.urlopen(req, timeout=5) as r:
            print(f"REST OK {ref2}: {r.status}")
    except Exception as e:
        print(f"REST {ref2}: {str(e)[:80]}")
