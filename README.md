# Student Group Assignment Solver

## Overview
The Student Group Assignment Solver is a system designed to optimally assign students to their desired elective subjects and corresponding groups while satisfying multiple constraints. It leverages MiniZinc for constraint solving and Python with FastAPI for handling HTTP requests.

## Features
* 🎯 **Student Preferences**: Takes into account students' choices regarding elective subjects.
* 👨‍🏫 **Instructor Workload**: Ensures instructors do not exceed their maximum allowed teaching hours per term.
* 👥 **Group Size Constraints**: Maintains minimum and maximum student limits per group depending on subject type.
* 🔓 **Forced Assignments**: Allows certain subjects to be opened regardless of student preferences.
* ✒️ **Manual Overrides**: Enables assigning specific students to particular subjects/groups.
* ✈️ **Student Exchange Consideration**: Takes into account students going on exchange programs (they may not appear next term).
* 📅 **Schedule Optimization**: Minimizes scheduling conflicts for future timetable creation.
* 📌 **Division Into Clusters**: Ensures students enroll in the required number of subjects per cluster.
* 🤝 **Friend Preferences**: Allows students to request being grouped with specific peers.

## Tech Stack  
- **Python** – Backend implementation  
- **FastAPI** – API framework for handling requests  
- **MiniZinc** – Constraint programming tool for solving optimization problems  
- **OR-Tools** – Solver used by MiniZinc

## Usage  

**Clone the repository:**  
```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

**Install dependencies:**  
```bash
pip install -r requirements.txt
```

**Install MiniZinc 2.8.5:** https://github.com/MiniZinc/MiniZincIDE/releases/tag/2.8.5

**Run the FastAPI server:**  
```bash
uvicorn main:app --reload
```

**Access the API documentation at:**
http://127.0.0.1:8000/docs
