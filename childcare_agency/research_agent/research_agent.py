from agency_swarm import Agent
from .tools.education_search import EducationSearch
from .tools.keyword_extractor import KeywordExtractor
from .tools.trend_analyzer import TrendAnalyzer

class ResearchAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Pädagogischer Forschungsagent",
            description="Analysiert pädagogische Forschung und Trends zur Optimierung der Betreuungsqualität.",
            instructions="./instructions.md",
            tools=[EducationSearch, KeywordExtractor, TrendAnalyzer],
            temperature=0.7,
            max_prompt_tokens=2000
        ) 