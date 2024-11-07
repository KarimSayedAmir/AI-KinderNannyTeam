from agency_swarm.tools import BaseTool
from pydantic import Field
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import re

class KeywordExtractor(BaseTool):
    """
    Tool zur Extraktion und Analyse von Schlüsselwörtern aus pädagogischen Texten
    unter Verwendung von NLTK.
    """
    
    text: str = Field(
        ..., 
        description="Der zu analysierende Text"
    )
    
    language: str = Field(
        default="german",
        description="Sprache des Textes (german/english)"
    )
    
    num_keywords: int = Field(
        default=10,
        description="Anzahl der zu extrahierenden Schlüsselwörter"
    )

    def run(self):
        """
        Extrahiert Schlüsselwörter aus dem Text und analysiert deren Häufigkeit.
        """
        try:
            # Download benötigter NLTK-Daten
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            
            # Text vorverarbeiten
            text = self.text.lower()
            text = re.sub(r'[^\w\s]', '', text)
            
            # Tokenisierung
            tokens = word_tokenize(text, language=self.language)
            
            # Stopwörter entfernen
            stop_words = set(stopwords.words(self.language))
            tokens = [token for token in tokens if token not in stop_words]
            
            # Häufigkeitsanalyse
            fdist = FreqDist(tokens)
            
            # Top-Keywords extrahieren
            keywords = fdist.most_common(self.num_keywords)
            
            # Ergebnis formatieren
            result = "Extrahierte Schlüsselwörter:\n\n"
            for word, freq in keywords:
                result += f"- {word}: {freq} Vorkommen\n"
            
            return result
            
        except Exception as e:
            return f"Fehler bei der Keyword-Extraktion: {str(e)}"

if __name__ == "__main__":
    sample_text = """
    Die frühkindliche Bildung spielt eine zentrale Rolle in der Entwicklung.
    Durch gezielte Förderung können kognitive und soziale Fähigkeiten gestärkt werden.
    Sprachentwicklung und motorische Entwicklung sind dabei besonders wichtig.
    """
    
    tool = KeywordExtractor(
        text=sample_text,
        language="german",
        num_keywords=5
    )
    print(tool.run()) 