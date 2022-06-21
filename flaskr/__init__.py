from crypt import methods
import dbm
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )    
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    def paginate_categories(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page -1) * QUESTIONS_PER_PAGE 
        end = start + QUESTIONS_PER_PAGE

        categories = [cat.format() for cat in selection]
        current_category = categories[start:end]

        return current_category

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page -1) * QUESTIONS_PER_PAGE 
        end = start + QUESTIONS_PER_PAGE

        categories = [cat.format() for cat in selection]
        current_category = categories[start:end]

        return current_category


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        selection = Category.query.order_by(Category.id).all()
        current_categories = paginate_categories(request, selection)

        if len(current_categories)==0:
            abort(404)

        return jsonify({
            'success': True,
            'categories':current_categories,
            'total_category':len(Category.query.all())
        })

    @app.route('/categories/<int:category_id>', methods=['GET', 'POST'])
    def get_category(category_id):
        cat = Category.query.filter(Category.id == category_id).one_or_none()

        if cat is None:
            abort(404) 
        return jsonify({
            'success': True,
            'code':200,
            'categories':cat.format(),
            'message':'Successful'
        })

                
    @app.route('/')
    def index():
        return '<h1>Hello!! There!!</h1>'

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions)==0:

            abort(404)

        return jsonify({
            'success': True,
            'categories':current_questions,
            'total_category':len(Question.query.all())
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/question/<int:question_id>/delete', methods=['DELETE'])
    def delete_question(question_id):
        selected_question = Question.query.filter(Question.id==question_id).one_or_none()
        
        if selected_question is None:
            abort(404)
        else:
            if request.method=='DELETE':
                db.session.delete(selected_question)
                db.session.commit()

                return jsonify({
                    'success': True,
                    'code':200,
                    'message':'Deleted Successfully!'
                })
            return jsonify({
                'success': False,
                'code':405,
                'message':'inappropriate use of methods'
            })


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def no_resource(error):
        return jsonify({
            'success': False,
            'status': 404,
            'message': 'Resource not Found!!'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'status': 422,
            'message': 'Error 422 unprocessable!!'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success':False,
            'status':400,
            'message':'Error 400 Bad Request'
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'status': True,
            'code': 500,
            'message':'Error 500 Internal Server Error'
        }), 500



    

    return app

