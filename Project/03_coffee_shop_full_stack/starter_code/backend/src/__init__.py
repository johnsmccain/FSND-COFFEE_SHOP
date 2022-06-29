from email.base64mime import body_encode
import os
from turtle import title
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all,setup_db, Drink
from .auth.auth import AuthError, requires_auth

def create_app(test_config = None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    @TODO uncomment the following line to initialize the database
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    !! Running this funciton will add one
    '''
    db_drop_and_create_all()

    # ROUTES
    '''
    @TODO implement endpoint
        GET /drinks
            it should be a public endpoint
            it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks')
    def get_drinks():
        try:
            drinks = Drink.short()
            if len(drinks) > 0:
                return jsonify({
                    'status': 200,
                    'success': True,
                    'drinks': drinks,
                })

        except:
            abort(404)


    '''
    @TODO implement endpoint
        GET /drinks-detail
            it should require the 'get:drinks-detail' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks/<int:drink_id>')
    @requires_auth('get:drinks-detail')
    def get_drinkDetail(drink_id):
        try:
            drinks = Drink.long(drink_id)
            return jsonify({
                'status': 200,
                'success': True,
                'drinks': drinks
            })
        except:
            abort(404)


    '''
    @TODO implement endpoint
        POST /drinks
            it should create a new row in the drinks table
            it should require the 'post:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks', methods=['POST'])
    @requires_auth('post:drinks')
    def create_drink():
        body = request.get_json()
        try:
            title = body.get('title', None)
            recipe = body.get('recipe', None)

            drink = Drink(title=title, recipe=recipe)
            drink.insert()
            return jsonify({
                'success': True,
                'status': 200
            })
        except:
            abort(404)


    '''
    @TODO implement endpoint
        PATCH /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks/<id>', methods=['PATCH'])
    @requires_auth('patch:drinks')
    def update_drink(id):
        body = request.get_json()
        try:
            title = body.get('title', None)
            recipe = body.get('recipe', None)
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            if not drink:
                abort(404)
            drink.update()
            return jsonify({
                'success': True,
                'status': 200,
                'drinks': drink
            })
        except:
            abort(422)

    '''
    @TODO implement endpoint
        DELETE /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks/<id>')
    @requires_auth('delete:drinks')
    def delete_drink(id):
        try:
            drink = Drink.query.filter(Drink.id == id)
            if not drink:
                abort(404)
            drink.delete()
        except:
            abort(404)

    # Error Handling
    '''
    Example error handling for unprocessable entity
    '''


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    '''
    @TODO implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resource not found"
        }), 404
    '''
    @TODO implement error handler for 404
        error handler should conform to general task above
    '''


    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above
    '''



    return app