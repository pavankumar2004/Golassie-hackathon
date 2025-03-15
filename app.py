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

    # Updated query to match new schema
    cursor.execute("""
        SELECT 
            pd.payer_detail_id,
            p.payer_id,
            pd.payer_name,
            pd.short_name,
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
    
    try:
        if request.method == 'POST':
            payer_name = request.form.get('payer_name')
            short_name = request.form.get('short_name')
            tax_id = request.form.get('tax_id')
            
            if not payer_name:
                raise ValueError("Payer name is required")
                
            cursor.execute("""
                UPDATE payer_details 
                SET payer_name = %s, short_name = %s, tax_id = %s 
                WHERE payer_detail_id = %s
                RETURNING *;
            """, (payer_name, short_name, tax_id, payer_detail_id))
            
            updated_record = cursor.fetchone()
            if not updated_record:
                raise ValueError(f"No payer detail found with ID {payer_detail_id}")
                
            conn.commit()
            return redirect(url_for('payer_details'))
        
        # GET request
        cursor.execute("""
            SELECT 
                pd.payer_detail_id,
                p.payer_id,
                pd.payer_name,
                pd.short_name,
                pd.tax_id,
                pg.payer_group_name
            FROM payer_details pd
            JOIN payers p ON pd.payer_id = p.payer_id
            JOIN payer_groups pg ON p.payer_group_id = pg.payer_group_id
            WHERE pd.payer_detail_id = %s;
        """, (payer_detail_id,))
        
        payer_detail = cursor.fetchone()
        if not payer_detail:
            return f"Payer detail with ID {payer_detail_id} not found", 404
            
        return render_template('edit_payer_detail.html', payer_detail=payer_detail)
        
    except ValueError as e:
        return str(e), 400
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
    finally:
        cursor.close()
        conn.close()

@app.route('/payers')
def payers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            p.payer_id,
            p.payer_name,
            pg.payer_group_name
        FROM payers p
        JOIN payer_groups pg ON p.payer_group_id = pg.payer_group_id;
    """)
    payers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('payers.html', payers=payers)

@app.route('/hierarchy')
def hierarchy():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get payer groups with their payers
    cursor.execute("""
        SELECT 
            pg.payer_group_id,
            pg.payer_group_name,
            array_agg(json_build_object(
                'payer_id', p.payer_id,
                'payer_name', p.payer_name
            )) as payers
        FROM payer_groups pg
        LEFT JOIN payers p ON pg.payer_group_id = p.payer_group_id
        GROUP BY pg.payer_group_id, pg.payer_group_name
        ORDER BY pg.payer_group_name;
    """)
    
    payer_groups = []
    for row in cursor.fetchall():
        group = {
            'payer_group_id': row[0],
            'payer_group_name': row[1],
            'payers': row[2] if row[2][0] is not None else []
        }
        payer_groups.append(group)
    
    cursor.close()
    conn.close()
    return render_template('hierarchy.html', payer_groups=payer_groups)

if __name__ == '__main__':
    app.run(debug=True)
