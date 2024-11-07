from agency_swarm.tools import BaseTool
from pydantic import Field
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
from datetime import datetime

class TrendAnalyzer(BaseTool):
    """
    Tool zur Analyse von Trends in der pädagogischen Forschung und Praxis
    mit Visualisierungsfunktionen.
    """
    
    data: list = Field(
        ..., 
        description="Liste von Datenpunkten für die Trendanalyse"
    )
    
    analysis_type: str = Field(
        default="frequency",
        description="Art der Analyse (frequency/correlation/development)"
    )
    
    time_period: str = Field(
        default="1Y",
        description="Zeitraum für die Analyse (z.B. '1Y', '6M', '5Y')"
    )

    def run(self):
        """
        Analysiert Trends in pädagogischen Daten und erstellt Visualisierungen.
        """
        try:
            # Daten in DataFrame konvertieren
            df = pd.DataFrame(self.data)
            
            # Verzeichnis für Grafiken erstellen
            output_dir = "trend_analysis"
            os.makedirs(output_dir, exist_ok=True)
            
            # Analyse basierend auf dem gewählten Typ
            if self.analysis_type == "frequency":
                plt.figure(figsize=(10, 6))
                df['occurrence'].value_counts().plot(kind='bar')
                plt.title('Häufigkeitsverteilung pädagogischer Konzepte')
                plt.xlabel('Konzept')
                plt.ylabel('Häufigkeit')
                
            elif self.analysis_type == "correlation":
                plt.figure(figsize=(8, 8))
                correlation_matrix = df.corr()
                plt.imshow(correlation_matrix, cmap='coolwarm')
                plt.colorbar()
                plt.title('Korrelationsmatrix pädagogischer Faktoren')
                
            elif self.analysis_type == "development":
                plt.figure(figsize=(12, 6))
                df.plot(x='date', y='value', kind='line')
                plt.title('Entwicklungstrend über Zeit')
                plt.xlabel('Datum')
                plt.ylabel('Wert')
            
            # Grafik speichern
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trend_{self.analysis_type}_{timestamp}.png"
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath)
            plt.close()
            
            # Analyseergebnisse zusammenfassen
            summary = f"Trendanalyse durchgeführt:\n"
            summary += f"- Analysetype: {self.analysis_type}\n"
            summary += f"- Zeitraum: {self.time_period}\n"
            summary += f"- Visualisierung gespeichert unter: {filepath}\n"
            
            if self.analysis_type == "frequency":
                summary += "\nTop 5 häufigste Konzepte:\n"
                top_5 = df['occurrence'].value_counts().head()
                for concept, count in top_5.items():
                    summary += f"- {concept}: {count}\n"
            
            return summary
            
        except Exception as e:
            return f"Fehler bei der Trendanalyse: {str(e)}"

if __name__ == "__main__":
    sample_data = [
        {"date": "2023-01-01", "concept": "Sprachförderung", "value": 75, "occurrence": "häufig"},
        {"date": "2023-02-01", "concept": "Motorik", "value": 82, "occurrence": "mittel"},
        {"date": "2023-03-01", "concept": "Soziales Lernen", "value": 90, "occurrence": "häufig"},
    ]
    
    tool = TrendAnalyzer(
        data=sample_data,
        analysis_type="frequency",
        time_period="3M"
    )
    print(tool.run()) 