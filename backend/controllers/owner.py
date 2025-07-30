from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from auth import role_required
from model.models import *
from sqlalchemy.exc import IntegrityError
from redis_config import cache

auth_admin = Blueprint("auth_admin", __name__)

@auth_admin.get("/")
@jwt_required()
@role_required("admin")
def admin_dashboard():
    reg_admin = Admin.query.filter_by(role_type='admin').first_or_404()
    subjects = Subject.query.all()

    return jsonify({
        'admin_name': reg_admin.email,
        'subjects': [
            {
                'subject_id': subject.subject_id,
                'subject_name': subject.subject_name,
                'chapters': [
                    {
                        'chapter_id': chapter.chapter_id,
                        'chapter_name': chapter.chapter_name,
                        'question_count': sum([ quiz.question_count for quiz in chapter.quizzes])
                    } for chapter in subject.chapters
                ]
            } for subject in subjects
        ]
    })

# ----------------------------------------------User Management-----------------------------------------------------------------------------
@auth_admin.get("/user_details/")
@jwt_required()
@role_required("admin")
@cache.cached(timeout=180, key_prefix="quiz")
def user_details():
    users = User.query.filter_by(role_type="user").all()
    reg_admin = Admin.query.first_or_404()

    return jsonify({
        'admin_email': reg_admin.email,
        'admin_role': reg_admin.role_type,
        'users': [
            {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'qualification': user.qualification,
                'dob': user.dob.strftime("%a, %d %b %Y"),
                'location': user.location,
                'user_role': user.role_type,
            } for user in users
        ]
    })

# ---------------------------------------------------Subject Management - Create, Read, Update, Delete--------------------------------------
# Add Subject Route
@auth_admin.post("/add_subject/")
@jwt_required()
@role_required("admin")
def add_subject():
    data = request.get_json()
    try:
        new_subject = Subject(
            subject_name = data["subject_name"],
            description = data["description"],
        )
        db.session.add(new_subject)
        db.session.commit()

        return jsonify({
            'msg': 'Subject has added successfully',
            'subject_id': new_subject.subject_id,
        }), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'msg': f'subject already exists.'}), 404
    
# Edit Subject Route
@auth_admin.put("/edit_subject/<string:subject_id>/")
@jwt_required()
@role_required("admin")
def edit_subject(subject_id):
    subject = Subject.query.get(subject_id) # fetch subject by UUID
    if not subject:
        return jsonify({'msg': 'subject not found!!!'}), 404
    
    # data = request.get_json()
    try:
        data = request.get_json()
        subject.subject_name = data.get('subject_name') # update subject name
        subject.description = data.get('description') # update description
        db.session.commit()

        return jsonify({
            'msg': 'Subject has updated successfully',
            'subject_id': subject.subject_id,
            'subject_name': subject.subject_name,
            'description': subject.description,
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({'msg': 'Something Went Wrong!'}), 404
    
# Delete Subject Route
@auth_admin.delete("/delete_subject/<string:subject_id>/")
@jwt_required()
@role_required("admin")
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id) # fetch subject by UUID
    if not subject:
        return jsonify({'msg': 'subject not found!!!'}), 404
    
    db.session.delete(subject)
    db.session.commit()

    return jsonify({'msg': 'Subject Deleted Successfully!'}), 200

# ------------------------------------------Chapter Management - Create Read Update Delete----------------------------------------------------
# Create Chapter Route
@auth_admin.post("/add_chapter/<string:subject_id>/")
@jwt_required()
@role_required("admin")
def add_chapter(subject_id):
    subject = Subject.query.get(subject_id) # fetch subject UUID from subject table to connect with chapter

    data = request.get_json()
    try:
        new_chapter = Chapter(
            chapter_name = data["chapter_name"],
            description = data["description"],
            subject_id = subject.subject_id,
        )
        db.session.add(new_chapter)
        db.session.commit()

        return jsonify({
            'msg': 'Chapter had added Successfully',
            'subject_id': new_chapter.subject_id,
            'chapter_id': new_chapter.chapter_id,
        }), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'msg': 'Chapter already exists!'}), 404
    
