import socket, subprocess, urllib.request, json

ref_new = "kxyxhmkcktqkjhcdofki"
ref_old = "sumhxcjrwfjsjnojslrp"
key = "sb_publishable_DCBMvFSxEgOpWre6WcQW5A_nhXtjlIp"
pwd = "jpsKrXhC1V7Fn20P"

# 1. Check IPv6 for direct host
print("=== IPv6 DNS check ===")
for ref in [ref_new, ref_old]:
    host = f"db.{ref}.supabase.co"
    try:
        addrs = socket.getaddrinfo(host, 5432)
        for fam, typ, proto, canon, sa in addrs:
            print(f"{host} -> {sa}")
    except Exception as e:
        print(f"{host} -> FAIL: {e}")

# 2. REST API con la key real
print("\n=== REST API test ===")
for ref in [ref_new, ref_old]:
    try:
        url = f"https://{ref}.supabase.co/rest/v1/"
        req = urllib.request.Request(url, headers={"apikey": key, "Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=8) as r:
            body = r.read().decode()[:200]
            print(f"REST {ref}: {r.status} -> {body}")
    except urllib.request.HTTPError as e:
        body = e.read().decode()[:200]
        print(f"REST {ref}: HTTP {e.code} -> {body}")
    except Exception as e:
        print(f"REST {ref}: {e}")

# 3. Intentar conexion directa con IPv6 forzado (via getaddrinfo)
print("\n=== Direct connect via IPv6 ===")
import psycopg2
for ref in [ref_new, ref_old]:
    host = f"db.{ref}.supabase.co"
    try:
        addrs = socket.getaddrinfo(host, 5432, socket.AF_INET6)
        if addrs:
            ipv6 = addrs[0][4][0]
            url = f"postgresql://postgres:{pwd}@[{ipv6}]:5432/postgres?sslmode=require&connect_timeout=5"
            print(f"Intentando IPv6 {ipv6} para {ref}...")
            conn = psycopg2.connect(url)
            print(f"CONECTADO IPv6 para {ref}!")
            conn.close()
    except socket.gaierror as e:
        print(f"No IPv6 para {host}: {e}")
    except psycopg2.OperationalError as e:
        print(f"IPv6 connect FAIL {ref}: {str(e)[:120]}")
