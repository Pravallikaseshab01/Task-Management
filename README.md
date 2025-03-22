# Simple Task Management System

## Introduction
The **Simple Task Management System** is a lightweight and user-friendly application that allows users to manage tasks efficiently by adding, listing, removing, and prioritizing them. The system includes a basic machine learning model to recommend high-priority tasks based on previous data. The application is built using **Streamlit** for the user interface and **Python** for backend logic.

## Features
- **Add Tasks**: Users can add tasks along with priority levels (Low, Medium, High).
- **View Tasks**: Displays tasks in a table, sorted by priority.
- **Remove Tasks**: Allows users to delete tasks based on their index.
- **Task Recommendation**: Provides recommendations for high-priority tasks using a Naïve Bayes classification model.
- **Persistent Storage**: Tasks are saved in a CSV file (`tasks.csv`) for future reference.

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **Machine Learning**: Scikit-learn (TfidfVectorizer, Naïve Bayes classifier)
- **Data Storage**: CSV file (tasks.csv)

## Project Structure
```
Simple Task Management System/
│── main.py            # Main application file
│── tasks.csv          # Stores task data
│── requirements.txt   # Dependencies
```

## File Descriptions
### 1. `main.py`
The core logic of the application is implemented in `main.py`. It consists of:
- **TaskManager Class**: Handles task operations such as adding, removing, listing, and recommending tasks.
- **Machine Learning Model**: Uses TF-IDF vectorization and Naïve Bayes classifier to suggest high-priority tasks.
- **Streamlit UI**: Provides an interactive interface for managing tasks.

#### Key Functions:
- `_load_tasks()`: Loads tasks from `tasks.csv`.
- `_update_priority_numeric()`: Encodes priority labels into numeric values.
- `_save_tasks()`: Saves tasks back to `tasks.csv`.
- `_train_model()`: Trains a Naïve Bayes classifier for task recommendation.
- `add_task(description, priority)`: Adds a task to the list and updates storage.
- `remove_task(index)`: Removes a task by index.
- `list_tasks()`: Displays tasks sorted by priority.
- `recommend_task()`: Suggests a high-priority task based on trained model.

### 2. `tasks.csv`
A CSV file that stores task details in the following format:
```
description,priority,priority_numeric
complete reading the novel,Low,1
Submit the assignment,Medium,2
take medicines,High,0
```

## Installation & Setup
### 1. Clone the Repository
```
git clone https://github.com/your-repo/simple-task-manager.git
cd simple-task-manager
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Run the Application
```
streamlit run main.py
```

## Usage Guide
1. **Adding a Task**
   - Enter task description.
   - Select priority (Low, Medium, High).
   - Click `Add Task`.

2. **Viewing Tasks**
   - Tasks are displayed in a table sorted by priority.

3. **Removing a Task**
   - Enter the task index.
   - Click `Remove Task`.

4. **Getting Task Recommendations**
   - Click `Get Recommendation`.
   - The system suggests the most critical task based on priority.

## Future Enhancements
- **Database Integration**: Replace CSV with a database (SQLite/PostgreSQL) for better scalability.
- **User Authentication**: Allow multiple users to manage tasks independently.
- **Improved AI Model**: Use deep learning models for better task prioritization.

Conclusion
This Simple Task Management System is a powerful tool for managing and prioritizing tasks with an intuitive interface. The integration of machine learning* for task recommendations enhances productivity, making it a practical solution for personal or small-scale task management needs.

This is the deployment link to check how the code works:
https://the-task-tracker.streamlit.app/

