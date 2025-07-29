from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from auth import role_required
from model.models import *
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

reg_user = Blueprint("reg_user", __name__)

@reg_user.get("/<string:user_id>/")
@jwt_required()
@role_required("user")
def user_dashboard(user_id):
    quizzes = Quiz.query.all()
    reg_user = User.query.filter_by(user_id=user_id).first_or_404()

    return jsonify({
        'username': reg_user.username,
        'user_id': reg_user.user_id,
        'quizzes': [
            {
                'quiz_id': quiz.quiz_id,
                'chapter_id': quiz.chapter.chapter_id,
                'chapter_name': quiz.chapter.chapter_name,
                'question_count': len(quiz.questions),
                'start_time': quiz.start_time.strftime("%Y-%m-%d %H:%M"),
                'time_duration': quiz.time_duration,
                'remarks': quiz.remarks,
            } for quiz in quizzes
        ]
    })

# Quiz Interface
@reg_user.get("/<string:user_id>/quiz/<string:quiz_id>/start/")
@jwt_required()
@role_required("user")
def quiz(user_id, quiz_id):
    quiz = Quiz.query.filter_by(quiz_id=quiz_id).first_or_404()
    if not quiz:
        return jsonify({'msg': 'Quiz not found'}), 404
    
    now = datetime.now()
    start_time = quiz.start_time
    duration_parts = quiz.time_duration.split(":")
    duration = timedelta(minutes=int(duration_parts[0]), seconds=int(duration_parts[1]))
    end_time = start_time + duration

    if now < start_time:
        return jsonify({"message": "Quiz has not started yet."}), 403
    if now > end_time:
        return jsonify({"message": "Quiz time has expired."}), 403

    return jsonify({
        "quiz_id": quiz.quiz_id,
        "chapter_name": quiz.chapter.chapter_name,
        "start_time": quiz.start_time.strftime("%Y-%m-%d %H:%M"),
        "time_duration": quiz.time_duration,
        "questions": [
            {
                'question_id': question.question_id,
                'question_statement': question.question_statement,
                'question_title': question.question_title,
                'options': [question.option1, question.option2, question.option3, question.option4],
            } for question in quiz.questions
        ]
    })

# Quiz Submission Route
@reg_user.post("/<string:user_id>/quiz/<string:quiz_id>/submit/")
@jwt_required()
@role_required("user")
def scoreboard(user_id, quiz_id):
    data = request.get_json()
    answers = data.get("answers", [])

    total_score = 0
    quiz = Quiz.query.get(quiz_id)

    for question in quiz.questions:
        correct_option_map = {
            "1": question.option1.strip(),
            "2": question.option2.strip(),
            "3": question.option3.strip(),
            "4": question.option4.strip(),
        }

        correct_answer_number = str(question.correct_answer).strip()
        correct_answer_text = correct_option_map.get(correct_answer_number, "").lower()

        # Find matching answer from user
        for answer in answers:
            if str(answer.get("question_id")) == str(question.question_id):
                selected_answer = str(answer.get("selected_answer", "")).strip().lower()
                if selected_answer == correct_answer_text:
                    total_score += 1

    new_score = Score(
        quiz_id=quiz_id,
        user_id=user_id,
        total_scored=total_score
    )
    db.session.add(new_score)
    db.session.commit()

    return jsonify({"message": "Quiz submitted successfully", "total_scored": total_score})

# Quiz Evaluation Route
@reg_user.get("/<string:user_id>/summary/")
@jwt_required()
@role_required("user")
def summary(user_id):
    # reg_user = User.query.filter_by(user_id=user_id).first_or_404()

    # # All attempts by this user
    # attempts = Score.query.filter_by(user_id=user_id).order_by(Score.time_stamp_of_attempt.desc()).all()

    # # latest_attempt = attempts[0]
    # # quiz = Quiz.query.filter_by(quiz_id=latest_attempt.quiz_id).first()

    # # attempt_count = len(attempts)

    # # Calculate time taken for the latest attempt
    # # time_taken = latest_attempt.time_stamp_of_attempt - quiz.start_time

    # for attempt in attempts:
    #     quiz = Quiz.query.filter_by(quiz_id=attempt.quiz_id).first()
    #     time_taken = attempt.time_stamp_of_attempt - quiz.start_time

    # return jsonify({
    #     "attempts": [
    #         {
    #             "score_id": attempt.score_id,
    #             "total_scored": attempt.total_scored,
    #             "submitted_at": attempt.time_stamp_of_attempt.strftime("%Y-%m-%d %H:%M:%S"),
    #             "time_taken": str(time_taken),
    #             "question_count": attempt.quiz.question_count,
    #             "chapter_name": quiz.chapter.chapter_name
    #         }
    #     ]
        
    # })

    reg_user = User.query.filter_by(user_id=user_id).first_or_404()
    attempts = Score.query.filter_by(user_id=user_id).order_by(Score.time_stamp_of_attempt.desc()).all()

    if not attempts:
        return jsonify({"message": "No attempts found"}), 404

    attempt_list = []
    for attempt in attempts:
        quiz = Quiz.query.filter_by(quiz_id=attempt.quiz_id).first()
        time_taken = attempt.time_stamp_of_attempt - quiz.start_time

        attempt_list.append({
            "score_id": attempt.score_id,
            "total_scored": attempt.total_scored,
            "submitted_at": attempt.time_stamp_of_attempt.strftime("%Y-%m-%d %H:%M:%S"),
            "time_taken": str(time_taken),
            "question_count": quiz.question_count,
            "chapter_name": quiz.chapter.chapter_name
        })

    return jsonify({"attempts": attempt_list})
