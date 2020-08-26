import os
import sys
from flask import Flask, request, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import random

from models import setup_db, Question, Category, db

## Services
from services import question as question_service, category as category_service, response

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)

  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  @app.route('/')
  def home():
    return jsonify({'message': f"Hello World!"})

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def categories():
    categories = category_service.get_all()
    return jsonify({
      'categories': categories,
      'total': len(categories)
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():

    page = request.args.get('page', 1, type=int)
    start = (page-1) * 5
    end = start + 5

    questions = question_service.get_all()
    categories = category_service.get_all()

    return jsonify(response.format('success', {
      'questions': questions[start:end],
      'total_questions': len(questions),
      'categories': categories,
      'current_category': None
    }, True))


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):

    message = f'Question has been deleted successfully'

    try:
      question_service.delete(id)
    except:
      db.session.rollback()
      message = f'An error has occurred when deleting the question'
      print(sys.exc_info())
    finally:
      db.session.close()

    return jsonify(response.format(message))

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def store_question():
    message = f'Question created successfully'
    question_id = None

    try:
      question_id = question_service.create(request.json)
    except:
      db.session.rollback()
      message = f'An error has occurred creating a new question'
      print(sys.exc_info())
    finally:
      db.session.close()

    return jsonify(response.format(message, {'question_id': question_id} if question_id else {}))

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def category_questions(id):

    data = {
      'questions': [],
      'total_questions': 0,
      'current_category': category_service.get(id),
    }

    try:
      data['questions'] = category_service.questions(id)
      data['total_questions'] = len(data['questions'])
    except:
      message = f'An error has occurred getting category questions'
      print(sys.exc_info())
    finally:
      db.session.close()

    print(data)

    return jsonify(response.format(message='', data=data, flat=True))


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

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    