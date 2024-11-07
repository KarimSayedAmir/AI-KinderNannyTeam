from agency_swarm import Agency
from care_manager.care_manager import CareManager
from research_agent.research_agent import ResearchAgent
from development_analyst.development_analyst import DevelopmentAnalyst
from psychologist.psychologist import Psychologist

# Agenten initialisieren
care_manager = CareManager()
researcher = ResearchAgent()
analyst = DevelopmentAnalyst()
psychologist = Psychologist()

# Agency erstellen mit Kommunikationsflüssen
agency = Agency(
    [
        care_manager,  # Betreuungsmanager als Haupteinstiegspunkt
        [care_manager, researcher],  # Betreuungsmanager kann mit Forschungsagent kommunizieren
        [care_manager, analyst],     # Betreuungsmanager kann mit Entwicklungsanalyst kommunizieren
        [care_manager, psychologist], # Betreuungsmanager kann mit Psychologe kommunizieren
        [analyst, psychologist],      # Entwicklungsanalyst kann mit Psychologe kommunizieren
        [researcher, analyst]         # Forschungsagent kann mit Entwicklungsanalyst kommunizieren
    ],
    shared_instructions="agency_manifesto.md",
    temperature=0.7,
    max_prompt_tokens=2000
)

if __name__ == "__main__":
    agency.run_demo() 