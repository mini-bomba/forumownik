# forumownik

projekt na bezpieczeństwo aplikacji webowych czy coś

klon reddita (bardzo kreatywny projekt)

## uruchamianie środowiska deweloperskiego

1. utwórz virtual environment, wejdź do virtual environment, `pip install -r requirements.txt`
2. uruchom baze postgresql (np. według `compose.yml` - `docker compose -f dev-compose.yml up -d`)
3. przygotuj bucket S3 oraz użytkownika/klucz z dostępem do odczytu/zapisu
4. skopiuj plik `.env.example` do `.env` i wypełnij
5. `./manage.py runserver`

## środowisko produkcyjne

1. system powinien mieć zainstalowanego dockera z wtyczką docker compose i buildx oraz traefik jako reverse proxy

   compose zakłada, że skonfigurowany jest endpoint `http`.
   traefik w tym deploy nie zajmuje się szyfrowaniem ruchu, zamiast tego otrzymuje ruch odszyfrowany
   od innego, zewnętrznego reverse proxy (w moim przypadku nginx)

2. przygotuj `.env` według szablonu
3. `docker compose -f prod-compose.yml up -d`
