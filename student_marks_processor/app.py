import numpy as np
import sys
from collections import Counter
import os

def read_student_data(filename):
    # Read student data from file and return as list of tuples
    students = []
    
    # Check if file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Input file '{filename}' not found.")
    
    try:
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith('#'):  # Skip empty lines and comments
                    continue
                
                try:
                    parts = line.split(',')
                    if len(parts) != 3:
                        print(f"Warning: Line {line_num} has invalid format, skipping...")
                        continue
                    
                    reg_num = parts[0].strip()
                    exam_mark = float(parts[1].strip())
                    coursework_mark = float(parts[2].strip())
                    
                    # Validate marks
                    if not (0 <= exam_mark <= 100) or not (0 <= coursework_mark <= 100):
                        print(f"Warning: Invalid marks for {reg_num} on line {line_num}, skipping...")
                        continue
                    
                    students.append((reg_num, exam_mark, coursework_mark))
                    
                except ValueError as e:
                    print(f"Warning: Invalid data on line {line_num}, skipping...")
                    continue
                    
    except Exception as e:
        raise Exception(f"Error reading file: {e}")
    
    return students

def calculate_overall_mark(exam, coursework):
    # Calculate overall mark with weighting (60% exam, 40% coursework)
    return (exam * 0.6) + (coursework * 0.4)

def assign_grade(overall_mark):
    # Assign grade based on overall mark
    if overall_mark >= 70:
        return 'A'
    elif overall_mark >= 60:
        return 'B'
    elif overall_mark >= 50:
        return 'C'
    elif overall_mark >= 40:
        return 'D'
    else:
        return 'F'

def create_structured_array(students):
    # Create NumPy structured array with all student data
    # Define data type for structured array
    dtype = [
        ('registration', 'U20'),  # Unicode string, max 20 chars
        ('exam', 'f4'),           # 32-bit float
        ('coursework', 'f4'),     # 32-bit float
        ('overall', 'f4'),        # 32-bit float
        ('grade', 'U1')           # Unicode string, 1 char
    ]
    
    # Create array
    student_array = np.empty(len(students), dtype=dtype)
    
    # Populate array
    for i, (reg_num, exam, coursework) in enumerate(students):
        overall = calculate_overall_mark(exam, coursework)
        grade = assign_grade(overall)
        
        student_array[i] = (reg_num, exam, coursework, overall, grade)
    
    return student_array

def sort_by_overall_mark(student_array):
    # Sort students by overall mark (descending)
    return np.sort(student_array, order='overall')[::-1]  # Descending order

def write_results(student_array, filename):
    # Write sorted results to output file
    try:
        with open(filename, 'w') as file:
            # Write header
            file.write("Registration Number,Exam Mark,Coursework Mark,Overall Mark,Grade\n")
            
            # Write student data
            for student in student_array:
                file.write(f"{student['registration']},{student['exam']:.1f},"
                          f"{student['coursework']:.1f},{student['overall']:.1f},{student['grade']}\n")
        print(f"Successfully wrote results to {filename}")
    except Exception as e:
        raise Exception(f"Error writing output file: {e}")

def display_statistics(student_array):
    # Display grade statistics
    grades = student_array['grade']
    grade_counts = Counter(grades)
    total_students = len(student_array)
    
    print("\nGrade Statistics:")
    print("=" * 30)
    print(f"Total Students: {total_students}")
    print("\nGrade Distribution:")
    
    # Display in order A, B, C, D, F
    for grade in ['A', 'B', 'C', 'D', 'F']:
        count = grade_counts.get(grade, 0)
        percentage = (count / total_students * 100) if total_students > 0 else 0
        print(f"  Grade {grade}: {count:3d} ({percentage:5.1f}%)")
    
    # Calculate and display averages
    avg_exam = np.mean(student_array['exam'])
    avg_coursework = np.mean(student_array['coursework'])
    avg_overall = np.mean(student_array['overall'])
    
    print(f"\nAverage Marks:")
    print(f"  Exam:       {avg_exam:.1f}")
    print(f"  Coursework: {avg_coursework:.1f}")
    print(f"  Overall:    {avg_overall:.1f}")
    
    # Pass rate (grades A-D)
    pass_count = sum(grade_counts.get(g, 0) for g in ['A', 'B', 'C', 'D'])
    pass_rate = (pass_count / total_students * 100) if total_students > 0 else 0
    print(f"\nPass Rate:    {pass_rate:.1f}%")

def main():
    print("Student Marks Processing System")
    print("=" * 40)
    
    # Default filenames
    input_file = "student_marks.txt"
    output_file = "processed_results.txt"
    
    try:
        # Allow command line arguments for filenames
        if len(sys.argv) >= 2:
            input_file = sys.argv[1]
        if len(sys.argv) >= 3:
            output_file = sys.argv[2]
        
        print(f"Reading data from: {input_file}")
        
        # Read student data
        students = read_student_data(input_file)
        if not students:
            print("No valid student data found.")
            return
        
        print(f"Processing {len(students)} students...")
        
        # Create structured array
        student_array = create_structured_array(students)
        
        # Sort by overall mark
        sorted_array = sort_by_overall_mark(student_array)
        
        # Write results to file
        write_results(sorted_array, output_file)
        
        # Display statistics
        display_statistics(sorted_array)
        
        # Show top 5 students
        print(f"\nTop 5 Students:")
        print("-" * 50)
        print("Rank Reg. Number   Exam   Coursework  Overall  Grade")
        print("-" * 50)
        for i, student in enumerate(sorted_array[:5]):
            print(f"{i+1:2d}   {student['registration']:<12} {student['exam']:5.1f}  "
                  f"{student['coursework']:9.1f}   {student['overall']:6.1f}    {student['grade']}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please make sure the input file exists.")
        print("Current directory contents:")
        try:
            files = os.listdir('.')
            for file in files:
                print(f"  {file}")
        except:
            print("  Unable to list directory contents")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()