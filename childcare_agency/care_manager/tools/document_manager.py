from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from datetime import datetime

class DocumentManager(BaseTool):
    """
    Tool zum Erstellen und Verwalten von Markdown-Dokumenten für Betreuungspläne
    und pädagogische Dokumentation.
    """
    
    content: str = Field(
        ..., 
        description="Der Inhalt des Dokuments im Markdown-Format"
    )
    
    document_type: str = Field(
        ..., 
        description="Art des Dokuments (z.B. 'Betreuungsplan', 'Entwicklungsbericht')"
    )
    
    child_id: str = Field(
        ..., 
        description="Eindeutige ID des Kindes"
    )

    def run(self):
        """
        Erstellt oder aktualisiert ein Markdown-Dokument und speichert es im
        entsprechenden Verzeichnis.
        """
        # Erstelle Verzeichnisstruktur
        base_dir = "documents"
        child_dir = os.path.join(base_dir, self.child_id)
        os.makedirs(child_dir, exist_ok=True)
        
        # Generiere Dateinamen
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.document_type}_{timestamp}.md"
        filepath = os.path.join(child_dir, filename)
        
        try:
            # Schreibe Dokument
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.content)
            
            return f"Dokument erfolgreich gespeichert: {filepath}"
            
        except Exception as e:
            return f"Fehler beim Speichern des Dokuments: {str(e)}"

if __name__ == "__main__":
    test_content = """
    # Entwicklungsbericht
    
    ## Kind: Max Mustermann
    ## Datum: 2024-01-20
    
    ### Beobachtungen
    - Zeigt großes Interesse an kreativen Aktivitäten
    - Gute Fortschritte in der sprachlichen Entwicklung
    
    ### Empfehlungen
    1. Weitere Förderung im kreativen Bereich
    2. Sprachspiele zur Unterstützung der Entwicklung
    """
    
    tool = DocumentManager(
        content=test_content,
        document_type="Entwicklungsbericht",
        child_id="MM001"
    )
    print(tool.run()) 