from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
import pyrebase
from firebase_config import firebase_config
import requests
import json
from google import genai
from werkzeug.utils import secure_filename
import os
import PIL.Image
import firebase_admin
from firebase_admin import credentials, auth as admin_auth
import pymysql
cred = credentials.Certificate("serviceAccountKey.json")  # Path to your service account JSON
firebase_admin.initialize_app(cred)
from datetime import timedelta




# Initialize Pyrebase for client operations (email/password, etc.)
app = Flask(__name__)
app.secret_key = 'a56a9a3bb10d44b6094601229d98bba69cacca985c1f3a558b21b625319d9f19'  # Use a secure key in production
app.permanent_session_lifetime = timedelta(days=7)
firebase = pyrebase.initialize_app(firebase_config)
pyre_auth = firebase.auth()  # Using Pyrebase for non-social auth

# ========== ROUTES ==========
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

# Initialize Gemini model client
client = genai.Client(api_key="AIzaSyCEn5YfcEEUnKFTRhLYXO-ebLrAmSW6AUE")  # Replace with your actual Gemini API key

# Check allowed file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/set_language', methods=['POST'])
def set_language():
    data = request.get_json()
    session['language'] = data.get('language')
    return jsonify({'status': 'success'})

@app.route('/get_language')
def get_language():
    return jsonify({'language': session.get('language', '')})


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signin-option')
def signin_option():
    return render_template('signin.html')



# MySQL connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='bunny',
        database='edu',
        cursorclass=pymysql.cursors.DictCursor
    )
    
@app.route('/google-log', methods=['POST'])
def google_log():
    try:
        id_token = request.json.get('idToken')
        if not id_token:
            return jsonify({'error': 'Missing ID token'}), 400

        # Verify the token
        decoded_token = admin_auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        email = decoded_token.get('email')

        print(f"Google Sign-in Attempt: {email} (UID: {uid})")

        # Check if email exists in database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_details WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        session['user'] = email

        if user:
            return jsonify({'redirect': url_for('index')})
        else:
            return jsonify({'redirect': url_for('signup')})

    except Exception as e:
        print("Google Login Error:", str(e))
        return jsonify({'error': str(e)}), 400


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get email & password
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("❌ Passwords do not match.")
            return redirect(url_for('signup'))

        # Get other form details directly
        name = request.form.get('name')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        education = request.form.get('education')
        school = request.form.get('school')
        college = request.form.get('college')
        course = request.form.get('course')
        domain = request.form.get('domain')
        skills = request.form.get('skills')

        try:
            # Create Firebase user
            user = pyre_auth.create_user_with_email_and_password(email, password)
            pyre_auth.send_email_verification(user['idToken'])

            # Insert user data into MySQL
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO user_details 
                    (name, gender, phone, education, school, college, course, domain, skills, email) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    name, gender, phone, education, school, college, course, domain, skills, email
                ))
                connection.commit()
            connection.close()

            flash("✅ Verification email sent! Please check your inbox.")
            return redirect(url_for('login'))

        except Exception as e:
            error_message = str(e)
            print("Signup Error:", error_message)
            if "EMAIL_EXISTS" in error_message:
                flash("⚠️ This email is already registered. Please log in.")
                return redirect(url_for('login'))
            else:
                flash("❌ Signup failed. Please try again.")
                return redirect(url_for('signup'))

    return render_template('signup.html')


    
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         try:
#             user = pyre_auth.create_user_with_email_and_password(email, password)
#             pyre_auth.send_email_verification(user['idToken'])
#             flash("✅ Verification email sent! Please check your inbox.")
#             return redirect(url_for('login'))
#         except Exception as e:
#             error_message = str(e)
#             # Check for "EMAIL_EXISTS" from Firebase error
#             if "EMAIL_EXISTS" in error_message:
#                 flash("⚠️ This email is already registered. Please log in.")
#                 return redirect(url_for('login'))
#             else:
#                 flash("❌ Signup failed. Please try again.")
#                 return redirect(url_for('signup'))
#     return render_template('signup.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if email exists in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_details WHERE email = %s", (email,))
        user_in_db = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user_in_db:
            flash("❌ Email not registered. Please sign up first.")
            return redirect(url_for('signup'))

        try:
            user = pyre_auth.sign_in_with_email_and_password(email, password)
            user_info = pyre_auth.get_account_info(user['idToken'])
            verified = user_info['users'][0]['emailVerified']

            if not verified:
                flash("⚠️ Please verify your email before logging in.")
                return redirect(url_for('login'))

            session['user'] = email
            return redirect(url_for('index'))

        except Exception as e:
            flash("❌ INVALID LOGIN CREDENTIALS. Please try again.")
            return redirect(url_for('login'))

    return render_template('login.html')


# -------- Forgot Password --------
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        try:
            pyre_auth.send_password_reset_email(email)
            flash('Password reset link sent to your email.')
        except:
            flash('Error sending reset email. Try again.')
        return redirect(url_for('login'))
    return render_template('forgot-password.html')


