from agency_swarm import Agent
from .tools.personality_analyzer import PersonalityAnalyzer
from .tools.behavior_recorder import BehaviorRecorder
from .tools.emotion_analyzer import EmotionAnalyzer

class Psychologist(Agent):
    def __init__(self):
        super().__init__(
            name="Psychologe",
            description="Verantwortlich für die psychologische Betreuung und Analyse der Kinder.",
            instructions="./instructions.md",
            tools=[PersonalityAnalyzer, BehaviorRecorder, EmotionAnalyzer],
            temperature=0.7,
            max_prompt_tokens=2000
        ) 