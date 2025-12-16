# Agentti raportti


> Päätyikö agentti toimivaan ratkaisuun?

Agentti päätyi toimivaan ratkaisuun, piti kyllä vähän kertoa, mitä ominaisuuksia halusi. Aluksi antoi mahdollisuuden valita joka vuorolle ketä vastaan pelaa, jota en halunnut tässä tapauksessa (kuitenkin jännä idea valita joka vuorolle eri vastustaja).

> Miten varmistuit, että ratkaisu toimii?

Varmistuin, että ratkaisu toimi kertomalla *agentille* luomaan kattavat unit testit. Testailin vielä manuaalisesti (black box testing), jotta sovellus toimisi loppukäyttäjille.

> Oletko ihan varma, että ratkaisu toimii oikein?

*Agentti* loi unit testit myöskin frontendille ([`routeille`](./kivi-paperi-sakset/tests/test_frontend_routes.py)), joten luotan, että ratkaisu toimii hyvin (en ole etsinyt rajatapauksia).

> Kuinka paljon jouduit antamaan agentille komentoja matkan varrella?

Prompteja piti antaa *agentille* muutama kunnes alkoi tekemään työtä mitä halusin. Tämä saattaa johtua käyttäjän antamien promptien laadusta ja kuinka kattava se on.

> Kuinka hyvät agentit tekemät testit olivat?

*Agentin* luomat testit olivat kattavat, sillä annoin promptiksi luomaan kattavat testit. *Agentti* pyysi ajamaan `poetry run pytest -q`, jotta näkisi testien tulokset korjatakseen viat.

> Onko agentin tekemä koodi ymmärrettävää?

Mielestäni kyllä, lukuunottamatta kovin pitkää metodia [`src.frontend.routes.play`](./kivi-paperi-sakset/src/frontend/routes.py), jonka itse olisin pilkkonut moneenkin osaan.

> Miten agentti on muuttanut edellisessä tehtässä tekemääsi koodia?

[ba35641452719f20175f60d1f13f2568f9443b8f](https://github.com/kahkaar/ohtu/commit/ba35641452719f20175f60d1f13f2568f9443b8f?diff=split#diff-5a1716634c229b33276a0609ae39fe37a5b5f197289e5deff442c49c56901b7f)

- Pieniä muutoksia `src/kps_app._display_options` -metodissa.
- Loi uuden `moottori` -tiedoston joka ns. johtaa pelin menemistä (game manager).
- `src/kps_logic.py` -tiedostoon lisäsi mahdollisuuden pelin loppumiseen.
- Pieniä muutoksia `src/kps_types`, `src/tekoaly`, `src/tekoaly_parannettu` ja `src/tuomari` -tiedostoihin, jotka eivät muuttanut toiminnallisuutta.

> Mitä uutta opit?

Käytti `Flask` -kirjaston `Blueprintteja`, joita en ole vielä päässyt kokeilemaan, mutta kiva oopia lisää niistä. Myöskin käytti `@*.get("/")` ja `@*.post("/")` [`src.frontend.routes`](./kivi-paperi-sakset/src/frontend/routes.py) -tiedostossa, josta en ole tiennyt ennen tätä.  Myöskin [`src.frontend.state`](./kivi-paperi-sakset/src/frontend/state.py) -tiedoston ensimmäinen rivi, joka tuo `from __future__ import annotations`, josta en tiennyt aikaisemmin.
