# Filmová databáze

## Databáze
- Země
  - název
- Žánr
  - název
- filmy(Movie)
  - Originální název filmu
  - Český název filmu
  - Slovenský název filmu
  - Země původu -> FK(Země)
  - Žánr -> FK(žánr)
  - Režisér -> FK(Osobnosti)
  - Herci -> FK(Osobnosti)
  - Rok premiery
  - Hodnocení -> FK(Hodnocení)
  - Komentáře -> FK(Hodnocení)
  - obrázek -> FK(Obrázky)
  - Video -> (url odkaz na trailer)
  - Popis
- Hodnocení
  - id filmu
  - id uživatele
  - hodnocení
- Obrázky
  - id filmu
  - obrázek (název souboru / image ?)
  - Popis
- Osobnosti
    - Jméno
    - Příjmení
    - Rok narození
    - informace
    - filmy, ve kterých hráli / režírovali


## Funkce (views + templates)

- zobrazit novinky(homepage)
- zobrazovat seznam všech filmů
    - filtrování filmů (seznam)
        - podle žánru
        - podle hodnocení
        - podle herce
        - podle režiséra
- zobrazit detail filmu
- Přihlášený uživatel může:
  - hodnotit filmy
  - komentovat filmy
- Admin může:
  - přidat nový film/herce/režiséra/žánr/země/komentáře
  - Může smazat, nebo editovat film/herce/režiséra