"""
model.py - Machine Learning Module for Student Performance Analysis System
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Define feature columns used for training
FEATURE_COLS = [
    'Attendance_Percentage',
    'Study_Hours_Per_Day',
    'Assignment_Score',
    'Internal_Marks',
    'Midterm_Marks',
    'Previous_Semester_GPA',
    'Backlogs'
]

def classify_performance(row):
    """
    Rule-based Performance Classification Logic:
    - High Performance: Final Exam >= 75 AND Attendance >= 80 AND GPA >= 7.5 AND Backlogs == 0
    - Low Performance: Final Exam < 50 OR Attendance < 65 OR Backlogs >= 2
    - Medium Performance: All other students
    """
    if row['Final_Exam_Marks'] >= 75 and row['Attendance_Percentage'] >= 80 and row['Previous_Semester_GPA'] >= 7.5 and row['Backlogs'] == 0:
        return 'High Performance'
    elif row['Final_Exam_Marks'] < 50 or row['Attendance_Percentage'] < 65 or row['Backlogs'] >= 2:
        return 'Low Performance'
    else:
        return 'Medium Performance'

def prepare_data(df):
    """Adds the target column 'Performance_Category' to the DataFrame."""
    df_clean = df.copy()
    if 'Performance_Category' not in df_clean.columns:
        df_clean['Performance_Category'] = df_clean.apply(classify_performance, axis=1)
    return df_clean

def train_model(df):
    """
    Trains a Random Forest Classifier on the student dataset.
    Returns:
        model: Trained Scikit-Learn Model
        accuracy: Model Accuracy Score
        report_df: Classification Report DataFrame
    """
    df_prepared = prepare_data(df)
    
    X = df_prepared[FEATURE_COLS]
    y = df_prepared['Performance_Category']
    
    # Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Initialize Random Forest Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate Model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    report_dict = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report_dict).transpose()
    
    return model, accuracy, report_df

def predict_single_student(model, feature_values):
    """
    Predicts performance category for a single student input dictionary.
    feature_values dict format:
    {
        'Attendance_Percentage': float,
        'Study_Hours_Per_Day': float,
        'Assignment_Score': float,
        'Internal_Marks': float,
        'Midterm_Marks': float,
        'Previous_Semester_GPA': float,
        'Backlogs': int
    }
    """
    input_df = pd.DataFrame([feature_values])[FEATURE_COLS]
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    classes = model.classes_
    
    prob_dict = {classes[i]: round(probabilities[i] * 100, 2) for i in range(len(classes))}
    return prediction, prob_dict