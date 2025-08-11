# main.py

import os
import importlib
from config import Config
from base import BaseApp
from logger.logger import setup_logger

logger = setup_logger()

def load_modules_from_folder(folder_path, package_name):
    """Dynamically import all Python modules from a given folder."""
    modules = {}
    if not os.path.exists(folder_path):
        logger.warning(f"Folder '{folder_path}' does not exist.")
        return modules

    for filename in os.listdir(folder_path):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f"{package_name}.{module_name}")
                modules[module_name] = module
                logger.info(f"Loaded: {package_name}.{module_name}")
            except Exception as e:
                logger.error(f"Error loading {package_name}.{module_name}: {e}")
    return modules


def build_task_graph(validators, controllers, agents):
    """
    Build a simple execution order based on known dependencies.
    In a full system, this could be dynamic from a config or planner.
    """
    task_graph = [
        ("planner", "create_plan", {"topic": "The Future of AI in 2025"}),
        ("writer", "generate_article", {}),
        ("sanitizer", "sanitizer_text", {}),
        ("summarizer", "summarize", {}),
    ]
    return task_graph


def execute_task_graph(task_graph, agents, validators):
    """
    Execute the task graph step-by-step, passing output between steps.
    """
    result = None
    for step_name, method_name, params in task_graph:
        try:
            if step_name in agents:
                obj = agents[step_name]
            elif step_name in validators:
                obj = validators[step_name]
            else:
                logger.warning(f"Step {step_name} not found.")
                continue

            cls = None
            if hasattr(obj, method_name):
                # Direct function
                func = getattr(obj, method_name)
            else:
                # If it's a class, create an instance
                class_candidates = [getattr(obj, attr) for attr in dir(obj) if isinstance(getattr(obj, attr), type)]
                if class_candidates:
                    cls = class_candidates[0]()  # Instantiate first found class
                    func = getattr(cls, method_name)
                else:
                    logger.warning(f"No callable {method_name} in {step_name}")
                    continue

            if result is not None:
                params = {**params, list(params.keys())[0] if params else "input_text": result}

            result = func(**params)
            logger.info(f"{step_name}.{method_name} executed successfully.")

        except Exception as e:
            logger.error(f"Error executing {step_name}.{method_name}: {e}")
            break

    return result

def run_pipeline(topic: str, tone: str, length: str) -> dict:
    # returns something like:
    return {
        "plan": "...",
        "final_article": "...",
        "summary": "..."
    }

def main():
    logger.info("🚀 Multi-Agent AI App Starting...")

    config = Config()
    app = BaseApp(config)

    base_path = os.path.dirname(__file__)
    agents_path = os.path.join(base_path, "agents")
    validators_path = os.path.join(agents_path, "validators")
    controller_path = os.path.join(agents_path, "controller")

    validators = load_modules_from_folder(validators_path, "agents.validators")
    controllers = load_modules_from_folder(controller_path, "agents.controller")
    agent_core = load_modules_from_folder(agents_path, "agents")

    # Instantiate classes for agents and validators
    agent_instances = {}
    for name, module in agent_core.items():
        class_candidates = [getattr(module, attr) for attr in dir(module) if isinstance(getattr(module, attr), type)]
        if class_candidates:
            agent_instances[name] = class_candidates[0]()  # first found class

    validator_instances = {}
    for name, module in validators.items():
        class_candidates = [getattr(module, attr) for attr in dir(module) if isinstance(getattr(module, attr), type)]
        if class_candidates:
            validator_instances[name] = class_candidates[0]()

    # Build and execute the task graph
    task_graph = build_task_graph(validator_instances, controllers, agent_instances)
    final_output = execute_task_graph(task_graph, agent_instances, validator_instances)

    logger.info("✅ Final Output:")
    logger.info(final_output)

    logger.info("🏁 Multi-Agent AI App Finished.")


if __name__ == "__main__":
    main()
