from agency_swarm.tools import BaseTool
from pydantic import Field
import json
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

class EmotionAnalyzer(BaseTool):
    """
    Tool zur Analyse und Auswertung emotionaler Zustände und Entwicklungen.
    """
    
    child_id: str = Field(
        ..., 
        description="Eindeutige ID des Kindes"
    )
    
    emotion_data: dict = Field(
        ...,
        description="Daten zu emotionalen Zuständen und Reaktionen"
    )
    
    analysis_period: str = Field(
        default="1W",
        description="Analysezeitraum (z.B. '1D', '1W', '1M')"
    )

    def run(self):
        """
        Führt eine umfassende Analyse der emotionalen Entwicklung durch.
        """
        try:
            # Daten speichern
            self._save_emotion_data()
            
            # Emotionsanalyse durchführen
            emotion_analysis = self._analyze_emotions()
            
            # Entwicklungstrends identifizieren
            trends = self._identify_trends()
            
            # Visualisierung erstellen
            self._create_visualization()
            
            # Gesamtbericht erstellen
            report = "Emotionsanalyse:\n\n"
            report += emotion_analysis + "\n"
            report += trends
            
            return report
            
        except Exception as e:
            return f"Fehler bei der Emotionsanalyse: {str(e)}"
    
    def _save_emotion_data(self):
        """
        Speichert die Emotionsdaten strukturiert ab.
        """
        base_dir = os.path.join("psychological_data", self.child_id, "emotions")
        os.makedirs(base_dir, exist_ok=True)
        
        # Dateiname mit Zeitstempel
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(base_dir, f"emotions_{timestamp}.json")
        
        # Daten mit Zeitstempel speichern
        data_to_save = {
            "timestamp": datetime.now().isoformat(),
            "period": self.analysis_period,
            "emotions": self.emotion_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)
    
    def _analyze_emotions(self):
        """
        Analysiert die emotionalen Zustände und Muster.
        """
        analysis = "Emotionale Zustände und Muster:\n\n"
        
        # Grundstimmung
        mood = self.emotion_data.get('base_mood', {})
        analysis += "Grundstimmung:\n"
        for situation, mood_state in mood.items():
            analysis += f"- {situation}: {mood_state}\n"
        
        # Emotionale Reaktionen
        reactions = self.emotion_data.get('emotional_reactions', {})
        analysis += "\nEmotionale Reaktionen:\n"
        for trigger, reaction in reactions.items():
            analysis += f"- {trigger}: {reaction}\n"
        
        # Emotionsregulation
        regulation = self.emotion_data.get('emotion_regulation', {})
        analysis += "\nEmotionsregulation:\n"
        for strategy, effectiveness in regulation.items():
            analysis += f"- {strategy}: {effectiveness}\n"
        
        return analysis
    
    def _identify_trends(self):
        """
        Identifiziert Trends in der emotionalen Entwicklung.
        """
        trends = "\nEntwicklungstrends:\n\n"
        
        # Stimmungstrends
        if 'mood_history' in self.emotion_data:
            mood_trends = pd.Series(self.emotion_data['mood_history']).value_counts()
            trends += "Häufigste Stimmungen:\n"
            for mood, count in mood_trends.items():
                trends += f"- {mood}: {count} mal\n"
        
        # Entwicklungstrends
        if 'development_trends' in self.emotion_data:
            trends += "\nEmotionale Entwicklung:\n"
            for area, trend in self.emotion_data['development_trends'].items():
                trends += f"- {area}: {trend}\n"
        
        return trends
    
    def _create_visualization(self):
        """
        Erstellt Visualisierungen der emotionalen Entwicklung.
        """
        output_dir = os.path.join("psychological_data", self.child_id, "visualizations")
        os.makedirs(output_dir, exist_ok=True)
        
        # Emotionsverlauf visualisieren
        if 'mood_history' in self.emotion_data:
            plt.figure(figsize=(12, 6))
            mood_data = pd.Series(self.emotion_data['mood_history'])
            mood_data.value_counts().plot(kind='bar')
            plt.title('Emotionale Zustände im Zeitverlauf')
            plt.xlabel('Emotion')
            plt.ylabel('Häufigkeit')
            
            # Graph speichern
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"emotion_analysis_{timestamp}.png"
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath)
            plt.close()

if __name__ == "__main__":
    sample_data = {
        "base_mood": {
            "Morgen": "ausgeglichen",
            "Mittag": "aktiv",
            "Nachmittag": "müde"
        },
        "emotional_reactions": {
            "Gruppenaktivität": "begeistert",
            "Trennung": "leicht ängstlich",
            "Konflikt": "frustrationstolerant"
        },
        "emotion_regulation": {
            "Selbstberuhigung": "entwickelt sich",
            "Unterstützungssuche": "angemessen"
        },
        "mood_history": [
            "fröhlich", "ausgeglichen", "fröhlich", 
            "müde", "aufgeregt", "fröhlich"
        ],
        "development_trends": {
            "Emotionsausdruck": "zunehmend differenziert",
            "Selbstregulation": "positive Entwicklung"
        }
    }
    
    tool = EmotionAnalyzer(
        child_id="MM001",
        emotion_data=sample_data,
        analysis_period="1W"
    )
    print(tool.run()) 