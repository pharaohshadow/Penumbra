"""
Card e CardDatabase - tutte le 150+15+15 carte del GDD
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Callable, Any
from .constants import Color, CardType


@dataclass
class Card:
    id: int
    name: str
    cost: int
    card_type: CardType
    color: Color
    atk: int = 0
    hp: int = 0
    text: str = ""
    is_boss: bool = False
    is_eldrazi: bool = False
    sacrifice_cost: int = 0          # solo Mostrissimi (2-6)
    keywords: List[str] = field(default_factory=list)  # "Flying", "Charge", "FirstStrike", "Trample", etc.
    # Funzione opzionale per effetti speciali (verrà collegata più avanti)
    effect: Optional[Callable] = None

    def __str__(self) -> str:
        if self.card_type == CardType.MONSTER or self.card_type == CardType.BOSS or self.card_type == CardType.ELDRAZI:
            return f"[{self.cost}] {self.name} ({self.atk}/{self.hp}) - {self.color.value}"
        return f"[{self.cost}] {self.name} ({self.card_type.value}) - {self.color.value}"

    def is_creature(self) -> bool:
        return self.card_type in (CardType.MONSTER, CardType.BOSS, CardType.ELDRAZI, CardType.NEUTRAL)


class CardDatabase:
    """Carica e fornisce tutte le carte del gioco."""

    def __init__(self):
        self.cards: Dict[int, Card] = {}
        self.by_color: Dict[Color, List[Card]] = {c: [] for c in Color}
        self.bosses: List[Card] = []
        self.eldrazi: List[Card] = []
        self._load_all()

    def _add(self, card: Card):
        self.cards[card.id] = card
        self.by_color[card.color].append(card)
        if card.is_boss:
            self.bosses.append(card)
        if card.is_eldrazi:
            self.eldrazi.append(card)

    def get(self, card_id: int) -> Optional[Card]:
        return self.cards.get(card_id)

    def get_by_color(self, color: Color) -> List[Card]:
        return self.by_color[color]

    def get_draftable(self, color: Optional[Color] = None) -> List[Card]:
        """Carte draftabili (costo 0-5, non boss, non eldrazi, non grigie)."""
        result = []
        for c in self.cards.values():
            if c.is_boss or c.is_eldrazi or c.color == Color.GRAY:
                continue
            if c.cost > 5:
                continue
            if color and c.color != color:
                continue
            result.append(c)
        return result

    def _load_all(self):
        """Carica l'intero database dal GDD (estratto completo)."""
        # ========== BIANCO ==========
        self._add(Card(1, "Scudiero di Luce", 0, CardType.MONSTER, Color.WHITE, 0, 2, "Difesa +1 agli alleati adiacenti.", keywords=["DefenderAura"]))
        self._add(Card(2, "Preghiera Mattutina", 0, CardType.CURSE, Color.WHITE, text="Fornisce 1 Mana temporaneo nel prossimo turno."))
        self._add(Card(3, "Raggio Solare", 0, CardType.CURSE, Color.WHITE, text="Cura 1 HP a una creatura bersaglio."))
        self._add(Card(4, "Trappola Luminosa", 0, CardType.TRAP, Color.WHITE, text="Rivela e blocca per 1 turno la prima creatura nemica che entra nella casella."))
        self._add(Card(5, "Benedizione Minore", 0, CardType.CURSE, Color.WHITE, text="+1 HP massimo a una creatura alleata."))

        self._add(Card(6, "Guardiano del Tempio", 1, CardType.MONSTER, Color.WHITE, 1, 3, "Non può attaccare nel turno in cui viene evocato.", keywords=["SummoningSickness"]))
        self._add(Card(7, "Accolito Benefico", 1, CardType.MONSTER, Color.WHITE, 1, 2, "All'evocazione, cura 1 HP all'alleato più ferito."))
        self._add(Card(8, "Scudo di Fede", 1, CardType.CURSE, Color.WHITE, text="Conferisce uno scudo da 2 HP che assorbe i prossimi danni."))
        self._add(Card(9, "Flash Sacro", 1, CardType.CURSE, Color.WHITE, text="Riduce di 1 l'ATK di un nemico fino al termine del turno."))
        self._add(Card(10, "Santuario Portatile", 1, CardType.TRAP, Color.WHITE, text="Crea una zona dove gli alleati rigenerano 1 HP a inizio turno."))

        self._add(Card(11, "Paladino dell'Alba", 2, CardType.MONSTER, Color.WHITE, 2, 3, "Subisce 1 danno in meno dagli attacchi nemici.", keywords=["ReduceDamage1"]))
        self._add(Card(12, "Clerico della Guarigione", 2, CardType.MONSTER, Color.WHITE, 1, 4, "Tap: Cura 2 HP a una creatura adiacente."))
        self._add(Card(13, "Giudizio Divino", 2, CardType.CURSE, Color.WHITE, text="Infligge 2 danni a una creatura nemica con la Corona."))
        self._add(Card(14, "Sigillo della Purezza", 2, CardType.CURSE, Color.WHITE, text="Rimuove tutte le maledizioni e i debuff da una creatura alleata."))
        self._add(Card(15, "Barriera Radiosa", 2, CardType.TRAP, Color.WHITE, text="Annulla il prossimo attacco sferrato su questa casella."))

        self._add(Card(16, "Crociato Inamovibile", 3, CardType.MONSTER, Color.WHITE, 3, 4, "Non può essere respinto dal Rimbalzo.", keywords=["Unbounceable"]))
        self._add(Card(17, "Angelo Custode", 3, CardType.MONSTER, Color.WHITE, 2, 4, "Veloce; reindirizza su di sé gli attacchi diretti alle creature adiacenti.", keywords=["Flying", "Redirect"]))
        self._add(Card(18, "Luce Purificatrice", 3, CardType.CURSE, Color.WHITE, text="Infligge 2 danni a tutte le creature nemiche in una riga."))
        self._add(Card(19, "Corazza Celestiale", 3, CardType.CURSE, Color.WHITE, text="+2 HP e +1 ATK permanenti ad un alleato."))
        self._add(Card(20, "Specchio della Verità", 3, CardType.TRAP, Color.WHITE, text="Ritorna il 50% dei danni subiti all'attaccante nemico."))

        self._add(Card(21, "Inquisitore Solare", 4, CardType.MONSTER, Color.WHITE, 4, 4, "Ignora la difesa e gli scudi nemici quando attacca.", keywords=["IgnoreDefense"]))
        self._add(Card(22, "Monolito di Luce", 4, CardType.MONSTER, Color.WHITE, 0, 8, "Struttura immobile; gli alleati entro 2 caselle guadagnano +1 ATK.", keywords=["Immobile", "AuraATK"]))
        self._add(Card(23, "Resurrezione Sacra", 4, CardType.CURSE, Color.WHITE, text="Evoca un mostro di costo 2 o inferiore precedentemente distrutto."))
        self._add(Card(24, "Furia Inquisitoria", 4, CardType.CURSE, Color.WHITE, text="Una creatura alleata attacca immediatamente senza spendere azioni."))
        self._add(Card(25, "Santuario Inviolabile", 4, CardType.TRAP, Color.WHITE, text="Rende invulnerabile la casella per un intero turno."))

        self._add(Card(26, "Serafino della Giustizia", 5, CardType.MONSTER, Color.WHITE, 5, 5, "Volante; ripristina 2 HP a tutti gli alleati ad ogni attacco con successo.", keywords=["Flying", "HealOnAttack"]))
        self._add(Card(27, "Campione del Voto", 5, CardType.MONSTER, Color.WHITE, 4, 6, "Ottiene +2 ATK se il Comandante alleato ha subito danni nel turno."))
        self._add(Card(28, "Apocalisse Radiosa", 5, CardType.CURSE, Color.WHITE, text="Infligge 3 danni a tutte le creature sul tabellone tranne quelle incoronate."))
        self._add(Card(29, "Aegis Suprema", 5, CardType.CURSE, Color.WHITE, text="Concede Invulnerabilità a una creatura per 1 turno intero."))
        self._add(Card(30, "Giudizio Finale", 5, CardType.TRAP, Color.WHITE, text="Distrugge la prima creatura nemica di costo 4+ che muove sulla casella."))

        # Boss Bianco
        self._add(Card(151, "Auriel, l'Arcangelo della Luce Suprema", 6, CardType.BOSS, Color.WHITE, 6, 8,
                       "Volante; Invulnerabile alle Maledizioni nemiche. Aura di Luce: Tutte le creature alleate rigenerano 2 HP all'inizio di ogni turno e guadagnano Scudo Sacro (+2 HP assorbiti).",
                       is_boss=True, keywords=["Flying", "CurseImmune", "AuraRegen2", "SacredShield"]))
        self._add(Card(152, "Bastione Inviolabile di Solaria", 6, CardType.BOSS, Color.WHITE, 0, 15,
                       "Struttura Divina Immobile. Impedisce qualsiasi movimento nemico entro 2 caselle. Ogni volta che un alleato subisce danni, Solaria assorbe l'impatto riducendolo a 0.",
                       is_boss=True, keywords=["Immobile", "ZoneControl", "DamageRedirect"]))
        self._add(Card(153, "Giudizio del Creatore", 6, CardType.BOSS, Color.WHITE, 0, 0,
                       "Distrugge istantaneamente tutte le creature nemiche con ATK ≥ 4. Ripristina completamente gli HP del tuo Comandante e di tutte le creature alleate.",
                       is_boss=True))

        # ========== BLU ==========
        self._add(Card(31, "Illusione di Fumo", 0, CardType.MONSTER, Color.BLUE, 0, 1, "Svanisce subendo qualsiasi danno senza concedere ricompense.", keywords=["Vanish"]))
        self._add(Card(32, "Calcolo Arcano", 0, CardType.CURSE, Color.BLUE, text="Guarda la prima tessera del mazzo Eventi."))
        self._add(Card(33, "Spinta Telecinetica", 0, CardType.CURSE, Color.BLUE, text="Sposta una creatura adiacente di 1 casella ortogonale."))
        self._add(Card(34, "Runica Ingannevole", 0, CardType.TRAP, Color.BLUE, text="Inverte la direzione di movimento della creatura che la attiva."))
        self._add(Card(35, "Micro-Portale", 0, CardType.CURSE, Color.BLUE, text="Scambia di posto due tessere adiacenti non esplorate."))
        self._add(Card(36, "Apprendista Arcano", 1, CardType.MONSTER, Color.BLUE, 1, 1, "All'evocazione, riduce di 1 il costo della prossima Maledizione giocata."))
        self._add(Card(37, "Elementale di Nebbia", 1, CardType.MONSTER, Color.BLUE, 0, 3, "Non può essere attaccato da creature a distanza."))
        self._add(Card(38, "Annullamento Arcano", 1, CardType.CURSE, Color.BLUE, text="Annulla la Maledizione appena giocata dall'avversario."))
        self._add(Card(39, "Mente Confusa", 1, CardType.CURSE, Color.BLUE, text="Impedisce ad una creatura nemica di usare abilità per 1 turno."))
        self._add(Card(40, "Trappola d'Etere", 1, CardType.TRAP, Color.BLUE, text="Sottrae 1 Mana al nemico quando passa sulla casella."))
        self._add(Card(41, "Mago delle Specchiature", 2, CardType.MONSTER, Color.BLUE, 2, 2, "All'evocazione, crea una copia illusoria 0/1 di se stesso."))
        self._add(Card(42, "Guardiano dei Portali", 2, CardType.MONSTER, Color.BLUE, 1, 4, "Può muoversi da qualsiasi Portale verso un altro Portale attivo spendendo 0 Mana.", keywords=["PortalWalker"]))
        self._add(Card(43, "Trasposizione Mentale", 2, CardType.CURSE, Color.BLUE, text="Scambia la posizione di due creature alleate sulla mappa."))
        self._add(Card(44, "Congelamento Temporale", 2, CardType.CURSE, Color.BLUE, text="Blocca completamente una creatura nemica per 1 turno."))
        self._add(Card(45, "Illusione Ottica", 2, CardType.TRAP, Color.BLUE, text="Teletrasporta l'attaccante in una casella casuale prima dell'impatto."))
        self._add(Card(46, "Tessere-Teleporte", 3, CardType.MONSTER, Color.BLUE, 2, 3, "Può trasportare con sé un alleato adiacente durante il movimento."))
        self._add(Card(47, "Drenatore di Magia", 3, CardType.MONSTER, Color.BLUE, 3, 2, "Guadagna +1 ATK ogni volta che viene giocata una Maledizione."))
        self._add(Card(48, "Distorsione Spaziale", 3, CardType.CURSE, Color.BLUE, text="Ruota la configurazione di un blocco 2x2 di caselle di 90 gradi."))
        self._add(Card(49, "Dominio Mentale", 3, CardType.CURSE, Color.BLUE, text="Prendi il controllo di una creatura nemica di costo 1 o 2 per 1 turno."))
        self._add(Card(50, "Sigillo di Riflessione", 3, CardType.TRAP, Color.BLUE, text="Copia e attiva la stessa abilità usata dall'avversario sulla casella."))
        self._add(Card(51, "Architetto del Caos", 4, CardType.MONSTER, Color.BLUE, 3, 5, "All'evocazione, rimescola tutte le tessere Evento non ancora scoperte."))
        self._add(Card(52, "Sfinge degli Enigmi", 4, CardType.MONSTER, Color.BLUE, 4, 4, "Il nemico deve spendere +1 Mana per attaccare questa creatura."))
        self._add(Card(53, "Vento Arcano", 4, CardType.CURSE, Color.BLUE, text="Sposta tutte le creature nemiche di 1 casella indietro rispetto alla direzione in cui guardano."))
        self._add(Card(54, "Furto di Memoria", 4, CardType.CURSE, Color.BLUE, text="Costringe il nemico a scartare 1 carta dalla mano a tua scelta."))
        self._add(Card(55, "Labirinto Mentale", 4, CardType.TRAP, Color.BLUE, text="Intrappola una creatura in una dimensione parallela per 2 turni."))
        self._add(Card(56, "Signore delle Illusioni", 5, CardType.MONSTER, Color.BLUE, 4, 5, "Inizio turno: Evoca una copia spettrale di una creatura nemica a scelta."))
        self._add(Card(57, "Drago dell'Etere", 5, CardType.MONSTER, Color.BLUE, 5, 4, "Volante; incorporeo (50% di probabilità di ignorare qualsiasi attacco o danni).", keywords=["Flying", "Incorporeal"]))
        self._add(Card(58, "Singolarità Dimensionale", 5, CardType.CURSE, Color.BLUE, text="Attira tutte le creature sulla mappa verso il centro C3 di 1 passo."))
        self._add(Card(59, "Riscrittura della Realtà", 5, CardType.CURSE, Color.BLUE, text="Scambia la posizione del tuo Comandante con quella del Comandante nemico."))
        self._add(Card(60, "Vuoto Assoluto", 5, CardType.TRAP, Color.BLUE, text="Rimuove dal gioco la creatura nemica che attiva la casella per il resto della partita."))

        # Boss Blu
        self._add(Card(154, "Aethelgard, il Sovrano delle Illusioni", 6, CardType.BOSS, Color.BLUE, 5, 7,
                       "All'evocazione crea 3 copie esatte di se stesso. Solo un attacco diretto rivela il vero Aethelgard.",
                       is_boss=True, keywords=["IllusionCopies"]))
        self._add(Card(155, "Chronos, il Signore del Tempo", 6, CardType.BOSS, Color.BLUE, 6, 6,
                       "All'inizio del tuo turno puoi riavvolgere lo stato del tabellone al turno precedente (danni al Comandante restano).",
                       is_boss=True, keywords=["TimeControl"]))
        self._add(Card(156, "Singolarità del Vuoto Eterno", 6, CardType.BOSS, Color.BLUE, 0, 0,
                       "Rimuove tutte le tessere Evento e Trappole. Congela il Comandante nemico per 1 turno.",
                       is_boss=True))

        # ========== ROSSO ==========
        self._add(Card(61, "Goblin Kamikaze", 0, CardType.MONSTER, Color.RED, 1, 1, "Alla morte, infligge 1 danno a tutte le creature adiacenti.", keywords=["Deathrattle"]))
        self._add(Card(62, "Spark di Fuoco", 0, CardType.CURSE, Color.RED, text="Infligge 1 danno a una creatura bersaglio."))
        self._add(Card(63, "Carica Frenetica", 0, CardType.CURSE, Color.RED, text="Fornisce +1 ATK ma -1 HP ad una creatura per questo turno."))
        self._add(Card(64, "Mina Esplosiva", 0, CardType.TRAP, Color.RED, text="Infligge 1 danno alla prima creatura che muove sulla casella."))
        self._add(Card(65, "Sangue Bollente", 0, CardType.CURSE, Color.RED, text="Fai subire 1 danno al tuo Comandante per guadagnare +1 ATK su una creatura."))
        self._add(Card(66, "Berserker di Sangue", 1, CardType.MONSTER, Color.RED, 2, 1, "Carica (può muoversi ed attaccare subito nel turno di evocazione).", keywords=["Charge"]))
        self._add(Card(67, "Elementale di Fuoco", 1, CardType.MONSTER, Color.RED, 2, 2, "Infligge 1 danno al suo attaccante ad ogni scontro.", keywords=["Thorns1"]))
        self._add(Card(68, "Dardo Pyrico", 1, CardType.CURSE, Color.RED, text="Infligge 2 danni diretti ad una creatura nemica."))
        self._add(Card(69, "Smania di Distruzione", 1, CardType.CURSE, Color.RED, text="Una creatura deve attaccare nel turno corrente se ne ha la possibilità."))
        self._add(Card(70, "Trappola Incendiaria", 1, CardType.TRAP, Color.RED, text="Infligge 2 danni in area 3x3 attorno alla casella attivata."))
        self._add(Card(71, "Sciamano del Vulcano", 2, CardType.MONSTER, Color.RED, 3, 1, "Tap: Infligge 1 danno a qualsiasi bersaglio entro 2 caselle."))
        self._add(Card(72, "Segugio Infernale", 2, CardType.MONSTER, Color.RED, 3, 2, "Movimento di 2 passi in diagonale invece di 1.", keywords=["DoubleMove"]))
        self._add(Card(73, "Esplosione Magmatica", 2, CardType.CURSE, Color.RED, text="Infligge 3 danni ad una creatura e 1 danno al suo proprietario."))
        self._add(Card(74, "Ondata di Furia", 2, CardType.CURSE, Color.RED, text="Tutte le creature alleate guadagnano +1 ATK fino a fine turno."))
        self._add(Card(75, "Superficie Lavica", 2, CardType.TRAP, Color.RED, text="Trasforma la casella in terreno vulcanico permanente."))
        self._add(Card(76, "Ogre Frantumatore", 3, CardType.MONSTER, Color.RED, 4, 3, "Distrugge i muri d'illusione o ostacoli quando vi muove sopra.", keywords=["Wallbreaker"]))
        self._add(Card(77, "Cavaliere del Caos", 3, CardType.MONSTER, Color.RED, 4, 2, "Carica; Iniziativa (colpisce sempre per primo).", keywords=["Charge", "FirstStrike"]))
        self._add(Card(78, "Piroclasma", 3, CardType.CURSE, Color.RED, text="Infligge 2 danni a TUTTE le creature sul tabellone."))
        self._add(Card(79, "Immolazione", 3, CardType.CURSE, Color.RED, text="Distruggi un tuo mostro per infliggere i suoi HP attuali come danni a un nemico."))
        self._add(Card(80, "Imboscata Caotica", 3, CardType.TRAP, Color.RED, text="Evoca un Berserker 2/1 direttamente sulla casella quando un nemico vi entra."))
        self._add(Card(81, "Manticora Furente", 4, CardType.MONSTER, Color.RED, 5, 3, "Volante; infligge 2 danni alle creature adiacenti ad ogni eliminazione.", keywords=["Flying", "DeathrattleArea"]))
        self._add(Card(82, "Gigante della Cenere", 4, CardType.MONSTER, Color.RED, 5, 5, "Subisce 1 danno extra dalle fonti di elemento Blu o Acqua."))
        self._add(Card(83, "Pioggia di Meteore", 4, CardType.CURSE, Color.RED, text="Infligge 4 danni distribuiti casualmente tra le creature nemiche."))
        self._add(Card(84, "Sacrificio del Sangue", 4, CardType.CURSE, Color.RED, text="Ottieni +3 Mana immediatamente subendo 3 danni al Comandante."))
        self._add(Card(85, "Campo Minato", 4, CardType.TRAP, Color.RED, text="Piazzi 3 mine trasparenti su 3 caselle adiacenti a scelta."))
        self._add(Card(86, "Idra vulcanica", 5, CardType.MONSTER, Color.RED, 6, 4, "Può attaccare due volte per turno spendendo Mana normalmente.", keywords=["DoubleAttack"]))
        self._add(Card(87, "Demone della Distruzione", 5, CardType.MONSTER, Color.RED, 6, 5, "Distrugge la tessera su cui atterra eliminando ogni effetto di gioco presente."))
        self._add(Card(88, "Cataclisma Infernale", 5, CardType.CURSE, Color.RED, text="Infligge 5 danni a una creatura e 2 danni a tutte le unità vicine."))
        self._add(Card(89, "Collerico Risveglio", 5, CardType.CURSE, Color.RED, text="Raddoppia l'ATK di un tuo mostro fino a fine turno."))
        self._add(Card(90, "Annientamento Totale", 5, CardType.TRAP, Color.RED, text="Distrugge istantaneamente l'attaccante ed il difensore coinvolti nello scontro."))

        # Boss Rosso
        self._add(Card(157, "Ignis, il Titanico Drago del Vulcano", 6, CardType.BOSS, Color.RED, 8, 6,
                       "Volante; Carica Divina. Ogni movimento/attacco incendia la casella (Magma 2 danni). Infligge 3 danni ad area.",
                       is_boss=True, keywords=["Flying", "Charge", "MagmaTrail", "AreaDamage"]))
        self._add(Card(158, "Malakor, Incarnazione della Furia", 6, CardType.BOSS, Color.RED, 9, 4,
                       "Primo Colpo Assoluto; Inarrestabile. Quando elimina, può muovere e attaccare di nuovo a costo 0.",
                       is_boss=True, keywords=["AbsoluteFirstStrike", "Unstoppable", "ExtraAttack"]))
        self._add(Card(159, "Supernova Catastrofica", 6, CardType.BOSS, Color.RED, 0, 0,
                       "Infligge 6 danni a TUTTE le creature e 3 danni a entrambi i Comandanti. Distrugge tutte le tessere non-struttura.",
                       is_boss=True))

        # ========== NERO ==========
        self._add(Card(91, "Scheletro Putrefatto", 0, CardType.MONSTER, Color.BLACK, 1, 1, "Ritorna in campo una volta con 1 HP dopo la prima morte.", keywords=["Reborn"]))
        self._add(Card(92, "Tocco della Fossa", 0, CardType.CURSE, Color.BLACK, text="Riduce di 1 l'ATK nemico in modo permanente."))
        self._add(Card(93, "Succhiasangue", 0, CardType.CURSE, Color.BLACK, text="Infligge 1 danno ad un nemico e cura 1 HP al tuo Comandante."))
        self._add(Card(94, "Fossa delle Ombre", 0, CardType.TRAP, Color.BLACK, text="Rallenta la creatura attivante impedendole di muoversi per il prossimo turno."))
        self._add(Card(95, "Patto Oscuro", 0, CardType.CURSE, Color.BLACK, text="Distruggi un tuo mostro 1/1 per recuperare 1 Mana."))
        self._add(Card(96, "Ghoul Corpse", 1, CardType.MONSTER, Color.BLACK, 2, 1, "Guadagna +1/+1 ad ogni creatura distrutta sul tabellone.", keywords=["GrowthOnDeath"]))
        self._add(Card(97, "Ombra Strisciante", 1, CardType.MONSTER, Color.BLACK, 1, 2, "Può attraversare le creature nemiche senza iniziare scontri.", keywords=["PassThrough"]))
        self._add(Card(98, "Drenaggio d'Anima", 1, CardType.CURSE, Color.BLACK, text="Infligge 2 danni ad una creatura ferita."))
        self._add(Card(99, "Maledizione della Putrefazione", 1, CardType.CURSE, Color.BLACK, text="La creatura nemica perde 1 HP all'inizio di ogni suo turno."))
        self._add(Card(100, "Nebbia Corroder", 1, CardType.TRAP, Color.BLACK, text="Infligge 1 danno e riduce l'ATK di 1 a chiunque entri nella casella."))
        self._add(Card(101, "Vampiro delle Ombre", 2, CardType.MONSTER, Color.BLACK, 2, 3, "Rubavita (si cura di pari danni inflitti).", keywords=["Lifesteal"]))
        self._add(Card(102, "Necromante Novizio", 2, CardType.MONSTER, Color.BLACK, 1, 3, "Tap: Evoca uno Scheletro 1/1 nella tua zona di Spawn."))
        self._add(Card(103, "Esecuzione", 2, CardType.CURSE, Color.BLACK, text="Distruggi una creatura nemica che ha 2 o meno HP rimanenti."))
        self._add(Card(104, "Pestilenza Diffusa", 2, CardType.CURSE, Color.BLACK, text="Infligge 1 danno a tutte le creature non-morte o danneggiate."))
        self._add(Card(105, "Risucchioso Mortale", 2, CardType.TRAP, Color.BLACK, text="Cura il tuo Comandante di 2 HP quando il nemico entra nella casella."))
        self._add(Card(106, "Mietitore di Anime", 3, CardType.MONSTER, Color.BLACK, 3, 3, "Ottiene il controllo del Frammento d'Anima nemico per 1 turno se elimina la Regina."))
        self._add(Card(107, "Spettro del Terrore", 3, CardType.MONSTER, Color.BLACK, 3, 2, "Le creature adiacenti subiscono un debuff di -1 ATK."))
        self._add(Card(108, "Rianimazione Oscura", 3, CardType.CURSE, Color.BLACK, text="Riporta in vita un mostro distrutto di costo 3 o meno sul tabellone."))
        self._add(Card(109, "Agonia Infinità", 3, CardType.CURSE, Color.BLACK, text="Una creatura target subisce danni pari al numero di mostri nel tuo cimitero."))
        self._add(Card(110, "Maledizione del Cimitero", 3, CardType.TRAP, Color.BLACK, text="Evoca due Scheletri 1/1 attorno al nemico che calpesta la tessera."))
        self._add(Card(111, "Cavaliere della Morte", 4, CardType.MONSTER, Color.BLACK, 4, 4, "Iniziativa; infligge danni diretti al Comandante se elimina un bersaglio.", keywords=["FirstStrike", "CommanderDamage"]))
        self._add(Card(112, "Lich Necromante", 4, CardType.MONSTER, Color.BLACK, 2, 6, "Gli scheletri e gli zombi alleati ottengono +1/+1 e Rubavita."))
        self._add(Card(113, "Olocausto d'Ombra", 4, CardType.CURSE, Color.BLACK, text="Distruggi una creatura alleata ed una creatura nemica a tua scelta."))
        self._add(Card(114, "Corruzione Mentale", 4, CardType.CURSE, Color.BLACK, text="Prendi il controllo definitivo di una creatura nemica ferita."))
        self._add(Card(115, "Portale della Fossa", 4, CardType.TRAP, Color.BLACK, text="Inghiotte la creatura nemica rispedendola nella mano del suo proprietario."))
        self._add(Card(116, "Signore dei Lich", 5, CardType.MONSTER, Color.BLACK, 5, 5, "Non può essere distrutto finché sono presenti scheletri alleati in campo.", keywords=["ConditionalImmune"]))
        self._add(Card(117, "Abominio Necrotico", 5, CardType.MONSTER, Color.BLACK, 6, 6, "Perde 1 HP all'inizio di ogni tuo turno come costo di mantenimento."))
        self._add(Card(118, "Decreti della Morte", 5, CardType.CURSE, Color.BLACK, text="Distruggi tutte le creature non-incoronate con meno di 3 HP."))
        self._add(Card(119, "Resurrezione di Massa", 5, CardType.CURSE, Color.BLACK, text="Riempi tutte le tue caselle liberate con Scheletri 1/1."))
        self._add(Card(120, "Mietitura Finale", 5, CardType.TRAP, Color.BLACK, text="Elimina il nemico ed evoca un Vampiro 2/3 sotto il tuo controllo."))

        # Boss Nero
        self._add(Card(160, "Thanatos, il Mietitore Supremo", 6, CardType.BOSS, Color.BLACK, 7, 7,
                       "Tocco della Morte: qualsiasi creatura colpita viene distrutta istantaneamente. Evoca Spettro 3/3 sulla casella della vittima.",
                       is_boss=True, keywords=["DeathTouch", "SpawnSpecter"]))
        self._add(Card(161, "Lord Vex, l'Immortale Signore dei Lich", 6, CardType.BOSS, Color.BLACK, 4, 10,
                       "Non può subire danni finché è presente almeno un'altra creatura alleata. Guadagna +1 ATK permanente per ogni alleato morto.",
                       is_boss=True, keywords=["ConditionalImmune", "GrowthOnAllyDeath"]))
        self._add(Card(162, "Apocalisse della Fossa Mortale", 6, CardType.BOSS, Color.BLACK, 0, 0,
                       "Prende il controllo di tutte le creature nel cimitero avversario e le rievoca con +1/+1 e Carica.",
                       is_boss=True))

        # ========== VERDE ==========
        self._add(Card(121, "Germoglio Selvaggio", 0, CardType.MONSTER, Color.GREEN, 0, 2, "All'inizio del turno guadagna +1 HP di crescita naturale.", keywords=["Growth"]))
        self._add(Card(122, "Radici Ancoranti", 0, CardType.CURSE, Color.GREEN, text="Impedisce ad una creatura di essere spostata da abilità per 1 turno."))
        self._add(Card(123, "Linfa Vitale", 0, CardType.CURSE, Color.GREEN, text="Fornisce +1 HP massimo ad una creatura alleata."))
        self._add(Card(124, "Liana Nascosta", 0, CardType.TRAP, Color.GREEN, text="Blocco del movimento: ferma la creatura nella casella attivata."))
        self._add(Card(125, "Symbiosis Minore", 0, CardType.CURSE, Color.GREEN, text="Distribuisce 1 HP tra due creature alleate adiacenti."))
        self._add(Card(126, "Lupo della Foresta", 1, CardType.MONSTER, Color.GREEN, 2, 1, "Branco: guadagna +1 ATK per ogni altro Lupo adiacente.", keywords=["Pack"]))
        self._add(Card(127, "Treant Protetto", 1, CardType.MONSTER, Color.GREEN, 1, 3, "Difesa +1; immune ai danni da trappole ambientali.", keywords=["TrapImmune"]))
        self._add(Card(128, "Crescita Rigogliosa", 1, CardType.CURSE, Color.GREEN, text="Fai guadagnare permanentemente +1/+1 ad una creatura."))
        self._add(Card(129, "Richiamo Selvaggio", 1, CardType.CURSE, Color.GREEN, text="Evoca un Lupo 2/1 nella tua zona di Spawn."))
        self._add(Card(130, "Fossa Rampicante", 1, CardType.TRAP, Color.GREEN, text="Infligge 1 danno e immobilizza il target per 1 turno."))
        self._add(Card(131, "Orso della Tundra", 2, CardType.MONSTER, Color.GREEN, 3, 3, "Statistiche pure elevate per il costo."))
        self._add(Card(132, "Druido della Terra", 2, CardType.MONSTER, Color.GREEN, 2, 2, "Tap: Fornisce +1 Mana alla tua riserva per il turno corrente."))
        self._add(Card(133, "Pelle di Pietra", 2, CardType.CURSE, Color.GREEN, text="Conferisce +3 HP ma riduce il movimento di 1 passo a una creatura."))
        self._add(Card(134, "Forzatura della Natura", 2, CardType.CURSE, Color.GREEN, text="Cura completamente gli HP di un mostro di costo 3 o inferiore."))
        self._add(Card(135, "Spine Difensive", 2, CardType.TRAP, Color.GREEN, text="Infligge 2 danni a chiunque attacchi la creatura su questa casella."))
        self._add(Card(136, "Ragno gigante", 3, CardType.MONSTER, Color.GREEN, 2, 5, "Raggiungere (può attaccare le creature Volanti senza penalità).", keywords=["Reach"]))
        self._add(Card(137, "Centauro Cacciatore", 3, CardType.MONSTER, Color.GREEN, 4, 3, "Movimento esteso in linea retta spendendo 1 Mana extra."))
        self._add(Card(138, "Forza Gigantesca", 3, CardType.CURSE, Color.GREEN, text="+3/+3 ad una creatura fino al termine del turno corrente."))
        self._add(Card(139, "Terremoto Improvviso", 3, CardType.CURSE, Color.GREEN, text="Distruggi tutte le strutture ed i muri d'illusione in campo."))
        self._add(Card(140, "Tana Improvvisata", 3, CardType.TRAP, Color.GREEN, text="Evoca un Orso 3/3 quando un nemico entra nella tua zona di campo."))
        self._add(Card(141, "Treant Antico", 4, CardType.MONSTER, Color.GREEN, 4, 6, "Rigenerazione: ripristina 1 HP a inizio di ogni tuo turno.", keywords=["Regenerate"]))
        self._add(Card(142, "Mastodonte delle Selve", 4, CardType.MONSTER, Color.GREEN, 5, 5, "Travolgere (i danni in eccesso rispetto agli HP del difensore vanno al Comandante).", keywords=["Trample"]))
        self._add(Card(143, "Risveglio della Foresta", 4, CardType.CURSE, Color.GREEN, text="Trasforma una tessera neutrale in un Treant 3/3 permanente."))
        self._add(Card(144, "Vigore Ancestrale", 4, CardType.CURSE, Color.GREEN, text="Raddoppia gli HP attuali di tutte le tue creature in campo."))
        self._add(Card(145, "Radici strangolatrici", 4, CardType.TRAP, Color.GREEN, text="Cattura un nemico infliggendogli 2 danni al turno finché non viene liberato."))
        self._add(Card(146, "Idra delle Nebbie", 5, CardType.MONSTER, Color.GREEN, 5, 7, "Guadagna +1 ATK ogni volta che subisce danni e sopravvive.", keywords=["Rage"]))
        self._add(Card(147, "Behemoth Primordiale", 5, CardType.MONSTER, Color.GREEN, 7, 6, "Distrugge le tessere su cui passa e non può essere bloccato da trappole.", keywords=["DestroyTiles", "TrapImmune"]))
        self._add(Card(148, "Furia della Terra", 5, CardType.CURSE, Color.GREEN, text="Tutte le tue creature possono attaccare due volte in questo turno."))
        self._add(Card(149, "Benedizione di Gaia", 5, CardType.CURSE, Color.GREEN, text="Fornisce +2/+2 ed Invulnerabilità per 1 turno a tutte le tue creature."))
        self._add(Card(150, "Vendetta della Natura", 5, CardType.TRAP, Color.GREEN, text="Elimina la creatura nemica ed evoca al suo posto un Treant 4/6 sotto il tuo controllo."))

        # Boss Verde
        self._add(Card(163, "Yggdrasil, il Gigante Primordiale", 6, CardType.BOSS, Color.GREEN, 8, 12,
                       "Travolgere; Rigenerazione Suprema (4 HP). Raggio d'attacco 2 caselle in tutte le direzioni.",
                       is_boss=True, keywords=["Trample", "SuperRegen", "Reach2"]))
        self._add(Card(164, "Ursa, la Madre della Foresta", 6, CardType.BOSS, Color.GREEN, 7, 9,
                       "All'evocazione e a inizio turno evoca due Orsi 3/3. Bestie e Treant alleati ottengono +2/+2 e Travolgere.",
                       is_boss=True, keywords=["SpawnBears", "BeastBuff"]))
        self._add(Card(165, "Risveglio della Terra Primordiale", 6, CardType.BOSS, Color.GREEN, 0, 0,
                       "Raddoppia permanentemente ATK e HP di tutte le creature alleate. Per 2 turni muovono e attaccano senza spendere Mana.",
                       is_boss=True))

        # ========== MOSTRISSIMI ELDRAZZICI (Grigi) ==========
        self._add(Card(201, "Behemoth dei Sepolcri", 0, CardType.ELDRAZI, Color.GRAY, 4, 5, "Recupera 1 HP ogni volta che elimina una creatura nemica.", is_eldrazi=True, sacrifice_cost=2, keywords=["LifestealOnKill"]))
        self._add(Card(202, "Sgranocchiatore d'Etere", 0, CardType.ELDRAZI, Color.GRAY, 5, 3, "Sottrae 1 Mana al proprietario della creatura colpita.", is_eldrazi=True, sacrifice_cost=2))
        self._add(Card(203, "Orrore Strisciante", 0, CardType.ELDRAZI, Color.GRAY, 3, 6, "Può muoversi di 2 caselle diagonali se non effettua attacchi.", is_eldrazi=True, sacrifice_cost=2, keywords=["DoubleMoveNoAttack"]))
        self._add(Card(204, "Devastatore Abissale", 0, CardType.ELDRAZI, Color.GRAY, 6, 6, "Infligge 1 danno ad area a tutte le creature adiacenti all'evocazione.", is_eldrazi=True, sacrifice_cost=3, keywords=["AreaOnSummon"]))
        self._add(Card(205, "Inseguitore delle Ombre", 0, CardType.ELDRAZI, Color.GRAY, 5, 7, "Iniziativa; ignora i terreni difficili e le trappole ambientali.", is_eldrazi=True, sacrifice_cost=3, keywords=["FirstStrike", "IgnoreTerrain"]))
        self._add(Card(206, "Titano di Cenere", 0, CardType.ELDRAZI, Color.GRAY, 7, 4, "Distrugge la tessera su cui viene evocato convertendola in terreno neutrale.", is_eldrazi=True, sacrifice_cost=3))
        self._add(Card(207, "Distruttore di Mondi", 0, CardType.ELDRAZI, Color.GRAY, 8, 7, "Travolgere; infligge 2 danni diretti al Comandante se elimina un'unità incoronata.", is_eldrazi=True, sacrifice_cost=4, keywords=["Trample", "CommanderDamage"]))
        self._add(Card(208, "Colosso del Vuoto", 0, CardType.ELDRAZI, Color.GRAY, 7, 9, "Riduce di 1 tutti i danni subiti da qualsiasi fonte.", is_eldrazi=True, sacrifice_cost=4, keywords=["DamageReduction1"]))
        self._add(Card(209, "Annientatore Cosmico", 0, CardType.ELDRAZI, Color.GRAY, 9, 6, "Colpisce ed elimina istantaneamente qualsiasi creatura di costo inferiore a 3 Mana.", is_eldrazi=True, sacrifice_cost=4, keywords=["ExecuteLowCost"]))
        self._add(Card(210, "Leviatano dell'Eternità", 0, CardType.ELDRAZI, Color.GRAY, 10, 8, "Può attaccare due volte per turno.", is_eldrazi=True, sacrifice_cost=5, keywords=["DoubleAttack"]))
        self._add(Card(211, "Avatar del Caos Primordiale", 0, CardType.ELDRAZI, Color.GRAY, 9, 10, "Immune alle Maledizioni e alle Trappole giocate dalla mano.", is_eldrazi=True, sacrifice_cost=5, keywords=["SpellImmune"]))
        self._add(Card(212, "Mietitore di Stelle", 0, CardType.ELDRAZI, Color.GRAY, 11, 7, "All'evocazione, forza la distruzione di una creatura nemica a scelta.", is_eldrazi=True, sacrifice_cost=5))
        self._add(Card(213, "Ulamog il Divoratore Supremo", 0, CardType.ELDRAZI, Color.GRAY, 12, 12, "Invulnerabile; ogni suo attacco distrugge la tessera bersaglio rendendola inaccessibile.", is_eldrazi=True, sacrifice_cost=6, keywords=["Invulnerable", "DestroyTile"]))
        self._add(Card(214, "Kozilek la Fine dei Tempi", 0, CardType.ELDRAZI, Color.GRAY, 13, 10, "Sottrae 2 Mana al nemico a inizio turno e forza lo scarto di 1 carta avversaria.", is_eldrazi=True, sacrifice_cost=6))
        self._add(Card(215, "Emrakul l'Eterno Flagello", 0, CardType.ELDRAZI, Color.GRAY, 15, 15, "Prende il controllo del Comandante e delle unità nemiche per 1 turno intero dopo l'evocazione.", is_eldrazi=True, sacrifice_cost=6, keywords=["MindControl"]))

        print(f"[CardDatabase] Caricate {len(self.cards)} carte "
              f"({len(self.bosses)} Boss, {len(self.eldrazi)} Mostrissimi)")


# Singleton di comodo
_db: Optional[CardDatabase] = None

def get_card_db() -> CardDatabase:
    global _db
    if _db is None:
        _db = CardDatabase()
    return _db
