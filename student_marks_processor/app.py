import pandas as pd
import numpy as np
import os

# Function to be used for assigning grade 
def assign_grade_vectorized(marks):
    return np.where(marks >= 70, 'A',
           np.where(marks >= 60, 'B',
           np.where(marks >= 50, 'C',
           np.where(marks >= 40, 'D', 'F'))))

def process_student_marks(input_file, output_file):
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError("Input CSV file not found.")

        # Reading data from .CSV file 
        df = pd.read_csv(input_file)

        # Checking for required columns
        if not {'RegNo', 'ExamMark', 'CourseworkMark'}.issubset(df.columns):
            raise ValueError("Missing required columns in CSV.")

        # Converting to float data type
        df['ExamMark'] = pd.to_numeric(df['ExamMark'], errors='coerce')
        df['CourseworkMark'] = pd.to_numeric(df['CourseworkMark'], errors='coerce')

        if df[['ExamMark', 'CourseworkMark']].isnull().any().any():
            raise ValueError("Non-numeric or missing values found in marks.")

        # Computing  overall marks 
        # inline weights: 70%(0.7) exam, 30%(0.3) coursework
        exam = df['ExamMark'].to_numpy()
        coursework = df['CourseworkMark'].to_numpy()
        overall = (exam * 0.7 + coursework * 0.3).round(2)

        # Assigning grades to students 
        grades = assign_grade_vectorized(overall)

        # Creating a structured NumPy array
        reg_nos = df['RegNo'].to_numpy()
        dtype = [('RegNo', 'U20'), ('ExamMark', 'f4'), ('CourseworkMark', 'f4'),
                 ('OverallMark', 'f4'), ('Grade', 'U2')]
        records = list(zip(reg_nos, exam, coursework, overall, grades))
        structured_array = np.array(records, dtype=dtype)

        #Sorting by OverallMark in descending order 
        sorted_array = np.sort(structured_array, order='OverallMark')[::-1]

        # Writing the data from df to the .csv file
        # creates a new file and writes the data   
        output_df = pd.DataFrame(sorted_array)
        output_df.to_csv(output_file, index=False)
        print(f"Results saved to: {output_file}")

        # Grade statistics
        print("\nGrade Statistics:")
        print(output_df['Grade'].value_counts().sort_index().to_string())

    except Exception as e:
        print("Error:", e)

# Main inputs 
input_file = "marks_input.csv"
output_file = "marks_output.csv"
# Calling the main function 
process_student_marks(input_file, output_file)