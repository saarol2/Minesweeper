import haravasto as h
import random
import time

tilasto = {"valinta": 0, "pelaaja": None, "miinat": 0, "ruutuja_jaljella": 0, "koko_x": 0, "koko_y": 0,
    "aika": None, "vuorot": 0, "kesto": 0, "tulos": "Keskeytys"
}

kentta = []
jaljella = []

def valikko():
    """
    Valikko, missä kysytään haluaako pelaaja aloittaa uuden pelin, katsoa tilasto, vai lopettaa.
    Palauttaa pelaajan antaman vaihtoehdon.
    """
    print("(1) Aloita uusi peli")
    print("(2) Katso tilastot")
    print("(3) Lopeta")
    while True:
        try:
            tilasto['valinta'] = int(input("Anna vaihtoehdon numero: "))
        except ValueError:
            print("Anna pelkkä numero!")
        else:
            if tilasto['valinta'] < 1 or tilasto['valinta'] > 3:
                print("Tämä numero ei kuulu vaihtoehtoihin!")
            else:
                if tilasto['valinta'] >= 1 or tilasto['valinta'] <= 3:
                    return tilasto['valinta']

def tilastojen_tallennus():
    """
    Tallentaa tekstitiedostoon pelien tulokset
    """
    try:
        with open("tulokset.txt", "a") as lahde:
            lahde.write(f"{tilasto['pelaaja']}, {tilasto['aika']}, {tilasto['kesto']} s, {tilasto['vuorot']}, "
            f"{tilasto['miinat']}, {tilasto['koko_x']}x{tilasto['koko_y']}, {tilasto['tulos']}\n")
    except IOError:
        print("Tiedostoa ei voitu avata.")

def tilastojen_tulostus():
    """
    Tulostaa tilastot tekstitiedostosta, johon ne on tallennettu
    """
    try:
        with open ("tulokset.txt", "r") as lahde:
            for rivi in lahde:
                tulokset = rivi.rstrip()
                lista = tulokset.split(",")
                print(f"Pelaaja: {lista[0]}, aika: {lista[1]}, kesto: {lista[2]}, vuorot: {lista[3]}, "
                f"miinojen lkm: {lista[4]}, kentän koko: {lista[5]}, tulos: {lista[6]}.")
    except IOError:
        print("Tilastoja ei vielä ole.")


def luo_kentta():
    """
    Kysyy käyttäjältä kentän koon ja luo kentan, sekä vapaiden miinojen listan
    """
    while True:
        try:
            tilasto['koko_x'] = int(input("Anna kentän leveys: "))
            tilasto['koko_y'] = int(input("Anna kentän korkeus: "))
        except ValueError:
            print("Anna kokonaisluku!")
        else:
            if tilasto['koko_x'] < 2 or tilasto['koko_y'] < 2:
                print("Kentän reunojen täytyy olla suurempi kuin 1 ruutu!")
            else:
                break
    for rivi in range(tilasto['koko_y']):
        kentta.append([])
        for sarake in range(tilasto['koko_x']):
            kentta[-1].append(" ")
    for y in range(tilasto['koko_y']):
        for x in range(tilasto['koko_x']):
            jaljella.append((x, y))
    tilasto['ruutuja_jaljella'] = tilasto['koko_x'] * tilasto['koko_y']

def miinoita():
    """
    Kysyy käyttäjältä miinojen lukumäärän ja sijoittaa ne kentälle satunnaisesti.
    Poistaa lopuksi miinaruudut jaljella olevista ruuduista
    """
    while True:
        try:
            tilasto['miinat']= int(input("Anna miinojen lukumäärä: "))
            kentan_koko = len(kentta[len(kentta)-1]) * len(kentta)
        except ValueError:
            print("Anna kokonaisluku!")
        else:
            if tilasto['miinat'] <= 0 or tilasto['miinat'] >= kentan_koko:
                print("Miinojen määrä täytyy olla suurempi kuin 0 ja pienempi kuin kentän ruutujen lukumäärä!")
            else:
                break
    for line in range(tilasto['miinat']):  
        miina = list(random.choice(jaljella))
        x_koordinaatti = miina[0]
        y_koordinaatti = miina[1]
        kentta[y_koordinaatti][x_koordinaatti] = 'x'
        jaljella.remove((x_koordinaatti, y_koordinaatti))

