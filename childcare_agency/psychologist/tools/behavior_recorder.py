from agency_swarm.tools import BaseTool
from pydantic import Field
import json
import os
from datetime import datetime
import pandas as pd

class BehaviorRecorder(BaseTool):
    """
    Tool zur detaillierten Aufzeichnung und Analyse von Verhaltensweisen,
    emotionalen Reaktionen und sozialen Interaktionen.
    """
    
    child_id: str = Field(
        ..., 
        description="Eindeutige ID des Kindes"
    )
    
    behavior_record: dict = Field(
        ...,
        description="Detaillierte Verhaltensdokumentation"
    )
    
    observation_setting: str = Field(
        default="regular",
        description="Beobachtungskontext (z.B. 'regular', 'special_situation', 'conflict')"
    )

    def run(self):
        """
        Zeichnet Verhaltensbeobachtungen auf und erstellt eine strukturierte Analyse.
        """
        try:
            # Aufzeichnung speichern
            self._save_behavior_record()
            
            # Verhaltensanalyse durchführen
            behavior_analysis = self._analyze_behavior()
            
            # Muster identifizieren
            patterns = self._identify_patterns()
            
            # Empfehlungen erstellen
            recommendations = self._create_recommendations()
            
            # Gesamtbericht zusammenstellen
            report = "Verhaltensaufzeichnung und Analyse:\n\n"
            report += behavior_analysis + "\n"
            report += patterns + "\n"
            report += recommendations
            
            return report
            
        except Exception as e:
            return f"Fehler bei der Verhaltensaufzeichnung: {str(e)}"
    
    def _save_behavior_record(self):
        """
        Speichert die Verhaltensaufzeichnung strukturiert ab.
        """
        base_dir = os.path.join("psychological_data", self.child_id, "behavior_records")
        os.makedirs(base_dir, exist_ok=True)
        
        # Dateiname mit Zeitstempel und Kontext
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(base_dir, f"behavior_{self.observation_setting}_{timestamp}.json")
        
        # Daten mit Metainformationen speichern
        data_to_save = {
            "timestamp": datetime.now().isoformat(),
            "setting": self.observation_setting,
            "record": self.behavior_record
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)
    
    def _analyze_behavior(self):
        """
        Analysiert die aufgezeichneten Verhaltensweisen.
        """
        analysis = "Verhaltensanalyse:\n\n"
        
        # Emotionale Reaktionen
        emotions = self.behavior_record.get('emotional_reactions', {})
        analysis += "Emotionale Reaktionen:\n"
        for situation, reaction in emotions.items():
            analysis += f"- {situation}: {reaction}\n"
        
        # Soziale Interaktionen
        interactions = self.behavior_record.get('social_interactions', {})
        analysis += "\nSoziale Interaktionen:\n"
        for interaction_type, details in interactions.items():
            analysis += f"- {interaction_type}: {details}\n"
        
        # Konfliktverhalten
        conflicts = self.behavior_record.get('conflict_behavior', {})
        if conflicts:
            analysis += "\nKonfliktverhalten:\n"
            for conflict, response in conflicts.items():
                analysis += f"- {conflict}: {response}\n"
        
        return analysis
    
    def _identify_patterns(self):
        """
        Identifiziert wiederkehrende Verhaltensmuster.
        """
        patterns = "\nIdentifizierte Verhaltensmuster:\n\n"
        
        # Emotionale Muster
        if 'emotional_patterns' in self.behavior_record:
            patterns += "Emotionale Muster:\n"
            for pattern, frequency in self.behavior_record['emotional_patterns'].items():
                patterns += f"- {pattern}: {frequency}\n"
        
        # Interaktionsmuster
        if 'interaction_patterns' in self.behavior_record:
            patterns += "\nInteraktionsmuster:\n"
            for pattern, frequency in self.behavior_record['interaction_patterns'].items():
                patterns += f"- {pattern}: {frequency}\n"
        
        return patterns
    
    def _create_recommendations(self):
        """
        Erstellt Handlungsempfehlungen basierend auf der Verhaltensanalyse.
        """
        recommendations = "\nHandlungsempfehlungen:\n\n"
        
        # Emotionale Unterstützung
        emotions = self.behavior_record.get('emotional_reactions', {})
        for situation, reaction in emotions.items():
            if 'überwältigt' in reaction.lower():
                recommendations += f"- Bei {situation}: Beruhigungsstrategien anbieten\n"
            elif 'unsicher' in reaction.lower():
                recommendations += f"- Bei {situation}: Mehr Bestätigung und Unterstützung geben\n"
        
        # Soziale Förderung
        interactions = self.behavior_record.get('social_interactions', {})
        for interaction_type, details in interactions.items():
            if 'zurückhaltend' in details.lower():
                recommendations += f"- {interaction_type}: Sanfte Ermutigung zur Teilnahme\n"
            elif 'konflikt' in details.lower():
                recommendations += f"- {interaction_type}: Konfliktlösungsstrategien üben\n"
        
        return recommendations

if __name__ == "__main__":
    sample_record = {
        "emotional_reactions": {
            "Gruppenspiel": "anfangs zurückhaltend, dann begeistert",
            "Konfliktsituation": "leicht frustriert, sucht Unterstützung"
        },
        "social_interactions": {
            "Peer-Kontakte": "selektiv, bevorzugt kleinere Gruppen",
            "Erwachsenen-Interaktion": "offen und vertrauensvoll"
        },
        "emotional_patterns": {
            "Rückzug bei Überforderung": "gelegentlich",
            "Positive Grundstimmung": "häufig"
        },
        "interaction_patterns": {
            "Sucht Einzelspiel": "regelmäßig",
            "Aktive Gruppenpartizipation": "zunehmend"
        }
    }
    
    tool = BehaviorRecorder(
        child_id="MM001",
        behavior_record=sample_record,
        observation_setting="regular"
    )
    print(tool.run()) 