
import streamlit as st
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class TaskManager:
    def __init__(self, file_name='tasks.csv'):
        self.file_name = file_name
        self.tasks = self._load_tasks()
        self.label_encoder = LabelEncoder()
        self._update_priority_numeric()
        self.model = self._train_model()

    def _load_tasks(self):
        if os.path.exists(self.file_name):
            tasks = pd.read_csv(self.file_name).dropna()
            return tasks
        return pd.DataFrame(columns=['description', 'priority'])

    def _update_priority_numeric(self):
        if not self.tasks.empty:
            self.tasks['priority_numeric'] = self.label_encoder.fit_transform(self.tasks['priority'])
        else:
            self.tasks['priority_numeric'] = pd.Series(dtype=int)

    def _save_tasks(self):
        self.tasks.to_csv(self.file_name, index=False)

    def _train_model(self):
        if len(self.tasks) > 1:
            X = self.tasks['description']
            y = self.tasks['priority_numeric']
            X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
            model = make_pipeline(TfidfVectorizer(), MultinomialNB())
            model.fit(X_train, y_train)
            return model
        return None

    def add_task(self, description, priority):
        priority = priority.capitalize()
        if priority not in ['Low', 'Medium', 'High']:
            return "Priority must be Low, Medium, or High"
        
        new_task = pd.DataFrame({'description': [description], 'priority': [priority]})
        self.tasks = pd.concat([self.tasks, new_task], ignore_index=True)
        self._update_priority_numeric()
        self._save_tasks()
        self.model = self._train_model()
        return "Task added successfully."

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks = self.tasks.drop(index).reset_index(drop=True)
            self._update_priority_numeric()
            self._save_tasks()
            self.model = self._train_model()
            return "Task removed successfully."
        return "Invalid task number."

    def list_tasks(self):
        return self.tasks.sort_values(by='priority_numeric', ascending=False).reset_index(drop=True)

    def recommend_task(self):
        if self.tasks.empty or self.model is None or len(self.tasks) < 2:
            return "Not enough data for recommendations."
        high_priority_tasks = self.tasks[self.tasks['priority'] == 'High']
        if not high_priority_tasks.empty:
            predictions = self.model.predict_proba(self.tasks['description'])
            high_priority_prob = predictions[:, self.label_encoder.transform(['High'])[0]]
            recommended_index = high_priority_prob.argmax()
            return f"Recommended task: {self.tasks.iloc[recommended_index]['description']}"
        return "No high-priority tasks available."

st.set_page_config(page_title="Task Manager", layout="wide")
st.title("📋 Task Management System")

task_manager = TaskManager()

# Sidebar
st.sidebar.header("Manage Tasks")
description = st.sidebar.text_input("Task Description")
priority = st.sidebar.selectbox("Priority", ["Low", "Medium", "High"])
if st.sidebar.button("Add Task"):
    st.sidebar.success(task_manager.add_task(description, priority))

# Main Display
st.header("Task List")
tasks_df = task_manager.list_tasks()
if not tasks_df.empty:
    st.table(tasks_df)
else:
    st.info("No tasks available.")

# Task Removal
st.sidebar.subheader("Remove Task")
if not tasks_df.empty:
    task_index = st.sidebar.number_input("Enter task number to remove", min_value=0, max_value=len(tasks_df)-1, step=1)
    if st.sidebar.button("Remove Task"):
        st.sidebar.success(task_manager.remove_task(task_index))

# Task Recommendation
st.subheader("Task Recommendation")
if st.button("Get Recommendation"):
    st.write(task_manager.recommend_task())
