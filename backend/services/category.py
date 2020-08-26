
from models import Category


def get_all():
    return [category.format() for category in Category.query.all()]

def get(id):
    return Category.query.get(id).format()

def questions(id):
    return [question.format() for question in Category.query.get(id).questions]