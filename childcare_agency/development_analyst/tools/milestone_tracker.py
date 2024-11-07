from agency_swarm.tools import BaseTool
from pydantic import Field
import json
import os
from datetime import datetime

class MilestoneTracker(BaseTool):
    """
    Tool zum Tracking und zur Analyse von Entwicklungsmeilensteinen bei Kindern.
    """
    
    child_id: str = Field(
        ..., 
        description="Eindeutige ID des Kindes"
    )
    
    milestone_category: str = Field(
        ...,
        description="Entwicklungsbereich (z.B. 'motorisch', 'sprachlich', 'sozial', 'kognitiv')"
    )
    
    milestone_data: dict = Field(
        ...,
        description="Daten zum Entwicklungsmeilenstein (erreicht/nicht erreicht, Datum, Bemerkungen)"
    )

    def run(self):
        """
        Erfasst und analysiert Entwicklungsmeilensteine eines Kindes.
        """
        try:
            # Verzeichnisstruktur erstellen
            base_dir = "development_data"
            child_dir = os.path.join(base_dir, self.child_id)
            os.makedirs(child_dir, exist_ok=True)
            
            # Dateiname für Meilensteine
            milestone_file = os.path.join(child_dir, f"milestones_{self.milestone_category}.json")
            
            # Bestehende Daten laden oder neue erstellen
            if os.path.exists(milestone_file):
                with open(milestone_file, 'r', encoding='utf-8') as f:
                    milestones = json.load(f)
            else:
                milestones = []
            
            # Neue Daten hinzufügen
            self.milestone_data['timestamp'] = datetime.now().isoformat()
            milestones.append(self.milestone_data)
            
            # Daten speichern
            with open(milestone_file, 'w', encoding='utf-8') as f:
                json.dump(milestones, f, indent=2, ensure_ascii=False)
            
            # Analyse der Entwicklung
            analysis = self._analyze_progress(milestones)
            
            return analysis
            
        except Exception as e:
            return f"Fehler beim Milestone-Tracking: {str(e)}"
    
    def _analyze_progress(self, milestones):
        """
        Analysiert den Entwicklungsfortschritt basierend auf den Meilensteinen.
        """
        total_milestones = len(milestones)
        achieved_milestones = sum(1 for m in milestones if m.get('achieved', False))
        
        analysis = f"Entwicklungsanalyse für {self.child_id} - {self.milestone_category}:\n\n"
        analysis += f"Gesamtzahl Meilensteine: {total_milestones}\n"
        analysis += f"Erreichte Meilensteine: {achieved_milestones}\n"
        analysis += f"Fortschritt: {(achieved_milestones/total_milestones)*100:.1f}%\n\n"
        
        # Letzte Entwicklungen
        analysis += "Letzte Entwicklungen:\n"
        for milestone in sorted(milestones, key=lambda x: x['timestamp'], reverse=True)[:3]:
            analysis += f"- {milestone.get('description', 'N/A')} "
            analysis += f"({'erreicht' if milestone.get('achieved') else 'nicht erreicht'})\n"
        
        return analysis

if __name__ == "__main__":
    sample_milestone = {
        "description": "Kann frei gehen",
        "achieved": True,
        "age_months": 15,
        "notes": "Sicherer Gang, gute Balance"
    }
    
    tool = MilestoneTracker(
        child_id="MM001",
        milestone_category="motorisch",
        milestone_data=sample_milestone
    )
    print(tool.run()) 