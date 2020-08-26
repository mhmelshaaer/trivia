from models import Question, Category, db


def get_all():
    return [question.format() for question in Question.query.all()]

def create(data):

    category = Category.query.get(data.get('category'))
    new_question = Question(
        question=data.get('question'),
        answer=data.get('answer'),
        category=data.get('category'),
        difficulty=data.get('difficulty')
    )

    # new_question.questionCategory = category

    db.session.add(new_question)
    db.session.commit()

    return new_question.id

def delete(id):
    Question.query.filter_by(id=id).delete()
    db.session.commit()