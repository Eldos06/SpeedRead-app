from flask import Flask, render_template, jsonify
from random import randint, choice
import operator

app = Flask(__name__)


def generate_math_problem():
    ops_map = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    num1 = randint(1, 99)
    num2 = randint(1, 99)
    op_symbol = choice(list(ops_map.keys()))

    raw_result = ops_map[op_symbol](num1, num2)
    result = round(raw_result, 2) if op_symbol == '/' else raw_result

    return {
        'equation': f"{num1} {op_symbol} {num2}",
        'result': result
    }


@app.route('/')
def home():
    problem = generate_math_problem()
    # Flask автоматически будет искать файл index.html в папке templates
    return render_template('index.html', problem=problem)


if __name__ == '__main__':
    app.run(debug=True)