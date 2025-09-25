from flask import Flask, render_template
import os, socket, psutil, psycopg2

app = Flask(__name__)

NFS_PATH = "/mnt/app_data"
DB_HOST = "10.105.16.22"
DB_NAME = "postgres"
DB_USER = "app_user"
DB_PASS = "redhat"

def get_node_info():
    return {
        "node": os.getenv("NODE_NAME", "Unknown"),
        "hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(),
        "mem": psutil.virtual_memory().percent
    }

@app.route("/")
def index():
    return render_template("index.html", result=None, **get_node_info())

@app.route("/health")
def health():
    return render_template("index.html", result="✅ App is healthy", **get_node_info())

@app.route("/nfs")
def nfs_test():
    try:
        test_file = os.path.join(NFS_PATH, "test.txt")
        with open(test_file, "w") as f:
            f.write("NFS test successful")
        with open(test_file, "r") as f:
            content = f.read()
        return render_template("index.html", result=f"✅ NFS Read: {content}", **get_node_info())
    except Exception as e:
        return render_template("index.html", result=f"❌ NFS Error: {str(e)}", **get_node_info())

@app.route("/db")
def db_test():
    try:
        conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return render_template("index.html", result=f"✅ PostgreSQL Version: {version}", **get_node_info())
    except Exception as e:
        return render_template("index.html", result=f"❌ DB Error: {str(e)}", **get_node_info())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