@app.route('/google-login', methods=['POST'])
def google_login():
    try:
        id_token = request.json.get('idToken')
        form_data = request.json.get('formData')

        if not id_token:
            return jsonify({'error': 'Missing ID token'}), 400

        decoded_token = admin_auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        email = decoded_token.get('email')

        # Save to session
        session['user'] = email
        print(f"User signed in: {email} (UID: {uid})")

        # Save user data in DB
        name = form_data.get('name')
        gender = form_data.get('gender')
        phone = form_data.get('phone')
        education = form_data.get('education')
        school = form_data.get('school')
        college = form_data.get('college')
        course = form_data.get('course')
        domain = form_data.get('domain')
        skills = form_data.get('skills')

        # Insert into DB
        con=  get_db_connection()
        cur=con.cursor()
        cur.execute("""
            INSERT INTO user_details (email, name, gender, phone, education, school, college, course, domain, skills)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (email, name, gender, phone, education, school, college, course, domain, skills))
        con.commit()
        con.close()

        return jsonify({'redirect': url_for('index')})

    except Exception as e:
        print("Error verifying ID token or saving user:", str(e))
        return jsonify({'error': str(e)}), 400


# # -------- Google Login (Firebase Admin SDK for token verification) --------
# @app.route('/google-login', methods=['POST'])
# def google_login():
#     try:
#         id_token = request.json.get('idToken')
#         if not id_token:
#             return jsonify({'error': 'Missing ID token'}), 400

#         # Verify the token using Firebase Admin SDK
#         decoded_token = admin_auth.verify_id_token(id_token)
#         uid = decoded_token['uid']
#         email = decoded_token.get('email')

#         print(f"User signed in: {email} (UID: {uid})")
#         session['user'] = email

#         return jsonify({'redirect': url_for('index')})
#     except Exception as e:
#         print("Error verifying ID token:", str(e))
#         return jsonify({'error': str(e)}), 400

# -------- Index (Dashboard) --------
@app.route('/index')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user=session['user'])
@app.route('/index/header')
def header():
    return render_template('header.html')

@app.route('/index/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/index/footer')
def footer():
    return render_template('footer.html')

@app.route('/facebook-login', methods=['POST'])
def facebook_login():
    try:
        access_token = request.json.get('accessToken')
        if not access_token:
            return jsonify({'error': 'Missing Facebook access token'}), 400

        # Call Firebase Identity Toolkit API with Facebook access token
        req_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={firebase_config['apiKey']}"
        payload = {
            "postBody": f"access_token={access_token}&providerId=facebook.com",
            "requestUri": "http://localhost",  # This can be a dummy URL
            "returnIdpCredential": True,
            "returnSecureToken": True
        }
        headers = {'Content-Type': 'application/json'}
        res = requests.post(req_url, json=payload, headers=headers)
        res.raise_for_status()
        data = res.json()

        # Extract info from the response
        email = data.get('email')
        name = data.get('displayName', email)
        session['user'] = email
        session['name'] = name

        print(f"Facebook user signed in: {name} ({email})")
        return jsonify({'redirect': url_for('index')})
    except Exception as e:
        print("Error during Facebook login:", str(e))
        return jsonify({'error': str(e)}), 400
# -------- Logout --------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))
#@app.route('/reset-password', methods=["GET", "POST"])
# def reset_password():
#     oob_code = request.args.get("oobCode")
#     mode = request.args.get("mode")
#     print("Reset requested:", oob_code, mode)
#     return render_template('reset-password.html')

# ========== RUN ==========
@app.route('/profile')
def profile():

    email = session['user']
    conn = get_db_connection()
    cursor = conn.cursor()  # Removed dictionary=True to fix the error
    cursor.execute("SELECT * FROM user_details WHERE email = %s", (email,))
    user_data = cursor.fetchone()
    cursor.close()  
    conn.close()

    return render_template('profile.html', user=user_data)


@app.route('/genai')
def genai():
    return render_template('genai.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form.get('prompt')
    image_file = request.files.get('image')
    prompt = f"{prompt} (Respond in {session.get('language', 'English')})"
    
    # Validate image
    #allowed_file(image_file.filename):
    if not image_file :
        image_filename=""
        # return jsonify({'error': 'No valid image provided.'}), 400
    image=""
    # Save the uploaded image
    if image_file:
        image_filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image_file.save(image_path)

    # Open the image using PIL
        image = PIL.Image.open(image_path)

    # Call Gemini AI to process the image and the prompt
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=[prompt, image]
        )
        # Return the response from Gemini AI
        return jsonify({'response': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

from datetime import datetime
@app.route("/message")
def message():
    return render_template('message.html')
@app.route("/get_messages")
def get_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_email, message, timestamp FROM messages ORDER BY timestamp ASC")
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(messages)

# Route to send a message
@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.get_json()
    user_email = session['user']  # Get user email from session
    message = data.get("message")

    if not user_email or not message:
        return jsonify({"error": "Invalid request"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (user_email, message, timestamp) VALUES (%s, %s, %s)",
                   (user_email, message, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"success": True})


@app.route('/youtube')
def youtube():
    return render_template('youtube.html')

import yt_dlp

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is missing"}), 400

    try:
        videos = fetch_youtube_links(query)
        return jsonify({"videos": videos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def fetch_youtube_links(query, num_results=6):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'default_search': 'ytsearch',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch{num_results}:{query}", download=False)
        videos = []
        for entry in info.get("entries", []):
            videos.append({
                "title": entry.get("title"),
                "url": entry.get("url") if "youtube.com" in entry.get("url", "") else f"https://www.youtube.com/watch?v={entry.get('id')}"
            })
        return videos

@app.route('/meet')
def meet():
    return render_template('meet.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

if __name__ == '__main__':
    app.run(debug=True)
