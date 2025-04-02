import pandas as pd
import os
from flask import Flask, request, jsonify
def setup():
    pass


def get_grade_point_china():
    # File Path
    #file_path = "testdata1.xlsx"
    file_path = "University List.xlsx"

    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")

    # Load Excel File
    xls = pd.ExcelFile(file_path)

    # Load Sheets Safely
    required_sheets = ["China University List", "China Formats"]
    missing_sheets = [sheet for sheet in required_sheets if sheet not in xls.sheet_names]

    if missing_sheets:
        raise ValueError(f"Missing required sheets: {missing_sheets}")

    # Load DataFrames
    university_df = pd.read_excel(xls, sheet_name="China University List")
    format_df = pd.read_excel(xls, sheet_name="China Formats", header=None)
    format_df.rename(columns={0: "Format"}, inplace=True)

    # Clean Column Names and Strip Whitespaces
    university_df.columns = university_df.columns.str.strip()
    format_df.columns = format_df.columns.str.strip()

    # Rename first column to 'Format' for consistency
    format_df.rename(columns={format_df.columns[0]: "Format"}, inplace=True)
    format_df["Format"] = format_df["Format"].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip().str.lower()

    # Print all available format names for debugging
    print("Available formats in format_df:", format_df["Format"].unique())

    # Ensure Required Columns Exist
    required_columns = {"University Name", "Format"}
    print(required_columns)
    print("**********")
    if not required_columns.issubset(university_df.columns):

        raise ValueError(f"Missing required columns: {required_columns - set(university_df.columns)}")

    # Create Mapping (Using 'University List' instead of 'University')
    university_mapping = {
        row["University Name"].strip().lower(): [fmt.strip().lower() for fmt in row["Format"].split(" / ")]
        for _, row in university_df.iterrows()
    }

    print("Inside grade point")
    university = request.args.get("university", "").strip().lower()
    student_grade = request.args.get("grade")
    print(f"value entered: {university}, student grade: {student_grade}")

    if not university or student_grade is None:
        return jsonify({"error": "University and grade parameters are required"}), 400

    if university not in university_mapping:
        return jsonify({"error": "University not found"}), 404

    print("Checking university and fetching applicable formats")
    applicable_formats = university_mapping[university]
    print(f"Applicable formats for {university}: {applicable_formats}")

    for format_name in applicable_formats:
        format_name = format_name.strip().lower()
        print(f"Looking for format: {format_name}")
        if not format_name:
            continue

        format_data = format_df[format_df["Format"] == format_name].reset_index(drop=True)
        print(f"Format data for {format_name}:", format_data)

        if format_data.empty:
            print(f"Format {format_name} not found in format_df")
            continue

        # Convert student_grade to a string for uniform comparison
        student_grade = str(student_grade).strip()

        # ✅ Extract grades from the **first row**, not column names
        grades_values = format_data.iloc[0, 1:].astype(str).str.strip().tolist()
        print(f"Grades in {format_name}: {grades_values}")

        # ✅ Fetch the US equivalence format (Format / US Grade Points)
        format_name_US = "Format / US Grade Points".strip().lower()
        format_data_US = format_df[format_df["Format"].str.strip().str.lower() == format_name_US].reset_index(drop=True)

        # Ensure Format / US Grade Points exists
        if format_data_US.empty:
            print(f"Error: {format_name_US} not found in format_df")
            continue

        us_scores_row = format_data_US.iloc[0, 1:].dropna().astype(float).tolist()
        print(f"US Scores Row: {us_scores_row}")

        # ✅ Find **all** indices where `student_grade` matches the first row values
        indices = [i for i, grade in enumerate(grades_values) if grade == student_grade]
        print(f"Matching indices for {student_grade}: {indices}")

        equivalent_scores = []  # Store equivalent scores

        for index in indices:
            if index < len(us_scores_row):
                equivalent_scores.append(us_scores_row[index])

        if equivalent_scores:
            print(f"Found grade {student_grade} in {format_name}. US equivalents: {equivalent_scores}")
            return jsonify({
                "university": university,
                "grade": student_grade,
                "format": format_name,  # ✅ Include the format name
                "us_equivalent_scores": equivalent_scores  # ✅ Return the list of scores
            })

    print(f"Grade {student_grade} not found in any applicable format for {university}")
    return jsonify({"error": "Grade not found in the university's formats"}), 404