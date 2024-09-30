from flask import Flask, jsonify, request, render_template
from datetime import datetime

app = Flask(__name__)

# In-memory database for tasks and completed tasks
tasks = []
completed_tasks = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json
    task['completed'] = False
    task['created_at'] = datetime.now().isoformat()  # Add timestamp
    task['pomodoro_cycles'] = task.get('pomodoro_cycles', 0)  # Optional Pomodoro cycles
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = tasks[task_id]
    task['completed'] = request.json['completed']
    if task['completed']:
        completed_tasks.append(task)  # Track completed tasks
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    del tasks[task_id]
    return '', 204

@app.route('/summary', methods=['GET'])
def get_summary():
    today_tasks = [task for task in completed_tasks if task['created_at'][:10] == datetime.now().isoformat()[:10]]
    task_count = len(today_tasks)
    pomodoro_cycles = sum([task.get('pomodoro_cycles', 0) for task in today_tasks])

    # Basic "AI" functionality: Recommend based on the user's progress
    if task_count == 0:
        tip = "Start small! Try completing at least one task to build momentum."
    elif task_count < 5:
        tip = "Good start! Try breaking down tasks into smaller steps."
    else:
        tip = "Great work! Keep up the productivity with regular breaks."

    return jsonify({
        "tasks_completed": task_count,
        "pomodoro_cycles": pomodoro_cycles,
        "tip": tip
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
