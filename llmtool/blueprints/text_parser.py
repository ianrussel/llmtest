import pandas as pd
import io
import os
from pathlib import Path
from flask import Blueprint, request, render_template, jsonify, send_file

from llmtool.scripts.text_processor import run

text_parser_blueprint = Blueprint("text_parser_blueprint", __name__)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


@text_parser_blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@text_parser_blueprint.route("/process", methods=["POST"])
def process():
    """
    Processes an uploaded text file or text input from a form, validates the content, and runs a processing function on it.

    This function performs the following steps:
    1. Checks if the upload folder exists, and creates it if it doesn't.
    2. Determines the type of upload (file or text).
    3. For file uploads:
       - Validates the presence and type of the file.
       - Reads the content of the file and converts it to a DataFrame.
    4. For text inputs:
       - Retrieves the text from the form.
    5. Validates the length of the text content.
    6. Processes the text content using a specified function.
    7. Writes the output to a file in the upload folder.
    8. Returns a JSON response indicating success or failure.

    Returns:
        JSON: A JSON response containing a message, the processed data or an error message, and an error flag.
    """
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
        file_extension = os.path.splitext(file.filename)[-1].lower()
        if file_extension not in [".txt"]:
            """we only allowed .txt file extension"""
            return (
                jsonify(
                    {
                        "message": "Required file type is in .txt",
                        "error": True,
                        "data": None,
                    }
                ),
                200,
            )
        if file.filename == "":
            return (
                jsonify({"message": "No selected file", "error": True, "data": None}),
                400,
            )
        file_content = file.read().decode("utf-8")
        df = pd.read_csv(io.StringIO(file_content), delimiter="\t")
        df_string = df.to_string()
    else:
        df_string = request.form.get("text")
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
    """download the processed ouput"""
    file_folder = "llmtool/files"
    absolute_path = os.path.abspath(file_folder)
    file_name = f"{absolute_path}/upload.txt"
    return send_file(file_name, as_attachment=True, download_name="downloaded_file.txt")
