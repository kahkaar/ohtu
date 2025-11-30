# Raportti Copilot katselmoinnista

- Copilot huomasi, että kyseessä oli `TennisGame` -luokan refaktoroinnista.

## Huomautukset

1. Huomasi, että moduuli kohtaiset vakiot eivät seuraa `PEP8` -koodityyliä.

    Vastaus: Nämä vakoit olevat *yksityisiä*, joten perustelen näiden nimeämisen alkaen alaviivalla (_). Koodissa myös kommentoitu, miksi näitä edes käytetään.

2. Väittää huomaavan virheen, koska edellisessä koodissa katsottiin `player_name == "player1"`, joten luuli, että tämä pitäisi olla näin myös refaktoroidussa koodissa.

3. Huomasi, että luokan parametrit pitäisi olla nimeltä `player1_name` ja `player2_name` eikä vain `player1` ja `player2`.

4. Huomautti testaus kattavuudesta, koska loin kaksi apumetodia.

5. Huomautti metodien `docstring` puuttuvuudesta.

## Olivatko ehdotukset hyviä?

Osa ehdotuksista oli hyviä, esim. edellisen osion `3.` kohta. Kuitenkin, jotkut olivat huonoja tai *väärinymmärrettyjä* ehdotuksia, esimerkiksi edellisen osion `2.` kohta.

## Oliko hyötyä?

Mielestäni tästä oli hyötyä, vaikka antoi n.s. huonoja ehdotuksia, mutta antoi kuitenkin myös hyviä ehdotuksia. Pitää olla vain tarkkana, kun lukee Copilotin tekemiä katselmointeja.
