from flask import Blueprint, request, jsonify, current_app
import os
import pandas as pd
from main.data_engineer.backend.sql_models.models import db, UploadedFile
from main.data_analyst_scientist.data_pipeline.cleaned_data import clean_data

# Define the blueprint
api_bp = Blueprint("api_bp", __name__)

# Upload route to handle all file uploads
@api_bp.route("/upload-file", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save the file to the designated upload folder
    upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file.filename)
    file.save(upload_path)

    try:
        # Attempt to read the file using pandas (it will handle both CSV and Excel)
        if file.filename.endswith(".csv"):
            df = pd.read_csv(upload_path, skiprows=4)
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(upload_path, sheet_name=0, skiprows=4)
        else:
            return jsonify({"error": "Unsupported file format. Only CSV and Excel files are allowed."}), 400

        # Get file size and column names
        file_size = os.path.getsize(upload_path)
        column_names = ",".join(df.columns)

        # Store file metadata in the database
        try:
            uploaded = UploadedFile(filename=file.filename, file_size=file_size, columns=column_names)
            db.session.add(uploaded)
            db.session.commit()
            clean_data()

        except Exception as e:
            db.session.rollback()  # Rollback if the database insertion fails
            current_app.logger.error(f"Database error: {str(e)}")  # Log the error for debugging
            return jsonify({"error": f"Error while saving to the database: {str(e)}"}), 500

        return jsonify({
            "message": f"File '{file.filename}' uploaded successfully!",
            "filename": uploaded.filename,
            "size": uploaded.file_size,
            "columns": df.columns.tolist()
        })

    except Exception as e:
        import traceback
        db.session.rollback()
        error_message = str(e)
        traceback.print_exc()  # This prints the full error traceback to the console
        return jsonify({"error": f"Error occurred while processing the file: {error_message}"}), 500

# Route to list all uploaded files
@api_bp.route("/uploaded-files", methods=["GET"])
def list_files():
    files = UploadedFile.query.all()
    return jsonify([{
        "filename": f.filename,
        "file_size": f.file_size,

        "upload_time": f.upload_time.isoformat(),
        "columns": f.columns.split(",") if f.columns else []
    } for f in files])