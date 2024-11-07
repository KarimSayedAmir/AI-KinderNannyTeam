from agency_swarm import Agent
from .tools.education_api_tool import EducationAPITool
from .tools.document_manager import DocumentManager

class CareManager(Agent):
    def __init__(self):
        super().__init__(
            name="Betreuungsmanager",
            description="Verantwortlich für die Koordination der Kinderbetreuung und Entwicklung von Betreuungsstrategien.",
            instructions="./instructions.md",
            tools=[EducationAPITool, DocumentManager],
            temperature=0.7,
            max_prompt_tokens=2000
        ) 