#	A Restful API for e-Library 
#	Author: Nikos-Nikitas

#	Used the flask_restful example code
#	Find more about Flask-RESTful: https://flask-restful.readthedocs.io/en/latest/index.html

#	importing Flask and the restful functions we'll use.
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__) # like in any flask app.
api = Api(app)

# All of our books in a multilevel dictionary with their title and authors.

BOOKS = {
    'Book1': {'author': 'Author1'},
    'Book2': {'author': 'Author2'},
    'Book3': {'author': 'Author3'},
}


def abort_if_book_doesnt_exist(Book_id):
    if book_id not in BOOKS:
        abort(404, message="Book {} doesn't exist".format(book_id))

# the parser parses arguments on request so that authors can be returned by the server.
parser = reqparse.RequestParser()
parser.add_argument('author')


# The Book class:
#  - shows a Book item and lets you delete a Book.
class Book(Resource):
    def get(self, Book_id):
        abort_if_Book_doesnt_exist(Book_id)
        return BookS[Book_id]

    def delete(self, Book_id):
        abort_if_Book_doesnt_exist(Book_id)
        del BookS[Book_id]
        return '', 204
	#puts author in the book
    def put(self, Book_id):
        args = parser.parse_args()
        author = {'author': args['author']}
        BookS[Book_id] = author
        return author, 201


# BookList
# shows a list of all Books, and lets you POST to add new authors
class BookList(Resource):
    def get(self):
        return BookS

    def post(self):
        args = parser.parse_args()
        Book_id = int(max(BookS.keys()).lstrip('Book')) + 1
        Book_id = 'Book%i' % Book_id
        BookS[Book_id] = {'author': args['author']}
        return BookS[Book_id], 201

# API Setup here
api.add_resource(BookList, '/Books')
api.add_resource(Book, '/Books/<Book_id>')

# like any flask application that runs
if __name__ == '__main__':
    app.run(debug=False)
