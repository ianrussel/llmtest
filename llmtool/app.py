import os

from pathlib import Path
from dotenv import load_dotenv
from flask import Flask


from llmtool.blueprints import text_parser

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(text_parser.text_parser_blueprint)

    return app


app = create_app()
