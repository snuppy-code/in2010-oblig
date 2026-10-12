IN2010 oppsett og testrunner

## Installasjon

1. Last ned nyeste `in2010-testrunner.zip` fra [releases](https://github.uio.no/IN2010/in2010-testrunner/releases).
   - (*Ikke* bruk «download zip» under clone-menyen.)
2. Kjør programmet med følgende kommando:

   ```
   python sti/til/in2010-testrunner.zip
   ```

   Hvis `in2010-testrunner.zip` ligger i mappen du er i, er det nok å kjøre:

   ```
   python in2010-testrunner.zip
   ```

*Ja*, Python støtter å kjøre zip-filer direkte (når de er satt opp riktig).

## Bruk

1. Start med å opprette en *tom* mappe for å lagre koden din i.
2. Flytt `in2010-testrunner.zip` til den nye mappen.
3. Fra den nye mappen, kjør `python in2010-testrunner.zip`
   - Programmet setter opp prosjektstrukturen første gang det kjøres.
4. Skriv løsningene dine i filene som blir opprettet av `in2010-testrunner`.
5. Hvis du vil kan du slette kildefiler du ikke trenger (`in2010-testrunner` oppretter både Java- og Python-filer).
6. Kjør koden din med `run`-kommandoen i `in2010-testrunner`-kommandolinjen.
7. Lag en zip-fil med `zip`-kommandoen i `in2010-testrunner`-kommandolinjen.
8. Last opp den resulterende zip-filen i [devilry](https://devilry.ifi.uio.no/devilry_student/).

## Installasjon med `pip` (valgfritt)

Programmet kan også installeres med:

```
pip install sti/til/in2010-testrunner.zip
```

Etter dette skal kommandoen `in2010-testrunner` være tilgjengelig på systemet ditt.

## Feilsøking

### MacOS pakket ut `in2010-testrunner.zip` automatisk

På MacOS blir zip-filer noen ganger pakket ut automatisk. Denne mappen
kan *også* kjøres direkte av Python.

I instruksjonene over kan du da erstatte alle forekomster av
`in2010-testrunner.zip` med `in2010-testrunner`.

### MacOS SSL-sertifikater

På MacOS kan Python noen ganger ha problemer med å finne riktige SSL-sertifikater.
Løsningen er:

1. Åpne Finder.
2. Gå til «Applications»/«Applikasjoner»-mappen, og deretter inn i «Python»-mappen.
3. Dobbeltklikk på «Install Certificates.command».

Alternativt kan du kjøre kommandoen:

```
bash /Applications/Python*/Install\ Certificates.command
```

i en terminal.

### Global installasjon med `pip`

På noen operativsystemer kan det være problematisk å installere
Python-pakker globalt med `pip`. Du kan da enten kjøre filen
direkte uten å installere den, eller [lage et virtuelt Python-miljø](https://docs.python.org/3/library/venv.html).
