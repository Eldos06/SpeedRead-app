import operator
from random import choice, randint, shuffle

from flask import Flask, render_template, request

from common import configure_logging, log

app = Flask(__name__)


MIN_NUMBER = 1
MAX_NUMBER = 99
OPERATOR_MAP = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
COUNT_FUNCTIONS = 112
SIZE_TABLE = 5


def get_function() -> dict[str, str]:
    """Формирует уравнение с результатом.

    Returns:
        dict[str, str]: уравнение с результатом.
    """

    operator_symbol = choice(list(OPERATOR_MAP))

    number_left = randint(MIN_NUMBER, MAX_NUMBER)
    number_right = randint(MIN_NUMBER, MAX_NUMBER)
    while True:
        result: float | int = OPERATOR_MAP[operator_symbol](number_left, number_right)
        if (
            operator_symbol == "/" and not result.is_integer()
        ):  # Если есть дробная часть - пересчитываем с новыми числами.
            number_left = randint(MIN_NUMBER, MAX_NUMBER)
            number_right = randint(MIN_NUMBER, MAX_NUMBER)
            continue
        return {"equation": f"{number_left} {operator_symbol} {number_right}", "result": str(result)}


def get_table(size: int = SIZE_TABLE) -> list[list[int | None]]:
    """Отдаёт таблицу Шульте.

    Args:
        size (int, optional): размер таблицы. По дефолту SIZE_TABLE.

    Returns:
        list[list[int | None]]: таблица Шульте.
    """
    numbers = list(range(1, size * size))
    shuffle(numbers)
    table: list[list[int | None]] = []
    point_index = size // 2
    for i in range(size):
        row = []
        table.append(row)
        for j in range(size):
            if point_index == i and point_index == j:
                row.append(None)
                continue
            row.append(numbers.pop())
    return table


@app.route("/")
def home():
    function = get_function()
    # Flask автоматически будет искать файл index.html в папке templates
    log(f"function: {function}")
    log(f"render_template('index.html', function=function): {render_template('index.html', function=function)}")
    return render_template("index.html", function=function)


@app.route("/functions/")
def functions() -> str:
    """Ручка получения html-страницы c формулами.

    Returns:
        str: html-страница.
    """
    count = request.args.get("count", COUNT_FUNCTIONS, type=int)
    if count <= 0:
        count = COUNT_FUNCTIONS
    return render_template("index.html", functions=[get_function() for _ in range(count)])


@app.route("/tables/")
def table() -> str:
    """Ручка получения html-страницы c таблицей Шульте.

    Returns:
        str: html-страница.
    """
    size = request.args.get("size", SIZE_TABLE, type=int)
    if size <= 2 and not size % 2:  # Должен быть больше 3x3 и нечётный, чтобы точка была по-середине.
        size = SIZE_TABLE
    return render_template("index.html", table=get_table(size))


if __name__ == "__main__":
    configure_logging()
    app.run(debug=True)
