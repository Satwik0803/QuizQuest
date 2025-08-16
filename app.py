from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="quiz"
        )
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return None

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

@app.route('/create', methods=['OPTIONS', 'POST'])
def register():
    if request.method == 'OPTIONS':
        return '', 200
    
    db = get_db_connection()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = None
    try:
        data = request.get_json()
        email = data['email']
        username = data['username']
        password = generate_password_hash(data['password'])

        cursor = db.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({"message": "Username already exists"}), 400

        cursor.execute("INSERT INTO users (email, username, password) VALUES (%s, %s, %s)", (email, username, password))
        db.commit()

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        new_user = cursor.fetchone()
        user_id = new_user['id']

       
        return jsonify({"message": "User registered successfully", "user_id": user_id, "username": username}), 200
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/login', methods=['OPTIONS', 'POST'])
def login():
    if request.method == 'OPTIONS':
        return '', 200 
    
    db = get_db_connection()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = None
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid input"}), 400 
        username = data['username']
        password = data['password']

        cursor = db.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            return jsonify({"user_id": user['id'], "username": user['username']}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/reset_password', methods=['POST'])
def reset_password():
    db = get_db_connection()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = None
    try:
        data = request.get_json()
        username = data['username']
        new_password = generate_password_hash(data['password'])

        cursor = db.cursor(dictionary=True)
        cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Username not found"}), 404
        
        return jsonify({"message": "Password updated successfully"}), 200
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/check_username', methods=['GET'])
def check_username():
    username = request.args.get('username')

    if not username:
        return jsonify({'exists': False}), 400

    db = get_db_connection()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            return jsonify({'exists': True}), 200
        else:
            return jsonify({'exists': False}), 404
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


@app.route('/questions', methods=['OPTIONS', 'GET'])
def get_questions():
    if request.method == 'OPTIONS':
        return '', 200
    
    user_id = request.args.get('userId')
    test_id = request.args.get('testId') 

    db = get_db_connection()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = None
    try:
        cursor = db.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT q.*, c.subject, c.quiz_code FROM questions q, course c where q.test_id = c.course_code and test_id= %s", (test_id,))
        questions = cursor.fetchall()
        return jsonify({

            "questions": questions,
            "user_id": user_id,
            "test_id": test_id
        }), 200
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/submit_answer', methods=['OPTIONS','POST'])
def submit_answer():
    if request.method == 'OPTIONS':
        return '', 200 
    
    data = request.get_json()
    user_answer = data.get('answer')
    question_id = data.get('question_id')
    user_id = data.get('user_id')
    test_id = data.get('test_id')
    db = get_db_connection()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = None
    try:
        cursor = db.cursor(dictionary=True , buffered=True)
        cursor.execute("SELECT correct_choice FROM questions WHERE question_id = %s and test_id = %s", (question_id,test_id))
        result = cursor.fetchone()

        if result:
            correct_choice = result['correct_choice']
            is_correct = user_answer == correct_choice
            score = 1 if is_correct else 0
            
            cursor.execute(
                "INSERT INTO answers (test_id, user_id, question_id, user_answer, is_correct) VALUES (%s, %s, %s, %s, %s)",
                (test_id, user_id, question_id, user_answer, is_correct)
            )
            db.commit()

            return jsonify({"score": score}), 200
        else:
            return jsonify({"message": "Question not found"}), 404

    except Exception as e:
        print("Error during answer submission:", str(e))
        return jsonify({"message": "Submission failed", "error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/get_username', methods=['GET'])
def get_username():
    user_id = request.args.get('userId')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()

        if result:
            username = result[0]
            return jsonify({'username': username}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/summary', methods=['GET'])
def get_user_summary():
    user_id = request.args.get('userId')
    subject = request.args.get('subject')  

    if not user_id:
        return jsonify({"error": "userId parameter is required"}), 400

    db = get_db_connection()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = None
    try:
        cursor = db.cursor(dictionary=True, buffered=True)
        
        if subject:  # Query for a specific test ID if provided
            cursor.execute("""
                SELECT COUNT(distinct test_id) AS quizzesAttempted,
                       COALESCE(SUM(is_correct * 100) / (COUNT(distinct test_id) * 10), 0) AS averageScore
                FROM    answers a,course c
                WHERE a.user_id = %s AND a.test_id = c.course_code AND subject = %s
            """, (user_id, subject))
        else:  # Query for all tests if test_id is not provided
            cursor.execute("""
                SELECT COUNT(distinct test_id) AS quizzesAttempted,
                       COALESCE(SUM(is_correct * 100) / (COUNT(distinct test_id) * 10), 0) AS averageScore
                FROM answers 
                WHERE user_id = %s
            """, (user_id,))

        result = cursor.fetchone()
        quizzes_attempted = result['quizzesAttempted'] if result else 0
        average_score = round(result['averageScore'], 2) if result else 0.0

        return jsonify({
            "quizzesAttempted": quizzes_attempted,
            "averageScore": average_score
        }), 200

    except Exception as e:
        print("Error fetching quiz summary:", str(e))
        return jsonify({"message": "Failed to fetch summary", "error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


@app.route('/attempts_and_scores', methods=['GET'])
def get_user_attempts_and_scores():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({"error": "userId parameter is required"}), 400

    db = get_db_connection()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = None
    try:
        cursor = db.cursor(dictionary=True, buffered=True)

        cursor.execute("""SELECT  COUNT(DISTINCT python_tests) AS python_tests_count,COUNT(DISTINCT java_tests) AS java_tests_count,COUNT(DISTINCT cpp_tests) AS cpp_tests_count
                        FROM 
                       ( SELECT 
                        CASE WHEN test_id IN (1, 2) THEN test_id ELSE NULL END AS python_tests,
	                    CASE WHEN test_id IN (3, 4) THEN test_id ELSE NULL END AS java_tests,
	                    CASE WHEN test_id IN (5, 6) THEN test_id ELSE NULL END AS cpp_tests
                        FROM answers
                        WHERE user_id = %s
                        ) AS inner_query
                        """, (user_id,))

        result = cursor.fetchone()
        
        attempts_and_scores = {
            "python": {
                "total": 2,
                "attempted": result['python_tests_count'] if result and result['python_tests_count'] is not None else 0
            },
            "cpp": {
                "total": 2,
                "attempted": result['cpp_tests_count'] if result and result['cpp_tests_count'] is not None else 0
            },
            "java": {
                "total": 2,
                "attempted": result['java_tests_count'] if result and result['java_tests_count'] is not None else 0
            }
        }

        return jsonify(attempts_and_scores), 200

    except Exception as e:
        print("Error fetching quiz attempts and scores:", str(e))
        return jsonify({"message": "Failed to fetch attempts and scores", "error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/quiz_attempted', methods=['GET'])

def quiz_attempted():
    user_id = request.args.get('userId')
    test_id = request.args.get('testId')

    if not user_id or not test_id:
        return jsonify({'error': 'userId and testId are required'}), 400

    db = get_db_connection()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS attempts FROM answers WHERE user_id = %s AND test_id = %s", (user_id, test_id))
        result = cursor.fetchone()

        attempted = result['attempts'] > 0
        return jsonify({'attempted': attempted}), 200

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/course_wise_scores', methods=['GET'])
def get_course_wise_scores():
    user_id = request.args.get('userId')
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Query to get course-wise average scores
    query = """ 
        select subject, max(case when quiz_code = 'Quiz 1' then quiz_score else null end) Quiz1_Score, 
                max(case when quiz_code = 'Quiz 2' then quiz_score else null end) Quiz2_Score,
                sum(quiz_score) / ((case when (max(case when quiz_code = 'Quiz 1' then quiz_score else null end)) is null then 0 else 1 end) + (case when (max(case when quiz_code = 'Quiz 2' then quiz_score else null end)) is null then 0 else 1 end)) AVG_SCORE
        from (SELECT subject, quiz_code, 
                sum(case when a.test_id is null then null when a.test_id is not null and a.is_correct = 1 then 1 else 0 end)*10 quiz_score
              FROM course AS c LEFT JOIN answers AS a ON c.course_code = a.test_id AND a.user_id = %s
              group by subject, quiz_code) as inner_query
               group by subject
               order by case when subject = 'python' then 1 when subject = 'CPP' then 2 else 3 end
        """
    
    cursor.execute(query, (user_id,))
    course_scores = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return jsonify(course_scores)


if __name__ == '__main__':
    app.run(port=5001, debug=True)

