IN2010 oppsett og testrunner

### Installasjon

1. Last ned nyeste `in2010-testrunner.zip` fra [releases](https://github.uio.no/IN2010/in2010-testrunner/releases) (ikke bruk
«download zip» under clone-menyen).
2. Enten:
   - kjør programmet direkte med `python sti/til/fil.zip`, eller
   - installer det med `pip install sti/til/fil.zip`.

> Merk:
> På noen operativsystemer kan det være problematisk å installere
> Python-pakker globalt med `pip`. Du kan da enten kjøre filen
> direkte uten å installere den, eller [lage et virtuelt Python-miljø](https://docs.python.org/3/library/venv.html).

### Bruk

1. Start med å opprette en tom mappe for å lagre koden din i.
2. Hvis du ikke har installert med `pip`, flytt `in2010-testrunner.zip` til den nye mappen.
3. Fra den nye mappen, kjør `in2010-testrunner` (eller `python in2010-testrunner.zip`).
4. Løs innleveringsoppgavene i filene som har blitt opprettet av `in2010-testrunner`.
5. Hvis du vil kan du slette kildefiler du ikke trenger (`in2010-testrunner` oppretter både Java- og Python-filer).
6. Kjør koden din med `run`-kommandoen i `in2010-testrunner`-kommandolinjen.
7. Lag en zip-fil med `zip`-kommandoen i `in2010-testrunner`-kommandolinjen.
8. Last opp den resulterende zip-filen i [devilry](https://devilry.ifi.uio.no/devilry_student/).
