from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
import requests

load_dotenv()

EDUCATION_DB_API_KEY = os.getenv("EDUCATION_DB_API_KEY")
API_BASE = "https://api.education-research.example.com/v1"

class EducationSearch(BaseTool):
    """
    Tool zur Recherche in spezialisierten pädagogischen Datenbanken und
    wissenschaftlichen Publikationen.
    """
    
    keywords: str = Field(
        ..., 
        description="Suchbegriffe für die Recherche"
    )
    
    research_type: str = Field(
        default="all",
        description="Art der Forschung (z.B. 'qualitative', 'quantitative', 'meta-analysis')"
    )
    
    publication_year_from: int = Field(
        default=2020,
        description="Frühestes Publikationsjahr"
    )

    def run(self):
        """
        Durchsucht pädagogische Datenbanken und gibt relevante Forschungsergebnisse zurück.
        """
        headers = {
            "Authorization": f"Bearer {EDUCATION_DB_API_KEY}",
            "Content-Type": "application/json"
        }
        
        params = {
            "keywords": self.keywords,
            "type": self.research_type,
            "year_from": self.publication_year_from
        }
        
        try:
            response = requests.get(
                f"{API_BASE}/research",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Formatierte Ausgabe der Forschungsergebnisse
            result = "Aktuelle Forschungsergebnisse:\n\n"
            for study in data.get("studies", []):
                result += f"## {study['title']}\n"
                result += f"Autoren: {study['authors']}\n"
                result += f"Jahr: {study['year']}\n"
                result += f"Methodik: {study['methodology']}\n"
                result += f"Hauptergebnisse: {study['key_findings']}\n\n"
            
            return result
            
        except requests.exceptions.RequestException as e:
            return f"Fehler bei der Forschungsrecherche: {str(e)}"

if __name__ == "__main__":
    tool = EducationSearch(
        keywords="frühkindliche Entwicklung Sprachförderung",
        research_type="meta-analysis",
        publication_year_from=2022
    )
    print(tool.run()) 