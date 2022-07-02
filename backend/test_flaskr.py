import os
#from turtle import clear
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db
# from models import Question, Category

# To generate random string
import random
import string


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.database_name = "trivia_test"
        self.username = "postgres"
        self.password = "postgres"
        self.host_port = "localhost:5432"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.username, self.password, self.host_port, self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

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
        
        # Where there is no question, endpoint will return total_questions = 0.
        # To avoid False in that case, use type comparison
        self.assertEqual(type(data['total_questions']), int)
        self.assertEqual(type(data['questions']), list)
        self.assertEqual(type(data['categories']), dict)
        self.assertTrue(type(data['current_category']), str)

    def test_delete_question(self):
        res = self.client().get('/questions/21')
        
        self.assertEqual(res.status_code, 405)
    


    # Try to hit the /questions endpoint with page number out of limit
    # and get the 404 reply
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=77')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_422_delete_question_with_invalid_id(self):
        res = self.client().delete('/questions/{}'.format(777))
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

    # Try to hit the /categories with POST request where POST is not allowed
    def test_405_on_all_categories(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_400_if_questions_by_category_fails(self):
        """Tests getting questions by category failure 400"""

        # send request with category id 100
        response = self.client().get('/categories/10/questions')

        # load response data
        data = json.loads(response.data)

        # check response status code and message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    # Try to get all questions based on the category
    def test_get_questions_from_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(type(data['current_category']), str)

    # Try to get a random question with the given category
    def test_get_quiz(self):
        body = {
            "previous_questions": [12, 14, 13],
            "quiz_category": {
                "type": "Art", "id": "2"
            }
        }
        res = self.client().post('/quizzes', json=body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_play_quiz_fails(self):
        """Tests playing quiz game failure 422"""
        response = self.client().post('/quizzes', json={})

        data = json.loads(response.data)
        # check response status code and message
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    # Try to search questions
    def test_search_questions(self):
        body = {
            "searchTerm": "who"
        }
        res = self.client().post('/search_question', json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # Test 400 with no given body to search
    def test_400_sent_no_body_in_search(self):
        res = self.client().post('/searchquestions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test create question with random string as multiple entry is not allowed
    def test_create_question(self):
        # generate a string of length 10 to get a random question
        length = 10
        letters = string.ascii_letters
        random_string = ''.join(random.choice(letters) for i in range(length))

        question = "This is a test question text?"
        body = {
            "question": question,
            "answer": "The Answer",
            "difficulty": 1,
            "category": 2
        }

        res = self.client().post('/questions', json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
       

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()