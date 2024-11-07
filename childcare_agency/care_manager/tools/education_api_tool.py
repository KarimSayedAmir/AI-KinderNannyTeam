from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("EDUCATION_API_KEY")
API_ENDPOINT = "https://api.education.example.com/v1"  # Beispiel-API-Endpoint

class EducationAPITool(BaseTool):
    """
    Tool zur Abfrage und Analyse pädagogischer Modelle und Strategien über eine
    spezialisierte Bildungs-API.
    """
    
    query: str = Field(
        ..., 
        description="Suchanfrage für pädagogische Modelle oder Strategien"
    )
    
    age_group: str = Field(
        ..., 
        description="Zielgruppen-Altersbereich (z.B. '3-6 Jahre')"
    )
    
    category: str = Field(
        default="all",
        description="Spezifische Kategorie der pädagogischen Strategie"
    )

    def run(self):
        """
        Führt die API-Abfrage durch und verarbeitet die Ergebnisse.
        """
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        params = {
            "query": self.query,
            "age_group": self.age_group,
            "category": self.category
        }
        
        try:
            response = requests.get(
                f"{API_ENDPOINT}/educational-models",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Formatierte Ausgabe der Ergebnisse
            result = "Gefundene pädagogische Modelle und Strategien:\n\n"
            for model in data.get("models", []):
                result += f"- {model['name']}\n"
                result += f"  Beschreibung: {model['description']}\n"
                result += f"  Altersgruppe: {model['age_group']}\n"
                result += f"  Effektivität: {model['effectiveness_rating']}/5\n\n"
            
            return result
            
        except requests.exceptions.RequestException as e:
            return f"Fehler bei der API-Abfrage: {str(e)}"

if __name__ == "__main__":
    tool = EducationAPITool(
        query="Montessori Methoden",
        age_group="3-6 Jahre",
        category="cognitive_development"
    )
    print(tool.run()) 