import streamlit as st
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

class TaskManager:
    def __init__(self, file_name='tasks.csv'):
        self.file_name = file_name
        self.tasks = self._load_tasks()
        self.priority_order = {"High": 3, "Medium": 2, "Low": 1}

    def _load_tasks(self):
        if os.path.exists(self.file_name):
            tasks = pd.read_csv(self.file_name).dropna()
            return tasks
        return pd.DataFrame(columns=['description', 'priority'])

    def _save_tasks(self):
        self.tasks.to_csv(self.file_name, index=False)

    def add_task(self, description, priority):
        priority = priority.capitalize()
        if priority not in ["Low", "Medium", "High"]:
            return "Priority must be Low, Medium, or High"
        
        new_task = pd.DataFrame({'description': [description], 'priority': [priority]})
        self.tasks = pd.concat([self.tasks, new_task], ignore_index=True)
        self._save_tasks()
        return "Task added successfully."

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks = self.tasks.drop(index).reset_index(drop=True)
            self._save_tasks()
            return "Task removed successfully."
        return "Invalid task number."

    def list_tasks(self):
        self.tasks["priority_numeric"] = self.tasks["priority"].map(self.priority_order)
        return self.tasks.sort_values(by=["priority_numeric", self.tasks.index], ascending=[False, True]).reset_index(drop=True)

    def recommend_task(self):
        if self.tasks.empty:
            return "No tasks available for recommendation."
        
        sorted_tasks = self.list_tasks()  # Sorted by priority first, then by order of entry
        return f"Recommended task: {sorted_tasks.iloc[0]['description']}"

# Streamlit UI
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
    st.table(tasks_df.drop(columns=["priority_numeric"]))  # Hide numeric priority
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
