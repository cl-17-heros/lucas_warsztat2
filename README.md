![Coders-Lab-1920px-no-background](https://user-images.githubusercontent.com/30623667/104709387-2b7ac180-571f-11eb-9b94-517aa6d501c9.png)

# Kilka ważnych informacji

Przed przystąpieniem do rozwiązywania zadań przeczytaj poniższe wskazówki

## Jak zacząć?

1. Stwórz [*fork*](https://guides.github.com/activities/forking/) repozytorium z zadaniami.
2. Sklonuj fork repozytorium (stworzony w punkcie 1) na swój komputer. Użyj do tego komendy `git clone adres_repozytorium`
Adres możesz znaleźć na stronie forka repozytorium po naciśnięciu w guzik "Clone or download".
3. Rozwiąż zadania i skomituj zmiany do swojego repozytorium. Użyj do tego komend `git add nazwa_pliku`.
Jeżeli chcesz dodać wszystkie zmienione pliki użyj `git add .` 
Pamiętaj że kropka na końcu jest ważna!
Następnie skommituj zmiany komendą `git commit -m "nazwa_commita"`
4. Wypchnij zmiany do swojego repozytorium na GitHubie.  Użyj do tego komendy `git push origin master`
5. Stwórz [*pull request*](https://help.github.com/articles/creating-a-pull-request) do oryginalnego repozytorium, gdy skończysz wszystkie zadania.

Poszczególne zadania rozwiązuj w odpowiednich plikach.

### Poszczególne zadania rozwiązuj w odpowiednich plikach.

**Repozytorium z ćwiczeniami zostanie usunięte 2 tygodnie po zakończeniu kursu. Spowoduje to też usunięcie wszystkich forków, które są zrobione z tego repozytorium.**


# Warsztat &ndash; Konfiguracja bazy danych

Zanim przygotujemy skrypt, który utworzy nam bazę danych, musimy przygotować nasz projekt.
W tym celu:
* stwórz folder pod aplikację,
* utwórz repozytorium na `githubie`,
* stwórz plik `.gitignore` i dodaj do niego podstawowe dane (podpowiedź: możesz znaleźć gotowy plik dla pythona w sieci)

**Pamiętaj, o robieniu backapów bazy danych i częstym tworzeniu commitów.**

Na początek zajmijmy się skonfigurowaniem naszej bazy danych.
Napisz w tym celu skrypt pythona: `create_db.py`, w którym:

1. Utworzysz bazę danych. Jeśli baza już istnieje, skrypt ma poinformować o tym użytkownika, nie przerywając swojego
    działania (Podpowiedź: możesz przechwycić błąd: `DuplicateDatabase`).
2. Stworzysz tabelę trzymającą dane użytkownika (`users`). Powinna posiadać następujące kolumny:
    * `id` &ndash; klucz główny (najlepiej typu serial),
    * `username` &ndash; ciąg znaków (varchar(255)),
    * `hashed_password` &ndash; ciąg znaków (varchar(80)).
    Jeżeli istnieje już taka tabela, skrypt powinien poinformować o tym użytkownika, nie przerywając swojego działania
    (Podpowiedź: możesz przechwycić błąd: `DuplicateTable`).
3. Stworzysz tabelę przechowującą komunikaty (`messages`). Powinna posiadać następujące kolumny:
    * `id` &ndash; klucz główny (najlepiej typu serial),
    * `from_id` &ndash; klucz obcy do tabeli `users`,
    * `to_id` &ndash; klucz obcy do tabeli `users`,
    * `creation_date` &ndash; timestamp, dodawany automatycznie,
    * `text` &ndash; ciąg znaków (varchar(255)).
    Jeżeli istnieje już taka tabela, skrypt powinien poinformować o tym użytkownika, nie przerywając swojego działania
    (Podpowiedź: możesz przechwycić błąd: `DuplicateTable`).

**Pamiętaj o zamknięciu połączenia. Powinieneś też obsłużyć ewentualne błędy połączenia (`OperationalError`).**


# Warsztat &ndash; Obiektowa obsługa bazy danych

Mamy już stworzoną naszą bazy danych. Pola na stworzenie biblioteki odwzorowującej nasze tabele w postaci obiektów.
Utwórz teraz osobny moduł (np. `models.py`). W nim umieść kod z klasami, obsługującymi poszczególne tabele.


## Klasa użytkownika

1. Stwórz klasę, obsługującą użytkownika. Powinna ona posiadać następujące atrybuty:
    * `_id` &ndash; ustawione podczas tworzenia na `-1`,
    * `usename` &ndash; nazwa użytkownika,
    * `_hashed_password` &ndash; zahaszowane hasło użytkownika.
2. Udostępnij `_id` i `_hashed_password` do odczytu na zewnątrz.
3. Dodaj metodę, która pozwoli, na ustawienie nowego hasła (Podpowiedź: możesz użyć **settera**).
4. Dodaj metody do obsługi bazy:
    `save_to_db` &ndash; zapis do bazy danych lub aktualizacja obiektu w bazie,
    `load_user_by_username` &ndash; wczytanie użytkownika z bazy danych na podstawie jego nazwy,
    `load_user_by_id` &ndash; wczytanie użytkownika z bazy danych na podstawie jego id,
    `load_all_users` &ndash; wczytanie wszystkich użytkowników z bazy danych,
    `delete` &ndash; usunięcie użytkownika z bazy i nastawienie jego `_id` na `-1`.
    
Podpowiedzi:
* Wszystkie powyższe metody, powinny przyjmować **kursor** do obsługi bazy danych.
* Możesz wykorzystać kod, który omówiliśmy w artykule poświęconym wzorcowi projektowemu **Active Record**.
    Wystarczy, że dodasz do niego metodę, wczytującą użytkownika z bazy na podstawie jego imienia.
    
## Klasa wiadomości

1. Utwórz teraz klasę, która będzie obsługiwała nasze wiadomości. Powinna ona posiadać następujące atrybuty:
    * `_id` &ndash; ustawione podczas tworzenia na `-1`,
    * `from_id` &ndash; id nadawcy, ustawiane podczas tworzenia obiektu,
    * `to_id` &ndash; id odbiorcy, ustawiane podczas tworzenia obiektu,
    * `text` &ndash; tekst do przesłania,
    * `creation_data` &ndash; data utworzenia wiadomości. Podczas tworzenia przypisz do niej `None`. Ustawisz ją
    w momencie zapisu do bazy danych.
2. Udostępnij `_id` na zewnątrz.
3. Dodaj metody do obsługi bazy:
    * `save_to_db` &ndash; zapis do bazy danych lub aktualizacja obiektu w bazie,
    * `load_all_messages` &ndash; wczytanie wszystkich wiadomości.
    
Podpowiedzi:
* Usuwanie wiadomości, nie będzie nam potrzebne. 
* Metody, będą bardzo podobne do tych z klasy użytkownika. Wystarczy, że lekko je zmodyfikujesz.


**Pamiętaj, żeby przetestować, czy biblioteka działa. Możesz wykorzystać scenariusze testowe, opisane w artykule
omawiającym Active Record.**

# Warsztat &ndash; Aplikacja do obsługi użytkowników

Utwórzmy teraz aplikację, obsługującą naszych użytkowników. Będzie to aplikacja konsolowa, przyjmująca argumenty
wprowadzone przez użytkownika. Wykorzystaj do tego bibliotekę `argparse`. 
Aplikacja powinna obsługiwać następujące parametry:
    * `-u`, `--username` &ndash; nazwa użytkownika,
    * `-p`, `--password` &ndash; hasło użytkownika,
    * `-n`, `--new_pass` &ndash; nowe hasło,
    * `-l`, `--list` &ndash; listowanie użytkowników,
    * `-d`, `--delete` &ndash; usuwanie użytkownika,
    * `-e`, `--edit` &ndash; edycja użytkownika.
    
Aplikacja powinna obsługiwać scenariusze opisane poniżej.
Najprościej będzie, przygotować osobną funkcję na każdy, ze scenariuszy. W głównym kodzie programu wystarczy wtedy
sprawdzić parametry instrukcję `if` &ndash; `elif`, a następnie wywołać odpowiednie funkcje. 

## Tworzenie użytkownika

Jeśli podczas wywołania aplikacji, użytkownik poda tylko parametry: `username` i `password`:
* jeśli użytkownik o podanej nazwie istnieje &ndash; zgłaszamy błąd 
    (Podpowiedź: możesz przechwycić błąd: `UniqueViolation`),
* jeśli nie ma takiego użytkownika:
    * jeśli hasło ma co najmniej 8 znaków, należy go utworzyć, korzystając z podanych danych 
    (pamiętaj, o zapisaniu obiektu do bazy danych),
    * jeśli hasło jest za krótkie, należy wyświetlić odpowiedni komunikat.


## Edycja hasła użytkownika

Jeśli podczas wywołania aplikacji, użytkownik poda parametry:
* `username`,
* `password`,
* `edit`,
* `new_pass`,
powinniśmy:
* sprawdzić, czy użytkownik istnieje
* sprawdzić, czy hasło jest poprawne:
    * jeśli tak, sprawdzamy, czy nowe hasło (`new_pass`) ma wymaganą długość:
        * jeśli jest krótsze niż 8 znaków, zgłaszamy to odpowiednim komunikatem,
        * jeśli jest wystarczającej długości, ustawiamy nowe hasło,
    * jeśli hasło jest niepoprawne, zgłaszamy to odpowiednim komunikatem.
    
> Podpowiedź: Do sprawdzenia hasła, możesz wykorzystać funkcję `check_password` z biblioteki `clcrypto`.

## Usuwanie użytkownika

Jeśli podczas wywołania aplikacji, użytkownik poda parametry:
* `username`,
* `password`,
* `delete`,
należy:
* sprawdzić poprawność hasła,
    * jeśli jest poprawne &ndash; usunąć użytkownika z bazy danych,
    * jeśli jest niepoprawne &ndash; poinformować o tym użytkownika odpowiednim komunikatem np. `"Incorrect Password!`.


## Listowanie użytkowników:

Jeśli podczas wywołania aplikacji, użytkownik poda parametr `-l` (`--list`), należy wypisać listę
wszystkich użytkowników. 
   

## Pomoc

Jeśli użytkownik poda inny zestaw parametrów, należy wyświetlić mu panel pomocy. Można to zrobić, wywołując:
metodę `print_help` z obiektu parsera.

##### Przykład:
```python
import argparse

parser = argparse.ArgumentParser()
parser.print_help()
```




# Warsztat &ndash; Aplikacja do obsługi wiadomości

Stwórzmy teraz naszą główną aplikację. Będzie to program konsolowy pozwalający wysyłać i odczytywać wiadomości.
Aplikacja powinna przyjmować od użytkownika następujące argumenty:
* `-u`, `--username` &ndash; nazwa użytkownika,
* `-p`, `--password` &ndash; hasło użytkownika,
* `-t`, `--to` &ndash; nazwa użytkownika, do którego ma zostać wysłana wiadomość,
* `-s`, `--send` &ndash; treść wiadomości,
* `-l`, `--list` &ndash; żądanie wylistowania wszystkich komunikatów użytkownika (flaga).

Do parsowania argumentów użyj biblioteki `argparse`.

Aplikacja powinna obsługiwać scenariusze opisane poniżej.
Najprościej będzie, przygotować osobną funkcję na każdy, ze scenariuszy. W głównym kodzie programu wystarczy wtedy
sprawdzić parametry instrukcję `if` &ndash; `elif`, a następnie wywołać odpowiednie funkcje. 

## Listowanie wiadomości

Jeśli podczas wywołania aplikacji, użytkownik poda parametry: `username` i `password` oraz ustawi flagę `-l`:
* sprawdź, czy użytkownik istnieje, jeśli nie wyświetl odpowiedni komunikat,
* sprawdź, czy hasło jest poprawne:
    * jeśli nie, wyświetl odpowiedni komunikat,
    * jeśli tak, wypisz wszystkie wiadomości wysłane do tego użytkownika.
    
Każda z wiadomości powinna zawierać:
* adresata,
* datę wysłania wiadomości,
* treść wiadomości.

## Wysłanie wiadomości

Jeśli podczas wywołania aplikacji, użytkownik poda parametry: `username` i `password` oraz dodatkowo 
ustawi parametr `-t` (`--to`) i `-s` (`--send`):
* sprawdź, czy użytkownik istnieje, jeśli nie wyświetl odpowiedni komunikat,
* sprawdź, czy hasło jest poprawne:
    * jeśli nie, wyświetl odpowiedni komunikat,
    * jeśli tak:
        * sprawdź, czy adresat wiadomości istnieje (`--to`), jeśli nie, poinformuj o tym użytkownika,
        * sprawdź, czy wiadomość jest krótsza, niż 255 znaków:
            * jeśli nie, wyświetl odpowiedni komunikat,
            * jeśli tak, utwórz wiadomość i zapisz ją do bazy danych.


## Pomoc

Jeśli użytkownik poda inny zestaw parametrów, należy wyświetlić mu panel pomocy. Można to zrobić, wywołując:
metodę `print_help` z obiektu parsera.

##### Przykład:
```python
import argparse

parser = argparse.ArgumentParser()
parser.print_help()
```

