import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy.orm.query import Query

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. 
  Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization")
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, DELETE")
        return response

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    def get_all_categories():
        result = {}

        for category in Category.query.all():
            result[category.id] = category.type

        return result

    @app.route("/categories")  # Done
    def categories():
        return jsonify({
            "categories": get_all_categories(),
        })

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom
  of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

    @app.route("/questions")  # Done
    def paginated_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        result = questions[start:end]
        if len(result) == 0:
            abort(404)

        return jsonify({
            "questions": [Question.format(question) for question in result],
            "totalQuestions": len(questions),
            "categories": get_all_categories(),
            "currentCategory": "",
        })

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the
  question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

    @app.route("/questions/<int:id>", methods=["DELETE"])  # Done
    def delete_question(id):
        question = Question.query.filter(Question.id == id).one_or_none()
        if question is None:
            abort(404)

        else:

            id = question.id
            question.delete()
            return jsonify({
                "success": True,
                "message": "Question with id={} successfuly deleted".format(id)
            })

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.


  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will 
  appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route("/questions/create", methods=["POST"])  # Done
    def create_question():

        body = request.get_json()
        if body is None:
            abort(400)

        questionText = body.get("question", None)
        answer = body.get("answer", None)
        difficulty = body.get("difficulty", None)
        category = body.get("category", None)

        def noneChecker(value):
            return value is None

        is_not_valid = any([noneChecker(questionText), noneChecker(answer),
                            noneChecker(difficulty), noneChecker(category)])
        if is_not_valid:
            abort(400)
        try:
            question = Question(
                question=questionText, answer=answer, category=category,
                difficulty=difficulty)

            question.insert()

            return jsonify({
                "success": True,
                "message": "Question successfuly created",
            })

        except:
            abort(422)

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route("/questions", methods=["POST"])  # Done
    def get_question():
        body = request.get_json()
        if body is None:
            abort(400)

        search_term = body.get("searchTerm", None)
        if search_term is None:
            abort(400)

        search_res = Question.query.filter(
            Question.question.contains(search_term))

        return jsonify({
            "questions": [Question.format(question)
                          for question in search_res],
            "totalQuestions": len(Question.query.all()),
            "currentCategory": "",
        })

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route("/categories/<category_id>/questions")  # Done
    def questions_for_category(category_id):
        category = Category.query.get_or_404(category_id)

        result = Question.query.filter(Question.category == category_id)

        return jsonify({
            "questions": [Question.format(question) for question in result],
            "totalQuestions": len(Question.query.all()),
            "currentCategory": category.type,
        })
    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

    @app.route("/quizzes", methods=["POST"])  # Done
    def get_quiz_question():
        body = request.get_json()
        if body is None:
            abort(400)

        prevoius_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)
        if prevoius_questions is None or quiz_category is None:
            abort(400)

        # Filter questions based on the selected category
        if quiz_category["id"] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(
                Question.category == quiz_category["id"]).all()

        question_length = len(questions)
        # check if all question has already been visited
        if len(prevoius_questions) == question_length:
            return jsonify({
                "success": True
            })

        rand_question = questions[generate_ranndom_num(question_length-1)]

        while rand_question.id in prevoius_questions:
            rand_question = questions[generate_ranndom_num(question_length)]

        return jsonify({
            "success": True,
            "question": rand_question.format(),
        })

    def generate_ranndom_num(limit):
        return random.randint(0, limit)

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unable to process"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    return app
