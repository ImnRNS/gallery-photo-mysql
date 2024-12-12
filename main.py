from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

# Muat variabel lingkungan dari file .env
load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'scholarship_db'

mysql = MySQL(app)

if not os.path.exists('static/uploads/'):
    os.makedirs('static/uploads/')

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        file = request.files['file']
        
        if file:
            filename = file.filename
            file_path = os.path.join('static/uploads/', filename)
            file.save(file_path)
            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO images (name, description, filename) VALUES (%s, %s, %s)", (name, description, filename))
            mysql.connection.commit()
            cur.close()
                
            return redirect(url_for('gallery'))

@app.route('/gallery')
def gallery():
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, description, filename FROM images")
    images = cur.fetchall()
    cur.close()
    
    return render_template('gallery.html', images=images)

@app.route('/get_images', methods=['GET'])
def get_images():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, description, filename FROM images")
    images = cur.fetchall()
    cur.close()
    
    images_data = []
    for img in images:
        images_data.append({
            'id': img[0],
            'name': img[1],
            'description': img[2],
            'filename': img[3]
        })
    
    return jsonify(images_data)

if __name__ == '__main__':
    app.run(debug=True)
