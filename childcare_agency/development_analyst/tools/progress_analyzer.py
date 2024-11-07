from agency_swarm.tools import BaseTool
from pydantic import Field
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import json

class ProgressAnalyzer(BaseTool):
    """
    Tool zur detaillierten Analyse und Visualisierung von Entwicklungsfortschritten.
    """
    
    child_id: str = Field(
        ..., 
        description="Eindeutige ID des Kindes"
    )
    
    analysis_period: str = Field(
        default="6M",
        description="Analysezeitraum (z.B. '3M', '6M', '1Y')"
    )
    
    development_areas: list = Field(
        default=["motorisch", "sprachlich", "sozial", "kognitiv"],
        description="Zu analysierende Entwicklungsbereiche"
    )

    def run(self):
        """
        Führt eine umfassende Analyse der Entwicklungsfortschritte durch.
        """
        try:
            # Daten sammeln
            all_data = self._collect_development_data()
            
            # Analyse durchführen
            analysis_results = self._analyze_development_data(all_data)
            
            # Visualisierung erstellen
            self._create_visualization(all_data)
            
            return analysis_results
            
        except Exception as e:
            return f"Fehler bei der Fortschrittsanalyse: {str(e)}"
    
    def _collect_development_data(self):
        """
        Sammelt Entwicklungsdaten aus allen relevanten Dateien.
        """
        base_dir = "development_data"
        child_dir = os.path.join(base_dir, self.child_id)
        
        all_data = {}
        for area in self.development_areas:
            milestone_file = os.path.join(child_dir, f"milestones_{area}.json")
            if os.path.exists(milestone_file):
                with open(milestone_file, 'r', encoding='utf-8') as f:
                    all_data[area] = json.load(f)
            else:
                all_data[area] = []
        
        return all_data
    
    def _analyze_development_data(self, all_data):
        """
        Analysiert die gesammelten Entwicklungsdaten.
        """
        analysis = "Entwicklungsfortschrittsanalyse:\n\n"
        
        for area, data in all_data.items():
            if data:
                achieved = sum(1 for m in data if m.get('achieved', False))
                total = len(data)
                progress = (achieved/total)*100 if total > 0 else 0
                
                analysis += f"## {area.capitalize()}\n"
                analysis += f"Fortschritt: {progress:.1f}%\n"
                analysis += f"Erreichte Meilensteine: {achieved}/{total}\n"
                
                # Letzte Entwicklung
                last_milestone = sorted(data, key=lambda x: x['timestamp'])[-1]
                analysis += f"Letzte Entwicklung: {last_milestone.get('description', 'N/A')}\n\n"
        
        return analysis
    
    def _create_visualization(self, all_data):
        """
        Erstellt Visualisierungen der Entwicklungsfortschritte.
        """
        # Verzeichnis für Visualisierungen
        output_dir = os.path.join("development_data", self.child_id, "visualizations")
        os.makedirs(output_dir, exist_ok=True)
        
        # Fortschrittsgraph erstellen
        plt.figure(figsize=(12, 6))
        
        progress_data = []
        for area, data in all_data.items():
            if data:
                achieved = sum(1 for m in data if m.get('achieved', False))
                total = len(data)
                progress = (achieved/total)*100 if total > 0 else 0
                progress_data.append({'area': area, 'progress': progress})
        
        df = pd.DataFrame(progress_data)
        df.plot(kind='bar', x='area', y='progress')
        
        plt.title('Entwicklungsfortschritte nach Bereichen')
        plt.xlabel('Entwicklungsbereich')
        plt.ylabel('Fortschritt (%)')
        
        # Graph speichern
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"progress_analysis_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath)
        plt.close()

if __name__ == "__main__":
    tool = ProgressAnalyzer(
        child_id="MM001",
        analysis_period="6M",
        development_areas=["motorisch", "sprachlich"]
    )
    print(tool.run()) 