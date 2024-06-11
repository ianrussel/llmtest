import pandas as pd
import io
import os
from pathlib import Path
from flask import Blueprint, request, render_template, jsonify, redirect, send_file

from llmtool.scripts.sample_app import run

text_parser_blueprint = Blueprint("text_parser_blueprint", __name__)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


@text_parser_blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@text_parser_blueprint.route("/process", methods=["POST"])
def process():
    df_string = None
    file_folder = "llmtool/files"
    absolute_path = os.path.abspath(file_folder)
    file_name = "upload.txt"
    if not os.path.exists(absolute_path):
        os.makedirs(file_folder)
    upload_type = request.form.get("type")
    if upload_type == "file":
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        file_content = file.read().decode("utf-8")
        df = pd.read_csv(io.StringIO(file_content), delimiter="\t")
        df_string = df.to_string()
    else:
        print("its type text")
        df_string = request.form.get("text")
    print(f" lengt {len(df_string)}")
    if len(df_string) > 5000:
        return jsonify(
            {
                "message": "Text exceed max length of 1500 characters",
                "data": None,
                "error": True,
            }
        )
    if len(df_string) < 30:
        return jsonify(
            {
                "message": "Text too short, min length is 30 characters",
                "data": None,
                "error": True,
            }
        )
    output = run(df_string)
    output_filename = f"{absolute_path}/{file_name}"
    with open(output_filename, "w") as f:
        f.write(output)
    return jsonify({"message": "Success", "data": output, "error": False}), 200


@text_parser_blueprint.route("/download", methods=["GET"])
def download():

    file_folder = "llmtool/files"
    absolute_path = os.path.abspath(file_folder)
    file_name = f"{absolute_path}/upload.txt"
    return send_file(file_name, as_attachment=True, download_name="downloaded_file.txt")
