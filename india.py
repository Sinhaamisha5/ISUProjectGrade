import pandas as pd
import os
from flask import request, jsonify

def setup():
    pass

# ✅ NEW: India university dropdown endpoint (Name + City)
def get_india_universities():
    file_path = "India List.xlsx"

    if not os.path.exists(file_path):
        return jsonify({"error": f"The file '{file_path}' was not found."}), 404

    xls = pd.ExcelFile(file_path, engine='openpyxl')
    required_sheet = "India University List"
    if required_sheet not in xls.sheet_names:
        return jsonify({"error": f"Missing sheet: {required_sheet}"}), 404

    university_df = pd.read_excel(xls, sheet_name=required_sheet)
    university_df.columns = university_df.columns.str.strip()

    if "Name of the University" not in university_df.columns:
        return jsonify({"error": "'Name of the University' column not found"}), 400

    # Combine University Name + City for dropdown display
    university_df["Display"] = university_df.apply(
        lambda row: f"{row['Name of the University']} ({row['City/District']})" if pd.notna(row['City/District']) else row['Name of the University'],
        axis=1
    )
    dropdown_list = university_df[["Display", "Name of the University"]].dropna().drop_duplicates().sort_values(by="Display").to_dict(orient="records")
    return jsonify(dropdown_list)

# ✅ Main grade point lookup for India
def get_grade_point_india():
    file_path = "India List.xlsx"

    if not os.path.exists(file_path):
        return jsonify({"error": f"The file '{file_path}' was not found."}), 404

    xls = pd.ExcelFile(file_path, engine='openpyxl')
    required_sheets = ["India University List", "India Formats"]
    missing_sheets = [sheet for sheet in required_sheets if sheet not in xls.sheet_names]

    if missing_sheets:
        return jsonify({"error": f"Missing required sheets: {missing_sheets}"}), 404

    university_df = pd.read_excel(xls, sheet_name="India University List", engine='openpyxl')
    format_df = pd.read_excel(xls, sheet_name="India Formats", header=None, engine='openpyxl')
    format_df.rename(columns={0: "Format"}, inplace=True)

    university_df.columns = university_df.columns.str.strip()
    format_df.columns = format_df.columns.str.strip()
    format_df["Format"] = format_df["Format"].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip().str.lower()

    required_columns = {"Name of the University", "Format"}
    if not required_columns.issubset(university_df.columns):
        return jsonify({"error": f"Missing required columns: {required_columns - set(university_df.columns)}"}), 400

    university_mapping = {
        row["Name of the University"].strip().lower(): [fmt.strip().lower() for fmt in str(row["Format"]).split(" / ") if pd.notna(row["Format"])]
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

    format_data_us = format_df[format_df["Format"].isin(["format / us grade points", "grade points"])]
    if format_data_us.empty:
        return jsonify({"error": "US grade points format not found"}), 404

    us_scores_row = format_data_us.iloc[0, 1:].dropna().astype(float).tolist()

    try:
        student_grade_float = float(student_grade)
        is_numeric = True
    except ValueError:
        is_numeric = False

    for format_name in applicable_formats:
        format_data = format_df[format_df["Format"] == format_name.strip().lower()].reset_index(drop=True)
        if format_data.empty:
            continue

        grades_values = format_data.iloc[0, 1:].astype(str).str.strip().tolist()
        grades_values = [g.replace("＋", "+") for g in grades_values]

        sample_grade = grades_values[0] if grades_values else ""
        if is_numeric:
            try:
                sample_float = float(sample_grade)
                if (sample_float <= 10 and student_grade_float > 20) or (sample_float > 20 and student_grade_float <= 10):
                    continue
            except ValueError:
                continue

        indices = [i for i, grade in enumerate(grades_values) if grade.strip().lower() == student_grade.strip().lower()]
        if indices:
            equivalent_scores = [us_scores_row[i] for i in indices if i < len(us_scores_row)]
            if equivalent_scores:
                return jsonify({
                    "university": university,
                    "grade": student_grade,
                    "format": format_name,
                    "us_equivalent_scores": equivalent_scores
                })

        if is_numeric:
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

    if all_results:
        complete = [res for res in all_results if len(res.get("closest_grade_matches", [])) >= 2]
        return jsonify(complete[0] if complete else all_results[0])

    return jsonify({
        "error": f"Grade '{student_grade}' was not found in any format for '{university}'.",
        "valid_formats": applicable_formats
    }), 404
