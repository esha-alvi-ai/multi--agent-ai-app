# agents/planner.py
import time
from typing import Any, Dict, Optional

class AgentAdapter:
    """
    Lightweight adapter to give different agent implementations a common interface:
        agent_adapter.run(input_text, context=None) -> str
    It attempts common method names used in the project (run, summarize, generate_article, sanitize_text).
    """
    def __init__(self, agent_obj):
        self.agent = agent_obj

    def run(self, input_text: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Try several common method names for agents. The first existing method will be called.
        Passes context as an extra argument if the target method accepts it.
        """
        # Preferred method names & signatures (from our codebase)
        # - run(instruction, context=None)
        # - summarize(text)
        # - generate_article(prompt, tone, length) OR generate_article(prompt)
        # - sanitize_text(text)
        # - write(text) or write(text, context)
        method_candidates = [
            ("run", (input_text, context)),
            ("execute", (input_text,)),
            ("process", (input_text,)),
            ("summarize", (input_text,)),
            ("sanitize_text", (input_text,)),
            ("generate_article", (input_text,)),
            ("write", (input_text,)),
            ("create", (input_text,))
        ]

        for method_name, args in method_candidates:
            if hasattr(self.agent, method_name):
                method = getattr(self.agent, method_name)
                try:
                    # Try calling with both args (some methods ignore extra args)
                    return method(*[a for a in args if a is not None])
                except TypeError:
                    # Fallback: call with only the primary input_text if the method signature differs
                    try:
                        return method(input_text)
                    except Exception as e:
                        raise

        raise AttributeError(f"No supported execution method found on agent {self.agent!r}")
class Planner:
    def __init__(self, writer_agent, sanitizer_agent, summarizer_agent, memory_manager=None, logger=None, pause_between_steps: float = 0.3):
        self.writer = AgentAdapter(writer_agent)
        self.sanitizer = AgentAdapter(sanitizer_agent)
        self.summarizer = AgentAdapter(summarizer_agent)
        self.memory = memory_manager
        self.logger = logger
        self.pause = pause_between_steps

    def execute_plan(self, goal: str) -> Dict[str, str]:
        if not goal:
            raise ValueError("Goal must be a non-empty string.")

        # 🔹 Get past context
        past_context = ""
        if self.memory:
            past_memories = self.memory.search("long", goal)
            if past_memories:
                past_context = "\n\nPast relevant notes:\n" + "\n".join(m["content"] for _, m in past_memories)

        plan = self.plan_tasks(goal)
        stage_outputs = {}
        current_input = None

        for step in plan:
            agent_key = step["agent"]
            instruction = step["instruction"]

            if agent_key == "writer":
                adapter = self.writer
                call_input = instruction + past_context
            elif agent_key == "sanitizer":
                adapter = self.sanitizer
                call_input = current_input
            elif agent_key == "summarizer":
                adapter = self.summarizer
                call_input = current_input
            else:
                raise KeyError(f"Unknown agent key: {agent_key}")

            time.sleep(self.pause)
            output = adapter.run(call_input)

            # 🔹 Store stage output in short-term memory
            if self.memory:
                self.memory.store("short", output)

            stage_outputs[agent_key] = output
            current_input = output

        # 🔹 Store final summary in long-term memory
        if self.memory:
            self.memory.store("long", stage_outputs.get("summarizer", ""), tags=[goal])

        return {
            "goal": goal,
            "writer_output": stage_outputs.get("writer", ""),
            "sanitizer_output": stage_outputs.get("sanitizer", ""),
            "summary_output": stage_outputs.get("summarizer", "")
        }
