from agency_swarm import Agent
from .tools.milestone_tracker import MilestoneTracker
from .tools.progress_analyzer import ProgressAnalyzer
from .tools.behavior_analyzer import BehaviorAnalyzer

class DevelopmentAnalyst(Agent):
    def __init__(self):
        super().__init__(
            name="Entwicklungsanalyst",
            description="Analysiert und dokumentiert die Entwicklungsfortschritte der Kinder.",
            instructions="./instructions.md",
            tools=[MilestoneTracker, ProgressAnalyzer, BehaviorAnalyzer],
            temperature=0.7,
            max_prompt_tokens=2000
        ) 