import fitz
from .models import Question
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_questions_from_pdf(pdf_file):
    pdf_path = os.path.join(BASE_DIR, pdf_file)
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()

    # Parse text to extract questions
    questions = parse_questions_from_text(text)
    return questions

def populate_database(questions):
    for question_data in questions:
        question = Question(
            question_main=question_data['main'],
            a=question_data['a'],
            b=question_data['b'],
            c=question_data['c'],
            d=question_data['d'],
            e=question_data.get('e', '')  # Some questions may not have option E
        )
        question.save()


# used a regex generator to make this function work
def parse_questions_from_text(text):
    # Split the text into sections based on question numbers (assuming questions are numbered)
    question_blocks = re.split(r"\n?\d+\.\s", text)  # Split by the pattern 'number. ' (e.g., '1. ')

    questions = []
    for block in question_blocks[1:]:  # Skip the first split (since it may be irrelevant)
        # Extract the main question and the options (A, B, C, D)
        lines = block.strip().split("\n")

        # Assume the first line is the main question
        question_main = lines[0].strip()

        # Now, find the answer options
        options = {'a': '', 'b': '', 'c': '', 'd': ''}
        for line in lines[1:]:
            line = line.strip()
            if line.startswith('A.'):
                options['a'] = line[2:].strip()  # Get the text after 'A.'
            elif line.startswith('B.'):
                options['b'] = line[2:].strip()  # Get the text after 'B.'
            elif line.startswith('C.'):
                options['c'] = line[2:].strip()  # Get the text after 'C.'
            elif line.startswith('D.'):
                options['d'] = line[2:].strip()  # Get the text after 'D.'

        # Append the extracted question and options as a dictionary
        question_data = {
            'main': question_main,
            'a': options['a'],
            'b': options['b'],
            'c': options['c'],
            'd': options['d'],
            # Add 'e' option if your PDF contains questions with an 'E' option
        }
        questions.append(question_data)

    return questions


file = "PRINCIPLES_OF_ACCOUNTS.pdf"
questions = extract_questions_from_pdf(file)
populate_database(questions)
