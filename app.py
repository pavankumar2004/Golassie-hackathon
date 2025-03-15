from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Database connection setup
DATABASE_URL = "postgresql://postgres:golassie@db.cbgtocxhyfflpmaxbugd.supabase.co:5432/postgres"

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/payer_groups')
def payer_groups():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payer_groups;")
    payer_groups = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('payer_groups.html', payer_groups=payer_groups)

@app.route('/payer_groups/add', methods=['GET', 'POST'])
def add_payer_group():
    if request.method == 'POST':
        payer_group_name = request.form['payer_group_name']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO payer_groups (payer_group_name) VALUES (%s);", (payer_group_name,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('payer_groups'))
    return render_template('add_payer_group.html')

@app.route('/payer_details')
def payer_details():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Updated query to join payer_groups table
    cursor.execute("""
        SELECT 
            pd.payer_detail_id, 
            p.payer_name, 
            p.payer_number, 
            pd.payer_name AS detail_name, 
            pd.tax_id, 
            pg.payer_group_name, 
            pg.payer_group_id
        FROM payer_details pd
        JOIN payers p ON pd.payer_id = p.payer_id
        JOIN payer_groups pg ON p.payer_group_id = pg.payer_group_id;
    """)

    payer_details = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('payer_details.html', payer_details=payer_details)


@app.route('/payer_details/edit/<int:payer_detail_id>', methods=['GET', 'POST'])
def edit_payer_detail(payer_detail_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        payer_name = request.form['payer_name']
        payer_number = request.form['payer_number']
        tax_id = request.form['tax_id']
        cursor.execute("""
            UPDATE payer_details 
            SET payer_name = %s, payer_number = %s, tax_id = %s 
            WHERE payer_detail_id = %s;
        """, (payer_name, payer_number, tax_id, payer_detail_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('payer_details'))
    
    cursor.execute("SELECT * FROM payer_details WHERE payer_detail_id = %s;", (payer_detail_id,))
    payer_detail = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_payer_detail.html', payer_detail=payer_detail)

if __name__ == '__main__':
    app.run(debug=True)
