import sys
import os

# Add the src directory to Python's path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Now we can import the translator
from MangaAutoTranslator import MangaAutoTranslator

# Run it
if __name__ == "__main__":
    mat = MangaAutoTranslator(
        #fill out later with actual parameters, consider adding a CLI interface

    )