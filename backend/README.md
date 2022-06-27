# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.
## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks
One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT

```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

#### formatting the question by function defined in the class
def format_questions(all_questions):
    formatted_questions = [
        question.format() for question in all_questions]
    return formatted_questions

#### formatting the question by function defined in the class
def format_questions(all_questions):
    formatted_questions = [
    question.format() for question in all_questions]
    return formatted_questions

'''
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PUT, POST, DELETE, OPTIONS')
        return response

'''
    GET '/categories'
    - Fetches a dictionary of categories in which the keys are the ids
        and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories,
        that contains a object of id: category_string key:value pairs.
    {'1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"}
    '''

    def formatted_categories():
        # get all categories
        all_categories = Category.query.order_by(Category.id).all()

        categories = {}
        for category in all_categories:
            categories[category.id] = category.type

        return categories

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''

    # Get all categories
    @app.route('/categories', methods=['GET'])
    def get_categories():
        # Get the categories as a dictionay of {id: type, id: type}
        categories = formatted_categories()
        total_categories = len(categories)

        data = {
            'success': True,
            'categories': formatted_categories(),
            'total_categories': total_categories
        }

        # send data in json format
        return jsonify(data)

'''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application,
    you should see questions and categories generated,
    10 questions per page and pagination at the bottom of the screen
    for 3 pages. Clicking on the page numbers should update the questions.
    '''
    # Get all the questions. Default page = 1
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions)==0:

            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': [],
            'categories': formatted_categories(),
        }), 200

'''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed. This removal will persist in the database
    and when you refresh the page.
    '''
    # Delete a specific question
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            # if no question is found to delete,
            # that means request unprocessable
            if question is None:
                abort(422)

            question.delete()

            data = {
                'success': True,
                'deleted': question_id
            }

            return jsonify(data)

        except Exception:
            abort(422)

'''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page of the questions list in the "List" tab.
    '''

    # Create a question if the required fields are given
    # In table questions, the question field is unique.
    # Thus same question will not be added twice.
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        search = body.get('searchTerm', None)

        try:
            if search:
                questions = Question.query.filter(
                    Question.question.ilike(f'%{search}%')
                ).all()

                current_questions = [question.format()
                                     for question in questions]
                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(current_questions),
                })

            else:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty
                )
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all())
                })
        except Exception:
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

    # Search a question with given searchTerm
    @app.route("/search_question", methods=['POST'])
    def search():
        body = request.get_json()
        search = body.get('searchTerm')
        questions = Question.query.filter(
            Question.question.ilike('%'+search+'%')).all()

        if questions:
            currentQuestions = paginate_questions(request, questions)
            return jsonify({
                'success': True,
                'questions': currentQuestions,
                'total_questions': len(questions)
            })
        else:
            abort(404)

 '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    # Get questions from a category
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_from_category(category_id):
        try:
            # Get the parameter page from the request and by default page=1
            page = request.args.get('page', 1, type=int)

            # Get the questions in the form of Pagination object
            # according to the page number
            questions_in_range_obj = Question.query.order_by(
                Question.category).filter(
                Question.category == category_id).paginate(
                    per_page=QUESTIONS_PER_PAGE, page=page, error_out=True)

            # Get the total number of questions from the Pagination object
            total_questions = questions_in_range_obj.total

            # Get the items from the Pagination object
            questions_in_range = questions_in_range_obj.items

            # format the questions
            formatted_questions = format_questions(questions_in_range)

            # if there is no exported questions,
            # that means no questions is found. Through not found error 404
            if len(questions_in_range) == 0:
                abort(404)

            # get the category from category_id
            current_category = Category.query.get(category_id)

            # get the category type of the 1st question. Ex.: 'Science'
            current_category_type = current_category.type

            data = {
                'success': True,
                'questions': formatted_questions,
                'total_questions': total_questions,
                'current_category': current_category_type
            }

            # send data in json format
            return jsonify(data)

        except Exception:
            abort(404)

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

    # Get a question to play
    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        try:
            body = request.get_json()

            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            # If 'ALL' categories is 'clicked', filter available Qs
            if category['type'] == 'click':
                available_questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            # Filter available questions by chosen category & unused questions
            else:
                available_questions = Question.query.filter_by(
                    category=category['id']).filter(
                        Question.id.notin_((previous_questions))).all()

            # randomly select next question from available questions
            new_question = available_questions[random.randrange(
                0, len(available_questions))].format() if len(
                    available_questions) > 0 else None

            return jsonify({
                'success': True,
                'question': new_question
            })
        except:
            abort(422)

 '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    @app.errorhandler(400)
    def bad_request(error):
        data = {
            'success': False,
            'error': 400,
            'message': 'bad request'
        }
        return jsonify(data), 400

    @app.errorhandler(404)
    def not_found(error):
        data = {
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }
        return jsonify(data), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        data = {
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }
        return jsonify(data), 405

    @app.errorhandler(422)
    def unprocessable(error):
        data = {
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }
        return jsonify(data), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        data = {
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }
        return jsonify(data), 500

####Test API Tasks
"""
    TODO
    Write at least one test for each test for successful operation
    and for expected errors.
    """
    # Try to get all questions with no page number given
    # and default page=1 is taken automatically
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        print("\n######SUCCESS!!#######")
        # Where there is no question, endpoint will return total_questions = 0.
        # To avoid False in that case, use type comparison
        self.assertEqual(type(data['total_questions']), int)
        self.assertEqual(type(data['questions']), list)
        self.assertEqual(type(data['categories']), dict)
        self.assertTrue(type(data['current_category']), str)
        print("\n######SUCCESS!!#######")


    # Try to hit the /questions endpoint with page number out of limit
    # and get the 404 reply
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=7777777')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_422_delete_question_with_invalid_id(self):
        res = self.client().delete('/questions/{}'.format(77777777))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Try to get all the categories with get request
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['categories']), dict)
        self.assertTrue(data['total_categories'])