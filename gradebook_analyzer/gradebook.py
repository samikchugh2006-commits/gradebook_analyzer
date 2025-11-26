#!
"""
Name: Samik Chugh
Date: 24-11-25
Title: GradeBook Analyzer
"""

import csv
import statistics
from typing import Dict, List, Tuple

def print_welcome():
    print("Welcome to GradeBook Analyzer")
    print("Choose input method:")
    print("1) Manual entry")
    print("2) Load from CSV file")
    print("3) Exit")

# ---------- Task 2: Data entry / CSV import ----------
def manual_entry() -> Dict[str, int]:
    print("\nEnter student data. Type DONE as name when finished.")
    marks = {}
    while True:
        name = input("Student name: ").strip()
        if name.lower() == "done":
            break
        score_str = input("Marks (0-100): ").strip()
        try:
            score = int(score_str)
            if not (0 <= score <= 100):
                print("Enter marks between 0 and 100.")
                continue
        except ValueError:
            print("Please enter a valid integer.")
            continue
        marks[name] = score
    return marks

def load_csv(file_path: str) -> Dict[str, int]:
    marks = {}
    try:
        with open(file_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('Name') or row.get('name')
                mark_str = row.get('Marks') or row.get('marks') or row.get('Score') or row.get('score')
                if not name or mark_str is None:
                    continue
                try:
                    score = int(mark_str)
                except ValueError:
                    # skip bad rows
                    continue
                marks[name.strip()] = score
        return marks
    except FileNotFoundError:
        print("CSV file not found. Put file in same directory or give full path.")
        return {}

# ---------- Task 3: Statistical functions ----------
def calculate_average(marks_dict: Dict[str, int]) -> float:
    if not marks_dict:
        return 0.0
    return sum(marks_dict.values()) / len(marks_dict)

def calculate_median(marks_dict: Dict[str, int]) -> float:
    if not marks_dict:
        return 0.0
    return statistics.median(list(marks_dict.values()))

def find_max_score(marks_dict: Dict[str, int]) -> Tuple[List[str], int]:
    if not marks_dict:
        return ([], 0)
    max_score = max(marks_dict.values())
    students = [n for n,s in marks_dict.items() if s == max_score]
    return (students, max_score)

def find_min_score(marks_dict: Dict[str, int]) -> Tuple[List[str], int]:
    if not marks_dict:
        return ([], 0)
    min_score = min(marks_dict.values())
    students = [n for n,s in marks_dict.items() if s == min_score]
    return (students, min_score)

# ---------- Task 4: Grade assignment ----------
def assign_grade(score: int) -> str:
    if score >= 90:
        return "A"
    elif 80 <= score <= 89:
        return "B"
    elif 70 <= score <= 79:
        return "C"
    elif 60 <= score <= 69:
        return "D"
    else:
        return "F"

def build_gradebook(marks_dict: Dict[str,int]) -> Dict[str,str]:
    return {name: assign_grade(score) for name,score in marks_dict.items()}

def grade_distribution(gradebook: Dict[str,str]) -> Dict[str,int]:
    dist = {g:0 for g in ["A","B","C","D","F"]}
    for g in gradebook.values():
        if g in dist:
            dist[g] += 1
    return dist

# ---------- Task 5: Pass/Fail list using list comprehension ----------
def pass_fail_lists(marks_dict: Dict[str,int], pass_mark:int=40) -> Tuple[List[str],List[str]]:
    passed = [name for name,score in marks_dict.items() if score >= pass_mark]
    failed = [name for name,score in marks_dict.items() if score < pass_mark]
    return passed, failed

# ---------- Task 6: Output table and loop ----------
def print_results_table(marks_dict: Dict[str,int], gradebook: Dict[str,str]):
    print("\nName\tMarks\tGrade")
    print("-"*30)
    for name, marks in marks_dict.items():
        print(f"{name}\t{marks}\t{gradebook.get(name)}")
    print("-"*30)

def analysis(marks_dict: Dict[str,int]):
    if not marks_dict:
        print("No data to analyze.")
        return
    avg = calculate_average(marks_dict)
    med = calculate_median(marks_dict)
    max_students, max_score = find_max_score(marks_dict)
    min_students, min_score = find_min_score(marks_dict)
    gradebook = build_gradebook(marks_dict)
    dist = grade_distribution(gradebook)
    passed, failed = pass_fail_lists(marks_dict)

    # Print summary
    print("\n--- Analysis Summary ---")
    print(f"Average: {avg:.2f}")
    print(f"Median: {med}")
    print(f"Max score: {max_score} by {', '.join(max_students)}")
    print(f"Min score: {min_score} by {', '.join(min_students)}")
    print("\nGrade distribution:")
    for g in ["A","B","C","D","F"]:
        print(f"{g}: {dist[g]}")
    print(f"\nPassed ({len(passed)}): {', '.join(passed)}")
    print(f"Failed ({len(failed)}): {', '.join(failed)}")

    print_results_table(marks_dict, gradebook)
    # Bonus: ask user if they want CSV export
    save = input("Save final grade table to CSV? (y/n): ").strip().lower()
    if save == "y":
        fname = input("Enter file name (e.g. final_grades.csv): ").strip()
        with open(fname, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Name","Marks","Grade"])
            for name, mark in marks_dict.items():
                writer.writerow([name, mark, gradebook.get(name)])
        print(f"Saved to {fname}")

def main_loop():
    while True:
        print_welcome()
        choice = input("Enter option (1/2/3): ").strip()
        if choice == "1":
            marks = manual_entry()
            if marks:
                analysis(marks)
        elif choice == "2":
            path = input("Enter CSV path (or press Enter for 'grades.csv'): ").strip()
            if path == "":
                path = "grades.csv"
            marks = load_csv(path)
            if marks:
                analysis(marks)
            else:
                print("No valid data loaded.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main_loop()
