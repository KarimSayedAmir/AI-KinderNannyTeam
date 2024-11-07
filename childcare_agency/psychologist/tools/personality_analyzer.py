from agency_swarm.tools import BaseTool
from pydantic import Field
import json
import os
from datetime import datetime
import pandas as pd

class PersonalityAnalyzer(BaseTool):
    """
    Tool zur Analyse und Dokumentation von Persönlichkeitsmerkmalen und
    charakterlichen Eigenschaften der Kinder.
    """
    
    child_id: str = Field(
        ..., 
        description="Eindeutige ID des Kindes"
    )
    
    observation_data: dict = Field(
        ...,
        description="Beobachtungsdaten zu Persönlichkeitsmerkmalen"
    )
    
    analysis_context: str = Field(
        default="general",
        description="Kontext der Analyse (z.B. 'general', 'social', 'learning')"
    )

    def run(self):
        """
        Führt eine umfassende Persönlichkeitsanalyse durch und erstellt einen Bericht.
        """
        try:
            # Daten speichern
            self._save_observation_data()
            
            # Analyse durchführen
            personality_profile = self._create_personality_profile()
            
            # Empfehlungen generieren
            recommendations = self._generate_recommendations()
            
            # Gesamtbericht erstellen
            report = "Persönlichkeitsanalyse:\n\n"
            report += personality_profile + "\n"
            report += recommendations
            
            return report
            
        except Exception as e:
            return f"Fehler bei der Persönlichkeitsanalyse: {str(e)}"
    
    def _save_observation_data(self):
        """
        Speichert die Beobachtungsdaten in einer strukturierten Form.
        """
        base_dir = os.path.join("psychological_data", self.child_id)
        os.makedirs(base_dir, exist_ok=True)
        
        # Dateiname basierend auf Datum und Kontext
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(base_dir, f"personality_{self.analysis_context}_{timestamp}.json")
        
        # Daten mit Zeitstempel speichern
        data_to_save = {
            "timestamp": datetime.now().isoformat(),
            "context": self.analysis_context,
            "observations": self.observation_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)
    
    def _create_personality_profile(self):
        """
        Erstellt ein detailliertes Persönlichkeitsprofil basierend auf den Beobachtungen.
        """
        profile = f"Persönlichkeitsprofil für {self.child_id}:\n\n"
        
        # Temperament und Grundstimmung
        temperament = self.observation_data.get('temperament', {})
        profile += "Temperament und Grundstimmung:\n"
        for aspect, value in temperament.items():
            profile += f"- {aspect}: {value}\n"
        
        # Sozialverhalten
        social = self.observation_data.get('social_behavior', {})
        profile += "\nSozialverhalten:\n"
        for behavior, observation in social.items():
            profile += f"- {behavior}: {observation}\n"
        
        # Lernverhalten
        learning = self.observation_data.get('learning_style', {})
        profile += "\nLernverhalten:\n"
        for style, characteristic in learning.items():
            profile += f"- {style}: {characteristic}\n"
        
        return profile
    
    def _generate_recommendations(self):
        """
        Generiert personalisierte Empfehlungen basierend auf dem Persönlichkeitsprofil.
        """
        recommendations = "\nEmpfehlungen:\n\n"
        
        # Empfehlungen basierend auf Temperament
        temperament = self.observation_data.get('temperament', {})
        if 'activity_level' in temperament:
            if temperament['activity_level'] == 'hoch':
                recommendations += "- Bewegungsreiche Aktivitäten anbieten\n"
                recommendations += "- Ruhephasen strukturiert einplanen\n"
            elif temperament['activity_level'] == 'niedrig':
                recommendations += "- Sanfte Aktivierung durch spielerische Anreize\n"
                recommendations += "- Ausreichend Zeit für eigenes Tempo einräumen\n"
        
        # Empfehlungen für soziale Interaktion
        social = self.observation_data.get('social_behavior', {})
        if 'group_interaction' in social:
            if social['group_interaction'] == 'zurückhaltend':
                recommendations += "- Kleingruppenaktivitäten bevorzugen\n"
                recommendations += "- Schrittweise an größere Gruppen heranführen\n"
            elif social['group_interaction'] == 'dominant':
                recommendations += "- Soziale Kompetenzen durch Rollenspiele fördern\n"
                recommendations += "- Empathie-fördernde Aktivitäten einbauen\n"
        
        return recommendations

if __name__ == "__main__":
    sample_data = {
        "temperament": {
            "activity_level": "hoch",
            "adaptability": "gut",
            "emotional_intensity": "moderat"
        },
        "social_behavior": {
            "group_interaction": "aktiv",
            "cooperation": "gut",
            "conflict_resolution": "konstruktiv"
        },
        "learning_style": {
            "attention_span": "mittel",
            "interest_areas": ["kreativ", "bewegung"],
            "preferred_learning_method": "hands-on"
        }
    }
    
    tool = PersonalityAnalyzer(
        child_id="MM001",
        observation_data=sample_data,
        analysis_context="general"
    )
    print(tool.run()) 