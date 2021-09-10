# Raamatukogu
Raamatute laenutamise teemaline prooviülesanne. 
Ülesanne on teostatud kasutades Python 3.9 ja Vue.js 3.0.

## Tutvustus
Rakendus võimaldab kasutajatel laenata üksteisele raamatuid.
Kasutajatel on üks kahest võimalikust rollist: laenaja või laenutaja.

Laenajal on võimalik sisestada oma raamatud andmebaasi, kust seejärel
on laenutajatel võimalik neid raamatuid laenutada või broneerida.
Laenajal on võimalik eemaldada oma raamatud laenamise nimekirjast,
tühistada laenutaja poolt tehtud broneeringuid oma raamatutele või
märkida raamat laenutatuks või tagastatuks.

Laenutajal on võimalik otsida andmebaasis olevate raamatute seast
pealkirja, autori või ilmumisaasta järgi. Juhul kui raamat on saadaval,
siis on võimalik raamat kas broneerida või laenutada. Laenutajal on
võimalik enda poolt tehtud broneeringuid tühistada ning laenatud 
raamatud märkida tagastatuks.

## Installeerimine
Enne alustamist peaks olema installeeritud järgnev:
 - Python 3.9
 - NPM
 - Vue CLI 3

### Flask API ülesseadmine
Nõuded on saadaval failis requirements.txt

Installeerimiseks
```
pip install -r requirements.txt
```
Käivitamiseks
```
python run.py
```
### Vue.js kasutajaliidese ülesseadmine
Installeerimiseks
```
cd frontend
npm install
```
Käivitamiseks
```
npm run serve
```

## Kasutamine
Flask API on kasutamiseks saadaval `localhost:5000` 
ja Vue.js kasutajaliides `localhost:8080`.

### API päringud
Allpool on välja toodud kõik võimalikud päringud, mida Flask REST API võimaldab.

Iga päring, v.a. sisselogimine ja registreerimine, nõuab autoriseerimist.

Juhul kui päring vajab datat, siis siin on kirjeldatud selle formaat näidisena.

**Sisselogimine** 
`POST /login/`
```json
{
  "username": "kasutajatunnus", 
  "password": "parool"
}
```
**Registreerimine** 
`POST /register`
```json
{
  "username": "kasutajatunnus", 
  "password": "parool",
  "role": "lender"
}
```
Parameetri "role" väärtus saab olla "lender" (laenaja) või "borrower" (laenutaja)

**Raamatute nimekiri** 
`GET /books`

Päringule on võimalik lisada parameetreid 'title', 'author', 'year', 'filter'. 
Parameetri 'filter' väärtused saavad olla 'owned_by_me', 'borrowed_by_me' või 'reserved_by_me'.

Näiteks päringud:
GET /books?title=pealkiri või GET /books?filter=reserved_by_me

**Raamatu lisamine** 
`POST /books`
```json
{
  "title": "Harry Potter and Philosopher's Stone",
  "author": "J. K. Rowling", 
  "year": 1997
}
```

Järgnevatel päringutel URLi parameeter `id=[int]` sisaldab selle raamatu ID, mille kohta päritakse.

**Raamatu info**
`GET /book/:id`

**Raamatu eemaldamine** 
`DELETE /book/:id/`

**Raamatu välja laenamine** 
`POST /book/:id/lend`
```json
{
    "borrower": "kasutajanimi",
    "weeks": 4
}
```
Parameeter "borrower" peab sisaldama laenutaja kasutajanime. 
Parameeter "weeks" on valikuline ja määrab laenutuse kestuse nädalates.
Kui parameetrit ei määrata, siis kasutatakse vaikimisi laenutuse kestvust (neli nädalat).

**Raamatu laenutamine** 
`POST /book/:id/borrow`

**Raamatu tagastamine** 
`POST /book/:id/return`

**Raamatu broneerimine**
`POST /book/:id/reserve`

**Broneeringu tühistamine** 
`POST /book/:id/cancel`