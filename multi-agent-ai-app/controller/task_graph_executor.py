from logger.logger import Logger

class TaskGraphExecutor:
    def __init__(self):
        self.logger = Logger(__name__)
        self.task_graph = {}

    def add_task(self, task_id, dependencies=None, func=None):
        """Add a task with optional dependencies."""
        if dependencies is None:
            dependencies = []
        self.task_graph[task_id] = {
            "dependencies": dependencies,
            "func": func,
            "status": "pending"
        }
        self.logger.info(f"Task added: {task_id} with dependencies {dependencies}")

    def execute(self):
        """Execute tasks in dependency order."""
        executed = set()

        def run_task(task_id):
            task = self.task_graph.get(task_id)
            if not task:
                self.logger.error(f"Task '{task_id}' not found.")
                return
            # First run dependencies
            for dep in task["dependencies"]:
                if dep not in executed:
                    run_task(dep)
            # Run the task itself
            if task["func"]:
                self.logger.info(f"Executing task: {task_id}")
                try:
                    task["func"]()
                    task["status"] = "done"
                    executed.add(task_id)
                except Exception as e:
                    self.logger.error(f"Error executing task {task_id}: {e}")
                    task["status"] = "failed"

        for task_id in self.task_graph:
            if task_id not in executed:
                run_task(task_id)

    def reset(self):
        """Reset all tasks to pending state."""
        for task in self.task_graph.values():
            task["status"] = "pending"
        self.logger.info("Task graph reset.")
