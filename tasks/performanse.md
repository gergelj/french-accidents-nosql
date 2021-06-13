# Performanse

|||
|---|---|
| ![](graphs/performanse/1_1.png) | ![](graphs/performanse/1_2.png)  |
| ![](graphs/performanse/1_3.png) | ![](graphs/performanse/1_4.png)  |
| ![](graphs/performanse/1_5a.png)| ![](graphs/performanse/1_5b.png) |

Iz rezultata izvršenja samih upita se vidi da u svakom upitu `group` pipeline usporava izvršenje, posebno ona grupisanja gde se prebrojava veća količina dokumenata (uslovno ili bezuslovno).

## Korišćenje indeksa

Za Task 1_1 je iskorišćen indeks `int` (tip raskrsnice) napravljen nad kolekcijom `accidents`:

![](graphs/performanse/1_1_index.png)