def tulvataytto(x, y):
    """
    Tarkistaa onko ruudun viereisissä kohdissa miinoja ja laskee niiden määrän.
    Jos lähistöllä ei ole miinoja, ruutu merkitään tyhjäksi ja siirrytään sen viereisiin ruutuihin.
    """
    koordinaatit= [(x, y)]
    while koordinaatit:
        miinat = 0
        x, y = koordinaatit.pop()
        min_x = x - 1
        if min_x < 0:
            min_x = 0
        max_x = x + 1
        if max_x >= tilasto['koko_x']:
            max_x = tilasto['koko_x'] - 1
        min_y = y - 1
        if min_y < 0:
            min_y = 0
        max_y = y + 1
        if max_y >= tilasto['koko_y']:
            max_y = tilasto['koko_y'] - 1
        for j in range(min_y, max_y + 1):
            for i in range(min_x, max_x + 1):
                if kentta[j][i] == "x":
                    miinat += 1
        for j in range(min_y, max_y + 1):
            for i in range(min_x, max_x + 1):
                if kentta[j][i] == " " and miinat == 0:
                    koordinaatit.append((i, j))
        if kentta[y][x] == " ":
            tilasto['ruutuja_jaljella'] -= 1
        kentta[y][x] = str(miinat)

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    h.tyhjaa_ikkuna()
    h.piirra_tausta()
    h.aloita_ruutujen_piirto()
    for i, sarja in enumerate(kentta):
        for j, sarake in enumerate(sarja):
            if kentta[i][j] == 'x':
                h.lisaa_piirrettava_ruutu(" ", j * 40, i * 40)
            else:
                h.lisaa_piirrettava_ruutu(sarake, j * 40, i * 40)
    h.piirra_ruudut()
    
def kasittele_hiiri(x, y, nappi, muokkaus):
    """
    Käsittelee mitä kohtaa käyttäjä painaa ja tekee asioita napista riippuen
    """
    x = int(x/40)
    y = int(y/40)
    if nappi == h.HIIRI_VASEN:
        if kentta[y][x] == "x":
            h.aseta_piirto_kasittelija(piirra_kentta)
            tilasto['vuorot'] += 1
            tilasto['tulos'] = "häviö"
            print("Hävisit pelin!")
            h.lopeta()
        if kentta[y][x] == " ":
            tulvataytto(x, y)
            h.aseta_piirto_kasittelija(piirra_kentta)
            tilasto['vuorot'] += 1
            if tilasto['ruutuja_jaljella'] == tilasto['miinat']:
                tilasto['tulos'] = "voitto"
                print("Voitit pelin!")
                h.lopeta()

def main():
    """
    Pääohjelma. Kutsuu funktioita ja päivittää tilastoja.
    """
    tilasto['pelaaja'] = input("Pelaajan nimi: ")
    while True:
        valikko()
        if tilasto['valinta'] == 1:
            luo_kentta()
            miinoita()
            tilasto['aika'] = time.strftime("%d.%m.%Y %H:%M", time.localtime())
            tilasto['kesto'] = time.time()
            h.lataa_kuvat("spritet")
            h.luo_ikkuna(tilasto['koko_x'] * 40, tilasto['koko_y'] * 40)
            h.aseta_piirto_kasittelija(piirra_kentta)
            h.aseta_hiiri_kasittelija(kasittele_hiiri)
            h.aloita()
            tilasto['kesto'] = int(time.time() - tilasto['kesto'])
            tilastojen_tallennus()
            kentta.clear()
            jaljella.clear()
        elif tilasto['valinta'] == 2:
            tilastojen_tulostus()
        elif tilasto['valinta'] == 3:
            quit()
            break

if __name__ == "__main__":
    main()
