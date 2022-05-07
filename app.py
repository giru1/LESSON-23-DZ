import os

from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def other_command(iter_obj, query):
    query_items = query.split('|')
    result = iter(map(lambda v: v.strip(), iter_obj))
    for item in query_items:
        cmd_value = item.split(':')
        command = cmd_value[0]
        value = cmd_value[1]
        result = build_query(result, command, value)
    return result


def build_query(file_data, cmd, value):
    res = map(lambda v: v.strip(), file_data)
    if cmd == "filter":
        res = filter(lambda v, txt=value: txt in v, res)
    if cmd == "map":
        arg = int(value)
        res = map(lambda v, idx=arg: v.split(" ")[idx], res)
    if cmd == "unique":
        res = set(res)
    if cmd == "sort":
        reverse = value == "desc"
        res = sorted(res, reverse=reverse)
    if cmd == "Limit":
        arg = int(value)
        res = list(res)[: arg]
    return res


@app.route("/perform_query", methods=["POST", "GET"])
def perform_query():

    query = request.args.get("query")
    try:
        cmd1 = request.args.get("cmd1")
        cmd2 = request.args.get("cmd2")
        value1 = request.args.get("value1")
        value2 = request.args.get("value2")
        file_name = request.args.get("file_name")

    except KeyError:
        raise BadRequest(description=f"111not found key")
    file_path = os.path.join(DATA_DIR, file_name)
    print(111)
    if not os.path.exists(file_path):
        return BadRequest(description=f"222{file_name} was not found")

    with open(file_path)as file:
        if query is not None:
            result = other_command(file, query)
            content = '\n'.join(result)
        else:
            result = build_query(file, cmd1, value1)
            result = build_query(file, cmd2, value2)
            content = '\n'.join(result)

    return app.response_class(content, content_type="text/plain")


if __name__ == '__main__':
    app.run(debug=True)