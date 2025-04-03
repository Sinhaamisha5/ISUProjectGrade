import pandas as pd
import os
from flask import request, jsonify

def setup():
    pass

def get_grade_point_nigeria():
    file_path = "Nigeria List.xlsx"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")

    xls = pd.ExcelFile(file_path, engine='openpyxl')
    required_sheets = ["Nigeria University List", "Nigeria Formats"]
    missing_sheets = [sheet for sheet in required_sheets if sheet not in xls.sheet_names]

    if missing_sheets:
        raise ValueError(f"Missing required sheets: {missing_sheets}")

    university_df = pd.read_excel(xls, sheet_name="Nigeria University List", engine='openpyxl')
    format_df = pd.read_excel(xls, sheet_name="Nigeria Formats", header=None, engine='openpyxl')
    format_df.rename(columns={0: "Format"}, inplace=True)

    university_df.columns = university_df.columns.str.strip()
    format_df.columns = format_df.columns.str.strip()
    format_df["Format"] = format_df["Format"].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip().str.lower()

    required_columns = {"University List", "Format"}
    if not required_columns.issubset(university_df.columns):
        raise ValueError(f"Missing required columns: {required_columns - set(university_df.columns)}")

    university_mapping = {
        row["University List"].strip().lower(): [fmt.strip().lower() for fmt in str(row["Format"]).split(" / ") if pd.notna(row["Format"])]
        for _, row in university_df.iterrows()
    }

    university = request.args.get("university", "").strip().lower()
    student_grade = request.args.get("grade", "").replace(" ", "").replace("%2B", "+").strip()

    if not university or student_grade is None:
        return jsonify({"error": "University and grade parameters are required"}), 400

    if university not in university_mapping:
        return jsonify({"error": "University not found"}), 404

    applicable_formats = university_mapping[university]

    all_results = []

    for format_name in applicable_formats:
        format_name = format_name.strip().lower()
        format_data = format_df[format_df["Format"] == format_name].reset_index(drop=True)

        if format_data.empty:
            continue

        grades_values = format_data.iloc[0, 1:].astype(str).str.strip().tolist()
        grades_values = [g.replace("＋", "+") for g in grades_values]

        format_data_us = format_df[format_df["Format"].isin(["format / us grade points", "format"])].reset_index(drop=True)

        if format_data_us.empty:
            continue

        us_scores_row = format_data_us.iloc[0, 1:].dropna().astype(float).tolist()

        indices = [i for i, grade in enumerate(grades_values) if grade.strip().lower() == student_grade.strip().lower()]

        equivalent_scores = []
        for index in indices:
            if index < len(us_scores_row):
                equivalent_scores.append(us_scores_row[index])

        if equivalent_scores:
            return jsonify({
                "university": university,
                "grade": student_grade,
                "format": format_name,
                "us_equivalent_scores": equivalent_scores
            })

        # Handle numeric closest match
        try:
            student_grade_float = float(student_grade)
            numeric_grades = []
            for g in grades_values:
                try:
                    numeric_grades.append(float(g))
                except ValueError:
                    numeric_grades.append(None)

            valid_pairs = [(i, val) for i, val in enumerate(numeric_grades) if val is not None]

            closest_below = max((val for i, val in valid_pairs if val <= student_grade_float), default=None)
            closest_above = min((val for i, val in valid_pairs if val >= student_grade_float), default=None)

            bounds = []
            for bound in (closest_below, closest_above):
                if bound is not None:
                    indices = [i for i, val in valid_pairs if val == bound]
                    for idx in indices:
                        if idx < len(us_scores_row):
                            bounds.append({"grade": bound, "us_score": us_scores_row[idx]})

            if bounds:
                all_results.append({
                    "university": university,
                    "grade": student_grade,
                    "format": format_name,
                    "closest_grade_matches": bounds
                })
        except ValueError:
            continue

    if all_results:
        return jsonify(all_results[0])

    return jsonify({"error": "Grade not found in the university's formats"}), 404

