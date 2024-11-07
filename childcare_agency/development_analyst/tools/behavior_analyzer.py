from agency_swarm.tools import BaseTool
from pydantic import Field
import pandas as pd
import numpy as np
from datetime import datetime
import os
import json

class BehaviorAnalyzer(BaseTool):
    """
    Tool zur Analyse von Verhaltensmustern und Stimmungen.
    """
    
    child_id: str = Field(
        ..., 
        description="Eindeutige ID des Kindes"
    )
    
    behavior_data: dict = Field(
        ...,
        description="Verhaltensdaten (Aktivität, Stimmung, Interaktionen)"
    )
    
    analysis_type: str = Field(
        default="daily",
        description="Art der Analyse (daily/weekly/monthly)"
    )

    def run(self):
        """
        Analysiert Verhaltensmuster und erstellt einen detaillierten Bericht.
        """
        try:
            # Daten speichern
            self._save_behavior_data()
            
            # Analyse durchführen
            analysis_result = self._analyze_behavior()
            
            # Muster erkennen
            patterns = self._identify_patterns()
            
            # Gesamtbericht erstellen
            report = "Verhaltensanalyse:\n\n"
            report += analysis_result + "\n"
            report += patterns
            
            return report
            
        except Exception as e:
            return f"Fehler bei der Verhaltensanalyse: {str(e)}"
    
    def _save_behavior_data(self):
        """
        Speichert neue Verhaltensdaten.
        """
        base_dir = os.path.join("development_data", self.child_id, "behavior")
        os.makedirs(base_dir, exist_ok=True)
        
        # Dateiname basierend auf Datum
        date_str = datetime.now().strftime("%Y%m")
        filename = os.path.join(base_dir, f"behavior_{date_str}.json")
        
        # Bestehende Daten laden oder neue erstellen
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        else:
            existing_data = []
        
        # Neue Daten hinzufügen
        self.behavior_data['timestamp'] = datetime.now().isoformat()
        existing_data.append(self.behavior_data)
        
        # Daten speichern
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
    
    def _analyze_behavior(self):
        """
        Analysiert die Verhaltensdaten und erstellt eine Zusammenfassung.
        """
        analysis = f"Verhaltensanalyse für {self.child_id}:\n\n"
        
        # Stimmungsanalyse
        mood = self.behavior_data.get('mood', 'neutral')
        analysis += f"Aktuelle Stimmung: {mood}\n"
        
        # Aktivitätsanalyse
        activities = self.behavior_data.get('activities', [])
        if activities:
            analysis += "\nAktivitäten:\n"
            for activity in activities:
                analysis += f"- {activity['name']}: {activity['duration']} Minuten\n"
        
        # Interaktionsanalyse
        interactions = self.behavior_data.get('interactions', [])
        if interactions:
            analysis += "\nSoziale Interaktionen:\n"
            for interaction in interactions:
                analysis += f"- {interaction['type']}: {interaction['quality']}\n"
        
        return analysis
    
    def _identify_patterns(self):
        """
        Identifiziert Verhaltensmuster über Zeit.
        """
        patterns = "\nErkannte Muster:\n"
        
        # Stimmungsmuster
        if 'mood_history' in self.behavior_data:
            mood_freq = pd.Series(self.behavior_data['mood_history']).value_counts()
            patterns += f"\nHäufigste Stimmungen:\n"
            for mood, count in mood_freq.items():
                patterns += f"- {mood}: {count} mal\n"
        
        # Aktivitätsmuster
        if 'activity_history' in self.behavior_data:
            activity_freq = pd.Series([a['name'] for a in self.behavior_data['activity_history']]).value_counts()
            patterns += f"\nBevorzugte Aktivitäten:\n"
            for activity, count in activity_freq.items():
                patterns += f"- {activity}: {count} mal\n"
        
        return patterns

if __name__ == "__main__":
    sample_data = {
        "mood": "fröhlich",
        "activities": [
            {"name": "Malen", "duration": 30},
            {"name": "Bewegungsspiel", "duration": 45}
        ],
        "interactions": [
            {"type": "Gruppenspiel", "quality": "sehr gut"},
            {"type": "Einzelspiel", "quality": "konzentriert"}
        ],
        "mood_history": ["fröhlich", "neutral", "fröhlich", "müde"],
        "activity_history": [
            {"name": "Malen", "duration": 30},
            {"name": "Bewegungsspiel", "duration": 45},
            {"name": "Malen", "duration": 25}
        ]
    }
    
    tool = BehaviorAnalyzer(
        child_id="MM001",
        behavior_data=sample_data,
        analysis_type="daily"
    )
    print(tool.run()) 