# Edit Chapter Route
@auth_admin.put("/edit_chapter/<string:chapter_id>/")
@jwt_required()
@role_required("admin")
def edit_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id) # fetch subject by UUID
    if not chapter:
        return jsonify({'msg': 'Chapter Not Found'}), 404
    
    try:
        data = request.get_json()
        chapter.chapter_name = data.get('chapter_name') # update chapter name
        chapter.description = data.get('description') # update description
        db.session.commit()

        return jsonify({
            'msg': 'Chapter has updated successfully',
            'chapter_id': chapter.chapter_id,
            'chapter_name': chapter.chapter_name,
            'description': chapter.description,
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({'msg': 'Something Went Wrong!'}), 404
    
# Delete Chapter Route
@auth_admin.delete("/delete_chapter/<string:chapter_id>/")
@jwt_required()
@role_required("admin")
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id) # fetch subject by UUID
    if not chapter:
        return jsonify({'msg': 'chapter not found!!!'}), 404
    
    db.session.delete(chapter)
    db.session.commit()

    return jsonify({'msg': 'Chapter Deleted Successfully!'}), 200

# ----------------------------------------Quiz Management - Create Read Update Delete---------------------------------------------
# Quiz Dashboard Management
@auth_admin.get("/quiz_dash/")
@jwt_required()
@role_required("admin")
def quiz_dash():
    quizzes = Quiz.query.all() # fetch all quize info
    return jsonify({
        'quizzes': [
            {
                'quiz_id': quiz.quiz_id,
                'chapter_id': quiz.chapter_id,
                'chapter_name': quiz.chapter.chapter_name if quiz.chapter else "",
                'subject_name': quiz.chapter.subject.subject_name if quiz.chapter and quiz.chapter.subject else "",
                'time_duration': quiz.time_duration,
                'start_time': quiz.start_time.strftime("%Y-%m-%d %H:%M"),
                'remarks': quiz.remarks or "",
                'questions': [
                    {
                        'question_id': question.question_id,
                        'question_title': question.question_title,
                        'question_statement': question.question_statement,
                        'option1': question.option1,
                        'option2': question.option2,
                        'option3': question.option3,
                        'option4': question.option4,
                        'correct_answer': question.correct_answer,
                    } for question in quiz.questions
                ]
            } for quiz in quizzes
        ]
    })

# Add Quiz Route
@auth_admin.post("/add_quiz/")
@jwt_required()
@role_required("admin")
def add_quiz():
    chapters = Chapter.query.all()
    try:
        data = request.get_json()
        new_quiz = Quiz(
            chapter_id = data['chapter_id'],
            start_time = datetime.strptime(data['start_time'], "%Y-%m-%d %H:%M"),
            time_duration = data['time_duration'],
            remarks = data['remarks'],
        )
        db.session.add(new_quiz)
        db.session.commit()
        return jsonify({
            'msg': 'Quiz created successfully.',
            'quiz_id': new_quiz.quiz_id,
            'chapter_id': new_quiz.chapter_id,
        }), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'msg': f'Quiz already exists. Or, Reason: {str(e)}'})
        
# Edit Quiz Route
@auth_admin.put("/edit_quiz/<string:quiz_id>/")
@jwt_required()
@role_required("admin")
def edit_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id) # fetch quiz by UUID
    chapters = Chapter.query.all()
    if not quiz:
        return jsonify({'msg': 'quiz not found'}), 404
    
    try:
        data = request.get_json()
        quiz.chapter_id = data.get('chapter_id') # update chapter UUID
        quiz.time_duration = data.get('time_duration') # update time-span of the quiz
        quiz.start_time = datetime.strptime(data.get('start_time'), "%Y-%m-%d %H:%M") # update time of the quiz
        quiz.remarks = data.get('remarks') # update remarks(optional)
        db.session.commit()

        return jsonify({
            'msg': 'Quiz has updated successfully',
            'chapter_id': quiz.chapter.chapter_id,
            'quiz_id': quiz.quiz_id,
            'time_duration': quiz.time_duration,
            'remarks': quiz.remarks,
            'start_time': quiz.start_time.strftime("%Y-%m-%d %H:%M"),
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Something Went Wrong!', 'error': str(e)}), 500
    
# Delete Quiz Route
@auth_admin.delete("/delete_quiz/<string:quiz_id>/")
@jwt_required()
@role_required("admin")
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id) # fetch quiz by UUID
    if not quiz:
        return jsonify({'msg': 'quiz not found!!!'}), 404
    
    db.session.delete(quiz)
    db.session.commit()

    return jsonify({'msg': 'Quiz Deleted Successfully!'}), 200

# ----------------------------------------------Question Management - Create Read Update Delete------------------------------------------
# Create Question Route
@auth_admin.post("/add_question/<string:quiz_id>/")
@jwt_required()
@role_required("admin")
def add_question(quiz_id):
    quiz = Quiz.query.get(quiz_id) # fetch quiz id from quiz table to connect with question

    
    try:
        data = request.get_json()
        new_question = Question(
            question_statement = data["question_statement"],
            question_title = data["question_title"],
            option1 = data["option1"],
            option2 = data["option2"],
            option3 = data["option3"],
            option4 = data["option4"],
            correct_answer = data["correct_answer"],
            quiz_id = quiz.quiz_id,
        )
        db.session.add(new_question)
        db.session.commit()

        return jsonify({
            'msg': 'Question added Successfully',
            'question_id': new_question.question_id,
            'quiz_id': new_question.quiz_id,
        }), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'msg': 'Question already exists!'}), 404

# Edit Question Route
@auth_admin.put("/edit_question/<string:question_id>/")
@jwt_required()
@role_required("admin")
def edit_question(question_id):
    question = Question.query.get(question_id) # fetch question UUID
    if not question:
        return jsonify({'msg': 'Question Not Found'}), 404
    
    try:
        data = request.get_json()
        question.question_statement = data.get("question_statement")
        question.question_title = data.get("question_title")
        question.option1 = data.get("option1")
        question.option2 = data.get("option2")
        question.option3 = data.get("option3")
        question.option4 = data.get("option4")
        question.correct_answer = data.get("correct_answer")
        db.session.commit()

        return jsonify({
            'msg': 'Question has updated successfully',
            'question_id': question.question_id,
            'question_statement': question.question_statement,
            'question_title': question.question_title,
            'option1': question.option1,
            'option2': question.option2,
            'option3': question.option3,
            'option4': question.option4,
            'correct_answer': question.correct_answer,
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({'msg': 'Something Went Wrong!'}), 404
    
# Delete Question Route
@auth_admin.delete("/delete_question/<string:question_id>/")
@jwt_required()
@role_required("admin")
def delete_question(question_id):
    question = Question.query.get(question_id) # Fetch question by ID
    if not question:
        return jsonify({'msg': 'Question Not Found'}), 404
    
    db.session.delete(question)
    db.session.commit()

    return jsonify({'msg': 'Question deleted successfully'}), 200