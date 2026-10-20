# forumownik

projekt na bezpieczeństwo aplikacji webowych czy coś

klon reddita (bardzo kreatywny projekt)

## uruchamianie środowiska deweloperskiego

1. utwórz virtual environment, wejdź do virtual environment, `pip install -r requirements.txt`
2. uruchom baze postgresql (np. według `compose.yml`)
3. przygotuj bucket S3 oraz użytkownika/klucz z dostępem do odczytu/zapisu
4. skopiuj plik `.env.example` do `.env` i wypełnij
5. `./manage.py runserver`
