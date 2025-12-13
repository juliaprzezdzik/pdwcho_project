cat > README.md << 'EOF'
# 📚 System Rekomendacji Książek

> Proof-of-concept systemu rekomendacji opartego o grafową bazę danych Neo4j i algorytm Collaborative Filtering

## Demo

**[https://pdwcho-project.onrender.com](https://pdwcho-project.onrender.com)**

<img width="809" height="557" alt="Zrzut ekranu 2025-12-13 o 11 39 41" src="https://github.com/user-attachments/assets/083280fc-5f24-4e1e-a7bc-f14330de111c" />

## Funkcjonalności

- Rekomendacje książek oparte o Collaborative Filtering
- Grafowa baza danych (Neo4j)
- RESTful API (Flask)
- Single Page Application
- Deployment w chmurze (Render + AuraDB)
- Responsywny design (mobile-first)

## Technologie

**Backend:**
- Python 3.9
- Flask (RESTful API)
- Neo4j Python Driver
- Gunicorn

**Frontend:**
- HTML5 / CSS3
- Vanilla JavaScript (ES6)
- Fetch API

**Infrastructure:**
- Render.com (PaaS)
- Neo4j AuraDB (DBaaS)
- GitHub (CI/CD)

## Instalacja Lokalna

### Wymagania
- Python 3.9+
- Neo4j AuraDB account
- Git

### Kroki
```bash
# 1. Repozytorium
git clone https://github.com/TWOJ_USERNAME/PDCHO_PROJEKT.git
cd PDCHO_PROJEKT

# 2. Venv
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# 3. Zaleznosci
pip install -r requirements.txt

# 4. Zmienne
export NEO4J_URI="neo4j+s://your-instance.databases.neo4j.io"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your-password"

# 5.Uruchomienie
python app.py

# 6. http://localhost:5000
```

## Model Danych (Neo4j)
```cypher
// Węzły
(:User {username: string, name: string})
(:Book {isbn: string, title: string, author: string})

// Relacje
(:User)-[:READS {rating: float}]->(:Book)
```

## Rekomendache

1. **Znajdź podobnych użytkowników** - użytkownicy którzy czytali te same książki
2. **Oblicz punkty podobienstwa** - liczba wspólnych książek
3. **Generuj rekomendacje** - książki które czytali podobni użytkownicy
4. **Ranking** - sortowanie według średniej oceny i liczby rekomendujących

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Frontend (SPA) |
| GET | `/hello` | Health check |
| GET | `/recommendations/<username>` | Rekomendacje dla użytkownika |

**Przykład:**
```bash
curl https://pdwcho-project.onrender.com/recommendations/AnnaK
```

**Odpowiedz:**
```json
{
  "user": "AnnaK",
  "count": 5,
  "recommendations": [
    {
      "title": "Wykształciuch",
      "isbn": "978-8381880763",
      "avgRating": 5.0,
      "recommenders": 1
    }
  ]
}
```

## Struktura Projektu
```
PDCHO_PROJEKT/
├── app.py              # Backend (Flask + Neo4j)
├── index.html          # Frontend (SPA)
├── requirements.txt    # Python dependencies
├── README.md           # Ten plik
├── DOKUMENTACJA.md     # Pełna dokumentacja techniczna
```
