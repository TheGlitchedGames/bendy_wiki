"""
Comando de gestión Django para poblar la base de datos con juegos, personajes
y capítulos de Bendy and the Ink Machine (BATIM) y Bendy and the Dark Revival (BATDR).

Uso:
    python manage.py populate_bendy_data
    python manage.py populate_bendy_data --clear   # Borra los datos existentes antes de insertar
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify


# ── Datos de los juegos ───────────────────────────────────────────────────────

GAMES_DATA: list[dict] = [
    {
        "key": "batim",
        "title": "Bendy and the Ink Machine",
        "release_year": 2017,
        "slug": "bendy-and-the-ink-machine",
        "short_description": (
            "Juego de terror y aventura en primera persona ambientado en un estudio de animación "
            "de los años 60 infestado de criaturas de tinta. Protagonizado por Henry Stein, un "
            "exanimador que regresa al estudio décadas después de haberlo abandonado."
        ),
    },
    {
        "key": "batdr",
        "title": "Bendy and the Dark Revival",
        "release_year": 2022,
        "slug": "bendy-and-the-dark-revival",
        "short_description": (
            "Secuela espiritual de BATIM. Una joven llamada Audrey es arrastrada al Estudio Oscuro "
            "y debe sobrevivir a sus horrores mientras descubre la verdad sobre su propio origen "
            "y su vínculo con Joey Drew."
        ),
    },
]


# ── Datos de los personajes ───────────────────────────────────────────────────
# Campos de FK / M2M:
#   primary_game_key  → clave del juego principal  (str: "batim" | "batdr")
#   extra_game_keys   → lista de claves adicionales (list[str], puede estar vacía)
# El antiguo campo `game` con valor "both" se convierte ahora en:
#   primary_game_key = juego más representativo + extra_game_keys = [el otro]

CHARACTERS_DATA: list[dict] = [
    # ── BATIM ─────────────────────────────────────────────────────────────────
    {
        "name": "Bendy",
        "alias": "Bendy the Dancing Demon, Ink Bendy, Ink Demon, The Beast Bendy",
        "primary_game_key": "batim",
        "extra_game_keys": ["batdr"],
        "role": "antagonist",
        "character_type": "ink_monster",
        "description": (
            "Bendy es la mascota estrella de Joey Drew Studios, un personaje de dibujos "
            "animados creado a finales de los años 20 que protagonizó numerosas animaciones "
            "junto a Boris el Lobo y Alice Angel. El Demonio de Tinta (Ink Bendy) es un "
            "intento fallido de traer al Bendy de dibujos animados a la vida real usando la "
            "Máquina de Tinta, resultando en una entidad demoníaca sin alma que acecha los "
            "pasillos del estudio con una hostilidad implacable. En BATIM persigue a Henry "
            "a lo largo del juego. En BATDR adopta la forma de un Bendy más tranquilo y "
            "consciente llamado 'Buddy', que actúa como guía de Audrey."
        ),
        "appearance": (
            "Figura animada en blanco y negro estilo años 30, pequeño y rechoncho con grandes "
            "guantes blancos, pajarita y un eterno arco de sonrisa pintado. Su versión Ink Demon "
            "es una masa gigante y deforme de tinta negra con una figura vagamente humanoide, "
            "ojos blancos y un rostro que imita el del personaje animado original."
        ),
        "personality": (
            "El personaje animado original es travieso, pícaro y carismático. El Ink Demon de BATIM "
            "es una fuerza primitiva y destructiva que actúa por instinto. En BATDR, 'Buddy Bendy' "
            "muestra una personalidad más compleja, capaz de comunicarse y guiar a Audrey."
        ),
        "background": (
            "Creado por Joey Drew como mascota del estudio en los años 20, Bendy protagonizó "
            "cortos animados durante décadas. Joey Drew, obsesionado con dar vida a sus personajes, "
            "usó la Máquina de Tinta para intentar traer a Bendy a la vida. El resultado fue el "
            "Ink Demon, una entidad defectuosa sin alma que aterroriza el estudio."
        ),
        "real_world_inspiration": "Bimbo (personaje de Fleischer Studios, 1930)",
        "appears_in_chapters": "1, 2, 3, 4, 5 (BATIM) | Todos (BATDR)",
        "iconic_quote": (
            "My ink swells and boils. It consumes. I... am the Ink Demon. "
            "This realm is mine. You were born from it... you belong to it..."
        ),
        "quote_source": "Bendy and the Dark Revival",
        "is_alive_end": True,
        "is_playable": False,
        "voice_actor_batdr": "Tyler Bunch",
    },
    {
        "name": "Henry Stein",
        "alias": "Henry",
        "primary_game_key": "batim",
        "extra_game_keys": [],
        "role": "protagonist",
        "character_type": "human",
        "description": (
            "Henry Stein es el protagonista jugable de BATIM. Exanimador y cofundador de Joey Drew "
            "Studios, recibe una carta misteriosa de su antiguo socio Joey Drew pidiéndole que "
            "regrese al estudio. Al llegar descubre que el lugar está infestado de criaturas de "
            "tinta. En realidad, el Henry que controlamos es una réplica de tinta del Henry "
            "original, atrapada en un ciclo temporal sin fin por la maquinaria del estudio."
        ),
        "appearance": (
            "Hombre de mediana edad con ropa de trabajo, gorra y delantal de cuero. "
            "Su apariencia es la de un trabajador manual típico de los años 60."
        ),
        "personality": (
            "Pragmático, ingenioso y resiliente. Aunque se enfrenta a horrores constantes, "
            "mantiene la cabeza fría y usa el entorno a su favor para sobrevivir."
        ),
        "background": (
            "Henry fue el animador principal y segundo al mando de Joey Drew Studios durante "
            "30 años. Dejó el estudio en algún momento antes de los eventos del juego. "
            "Una réplica de tinta suya es introducida en el Ciclo por Joey alrededor de 1960."
        ),
        "appears_in_chapters": "1, 2, 3, 4, 5 (BATIM)",
        "iconic_quote": "On the plus side, I got a new character I think people are going to love.",
        "quote_source": "Bendy and the Ink Machine, Capítulo 1",
        "is_alive_end": None,
        "is_playable": True,
    },
    {
        "name": "Joey Drew",
        "alias": "Mr. Drew",
        "primary_game_key": "batim",
        "extra_game_keys": ["batdr"],
        "role": "antagonist",
        "character_type": "human",
        "description": (
            "Joey Drew es el fundador y director de Joey Drew Studios, el verdadero antagonista "
            "detrás de todos los horrores del juego. Su obsesión por dar vida a sus creaciones "
            "animadas lo llevó a realizar experimentos con la Máquina de Tinta usando las almas "
            "de sus propios empleados. Aparece físicamente en el Capítulo 5 de BATIM como un "
            "anciano que parece arrepentido, aunque su sinceridad es ambigua."
        ),
        "appearance": (
            "Hombre anciano en el Capítulo 5, con un bastón. En fotografías y referencias del "
            "pasado se le muestra como un hombre carismático y bien vestido."
        ),
        "personality": (
            "Soñador visionario y adicto al trabajo con un lado oscuro y obsesivo. "
            "Capaz de manipular y sacrificar a sus empleados en pos de sus ambiciones. "
            "Al final muestra señales de arrepentimiento, aunque no está claro si es genuino."
        ),
        "background": (
            "Fundó Joey Drew Studios y lo convirtió en un estudio de animación de éxito. "
            "Su creciente obsesión con la inmortalidad y con dar vida a sus personajes lo llevó "
            "a construir la Máquina de Tinta y a realizar rituales usando las almas de sus "
            "trabajadores. Es el arquitecto del Ciclo en el que están atrapados todos los personajes."
        ),
        "appears_in_chapters": "5 (BATIM, presencia física) | Mencionado en todos",
        "iconic_quote": "Henry, come visit the old workshop. There's something I need to show you.",
        "quote_source": "Carta de Joey Drew, inicio de BATIM",
        "is_alive_end": True,
        "is_playable": False,
    },
    {
        "name": "Boris the Wolf",
        "alias": "Buddy Boris, Boris",
        "primary_game_key": "batim",
        "extra_game_keys": [],
        "role": "ally",
        "character_type": "toon",
        "description": (
            "Boris es la reencarnación animada de Daniel 'Buddy' Lewek, un empleado del estudio "
            "asesinado por el Ink Bendy en 1946. Es el deuteragonista del Capítulo 3 y uno de "
            "los aliados más importantes de Henry. Su versión corrompida (Brute Boris) aparece "
            "como jefe en el Capítulo 4 tras ser capturado y modificado por Twisted Alice."
        ),
        "appearance": (
            "Lobo antropomórfico alto con overol amarillo, zapatos negros, guantes amarillos "
            "y orejas puntiagudas. Tiene mejillas negras y pecas en el hocico."
        ),
        "personality": (
            "Amable, leal y valiente. A pesar de su imponente tamaño es un personaje gentil "
            "que se convierte en el compañero fiel de Henry durante el Capítulo 3."
        ),
        "human_counterpart": "Daniel 'Buddy' Lewek",
        "real_world_inspiration": "Koko the Clown (Fleischer Studios)",
        "appears_in_chapters": "2 (muerto), 3, 4 (como Brute Boris)",
        "iconic_quote": "Good golly gosh!",
        "quote_source": "Corto animado de Bendy",
        "is_alive_end": False,
        "is_playable": False,
    },
    {
        "name": "Twisted Alice",
        "alias": "Alice Angel, Alice, Susie",
        "primary_game_key": "batim",
        "extra_game_keys": ["batdr"],
        "role": "secondary_antagonist",
        "character_type": "ink_monster",
        "description": (
            "Twisted Alice es la forma corrompida de Susie Campbell, la actriz de voz original "
            "de Alice Angel, quien fue absorbida por la Máquina de Tinta. Obsesionada con su "
            "propia belleza y perfección, captura a otros seres del estudio para robarles sus "
            "partes y volverse más 'perfecta'. En BATIM actúa como antagonista del capítulo 3 "
            "y 4. En BATDR aparece en una forma diferente y menos dominante."
        ),
        "appearance": (
            "Mitad ángel animada, mitad monstruo de tinta. La mitad derecha de su cuerpo "
            "mantiene la apariencia estilizada de Alice Angel; la izquierda es una masa deforme "
            "de tinta negra con un ojo enorme y una pierna mecánica improvisada."
        ),
        "personality": (
            "Narcisista, manipuladora y cruel. Usa una fachada de amabilidad y encanto para "
            "conseguir lo que quiere, revelando su verdadera naturaleza brutal cuando no obtiene "
            "lo que desea."
        ),
        "human_counterpart": "Susie Campbell",
        "real_world_inspiration": "Betty Boop (Fleischer Studios, 1930)",
        "appears_in_chapters": "3, 4, 5 (BATIM) | Acto 1-2 (BATDR)",
        "iconic_quote": "I am the most perfect, most beautiful angel.",
        "quote_source": "Bendy and the Ink Machine, Capítulo 3",
        "is_alive_end": False,
        "is_playable": False,
        "voice_actor_batim": "Ally Murphy",
        "voice_actor_batdr": "Ally Murphy",
    },
    {
        "name": "Sammy Lawrence",
        "alias": "The Prophet, Sammy",
        "primary_game_key": "batim",
        "extra_game_keys": [],
        "role": "secondary_antagonist",
        "character_type": "ink_monster",
        "description": (
            "Sammy Lawrence fue el director musical de Joey Drew Studios y uno de los primeros "
            "en ser corrompido por la Máquina de Tinta. Convertido en una criatura de tinta, "
            "desarrolló una devoción fanática hacia el Ink Demon Bendy, al que venera como un "
            "dios al que pretende ofrecerle a Henry como sacrificio ritual."
        ),
        "appearance": (
            "Criatura de tinta con un cuerpo humanoide envuelto en una túnica improvisada "
            "y con una máscara de cartón con la cara de Bendy que cubre su rostro deforme."
        ),
        "personality": (
            "Fanático religioso con comportamiento errático e imprevisible. Alterna entre "
            "momentos de lucidez donde recuerda su vida pasada y accesos de fervor ritual."
        ),
        "background": (
            "Compositor y director musical de talento, su alma fue una de las primeras en ser "
            "consumidas por la Máquina de Tinta. La tinta transformó su devoción artística "
            "en fanatismo religioso hacia el Ink Demon."
        ),
        "appears_in_chapters": "2, 5 (BATIM)",
        "iconic_quote": "And now, sheep without a shepherd, I shall offer you to my lord!",
        "quote_source": "Bendy and the Ink Machine, Capítulo 2",
        "is_alive_end": False,
        "is_playable": False,
        "voice_actor_batim": "Aaron Landon",
    },
    # ── BATDR ─────────────────────────────────────────────────────────────────
    {
        "name": "Audrey",
        "alias": "Audrey Drew",
        "primary_game_key": "batdr",
        "extra_game_keys": [],
        "role": "protagonist",
        "character_type": "human",
        "description": (
            "Audrey es la protagonista jugable de BATDR. Trabajadora de un estudio de animación "
            "en los años 60, es arrastrada al Estudio Oscuro: la versión corrupta e interminable "
            "del antiguo Joey Drew Studios. A lo largo de su aventura descubrirá que su conexión "
            "con la tinta y con Joey Drew va mucho más allá de lo que imaginaba: es su hija, "
            "creada a partir de la propia tinta del estudio."
        ),
        "appearance": (
            "Joven mujer con cabello oscuro y vestimenta de trabajo de los años 60. "
            "A medida que avanza el juego, gana acceso a poderes de tinta que transforman "
            "brevemente su apariencia."
        ),
        "personality": (
            "Valiente, ingeniosa y empática. Mantiene la determinación incluso ante los horrores "
            "del Estudio Oscuro, y muestra compasión hacia los seres atrapados en él."
        ),
        "background": (
            "Aparentemente una animadora ordinaria de los años 60. La verdad es que Joey Drew "
            "la creó como su obra maestra personal — una hija de tinta con libre albedrío, "
            "destinada a ser la heredera del estudio y su legado."
        ),
        "appears_in_chapters": "Todos (BATDR)",
        "iconic_quote": "I'm not afraid of you. Not anymore.",
        "quote_source": "Bendy and the Dark Revival",
        "is_alive_end": True,
        "is_playable": True,
        "voice_actor_batdr": "Jeannie Tirado",
    },
    {
        "name": "Wilson Arch",
        "alias": "Wilson",
        "primary_game_key": "batdr",
        "extra_game_keys": [],
        "role": "antagonist",
        "character_type": "human",
        "description": (
            "Wilson Arch es el antagonista principal de BATDR. Se presenta inicialmente como un "
            "aliado que quiere ayudar a Audrey a escapar del Estudio Oscuro, pero sus verdaderos "
            "motivos son usar a Audrey — la hija de tinta de Joey Drew — para apoderarse del "
            "control absoluto del estudio y sus poderes sobre la tinta."
        ),
        "appearance": (
            "Hombre de mediana edad con traje oscuro y apariencia autoritaria. "
            "Transmite una imagen de confianza y profesionalismo que oculta sus verdaderas intenciones."
        ),
        "personality": (
            "Calculador, manipulador y ambicioso. Maestro del engaño que usa la amabilidad "
            "como herramienta. Su obsesión por el poder lo convierte en un antagonista "
            "más cerebral que los monstruos del estudio."
        ),
        "background": (
            "Antiguo asociado de Joey Drew Studios que conoce los secretos de la Máquina de Tinta. "
            "Lleva años planeando cómo aprovechar el poder del Estudio Oscuro para sus propios fines."
        ),
        "appears_in_chapters": "1, 2, 3, 4 (BATDR)",
        "iconic_quote": "I just want to help you get home, Audrey. That's all.",
        "quote_source": "Bendy and the Dark Revival",
        "is_alive_end": False,
        "is_playable": False,
        "voice_actor_batdr": "David Scully",
    },
    {
        "name": "Nathan Arch",
        "alias": "Nathan",
        "primary_game_key": "batdr",
        "extra_game_keys": [],
        "role": "secondary_antagonist",
        "character_type": "ink_monster",
        "description": (
            "Nathan Arch es el hermano de Wilson, convertido en una criatura de tinta que actúa "
            "como el músculo de su hermano dentro del Estudio Oscuro. Aunque mantiene cierta "
            "conciencia, ha perdido gran parte de su humanidad tras su transformación."
        ),
        "appearance": (
            "Gran criatura de tinta con una apariencia amenazante y distorsionada. "
            "Conserva rasgos vagamente humanos que recuerdan a su forma original."
        ),
        "personality": (
            "Leal a Wilson a pesar de su transformación. Brutal y directo en comparación "
            "con la sutileza manipuladora de su hermano."
        ),
        "appears_in_chapters": "2, 3, 4 (BATDR)",
        "iconic_quote": "",
        "is_alive_end": False,
        "is_playable": False,
    },
    {
        "name": "Allison Angel",
        "alias": "Allison, The Good Alice",
        "primary_game_key": "batdr",
        "extra_game_keys": [],
        "role": "ally",
        "character_type": "toon",
        "description": (
            "Allison Angel es la versión alternativa de Alice Angel, creada a partir del alma de "
            "Allison Pendle, la segunda actriz de voz de Alice Angel. A diferencia de Twisted Alice, "
            "Allison mantiene su humanidad y actúa como guía y aliada de Audrey en el Estudio Oscuro. "
            "En BATIM aparece brevemente en el final del Capítulo 5."
        ),
        "appearance": (
            "Versión más elegante y equilibrada de Alice Angel, con el aspecto del personaje "
            "animado original sin las deformidades de Twisted Alice."
        ),
        "personality": (
            "Compasiva, valiente y determinada. Mantiene su humanidad intacta a pesar de su "
            "transformación, lo que la distingue completamente de Twisted Alice."
        ),
        "human_counterpart": "Allison Pendle",
        "real_world_inspiration": "Betty Boop (Fleischer Studios, 1930)",
        "appears_in_chapters": "5 (BATIM, final) | 1, 2, 3, 4 (BATDR)",
        "is_alive_end": True,
        "is_playable": False,
        "voice_actor_batdr": "Debi Derryberry",
    },
    {
        "name": "Tom",
        "alias": "Tom the Wolf, Good Boris",
        "primary_game_key": "batdr",
        "extra_game_keys": [],
        "role": "ally",
        "character_type": "toon",
        "description": (
            "Tom es la versión alternativa de Boris the Wolf, creada a partir del alma de Thomas "
            "Connor, el fontanero del estudio. Compañero de Allison Angel, actúa como guardián "
            "silencioso y protector en el Estudio Oscuro. Aparece brevemente en el final del "
            "Capítulo 5 de BATIM."
        ),
        "appearance": (
            "Similar al Boris original pero con un brazo mecánico improvisado fabricado "
            "con piezas del estudio, que usa como arma."
        ),
        "personality": (
            "Callado y serio, habla muy poco pero sus acciones demuestran una lealtad "
            "inquebrantable hacia Allison y los aliados de Audrey."
        ),
        "human_counterpart": "Thomas Connor",
        "appears_in_chapters": "5 (BATIM, final) | 1, 2, 3 (BATDR)",
        "is_alive_end": True,
        "is_playable": False,
    },
]


# ── Datos de los capítulos ────────────────────────────────────────────────────
# El campo `game` ahora es la clave del modelo Game (str: "batim" | "batdr")

CHAPTERS_DATA: list[dict] = [
    # ── BATIM ─────────────────────────────────────────────────────────────────
    {
        "game_key": "batim",
        "number": 1,
        "title": "Moving Pictures",
        "art_theme": "animation",
        "art_theme_explanation": (
            "El primer capítulo homenajea la animación clásica y el proceso de creación de "
            "dibujos animados de los años 30. Las máquinas de proyección, los bocetos en las "
            "paredes y los pupitres de animadores recrean el ambiente de un estudio de la era "
            "dorada de la animación americana."
        ),
        "release_date": "2017-02-10",
        "last_update_date": "2018-11-13",
        "synopsis": (
            "Henry Stein recibe una carta de su antiguo socio Joey Drew y regresa al estudio "
            "que ambos fundaron hace 30 años. El estudio está abandonado y misteriosamente "
            "infestado de tinta y criaturas. Henry activa una antigua Máquina de Tinta y "
            "descubre los horrores que se ocultan en el lugar donde trabajó durante décadas."
        ),
        "aesthetics": (
            "Estética sepia y amarillenta que evoca el papel envejecido y la tinta seca. "
            "Los pasillos estrechos y la iluminación tenue crean una atmósfera de claustrofobia "
            "y decrepitud industrial mezclada con el encanto nostálgico de los cartoons clásicos."
        ),
        "setting_description": (
            "Las plantas superiores del Joey Drew Studios: salas de animación, despachos "
            "y la sala de la Máquina de Tinta. Techos bajos, madera oscura y tinta por todas partes."
        ),
        "difficulty": "introductory",
        "has_boss_fight": False,
        "has_stealth_sections": False,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 30,
        "protagonist": "Henry Stein",
        "main_villain": "Ink Bendy (persecución)",
        "new_characters_introduced": "Henry Stein, Ink Bendy, Sammy Lawrence (audio)",
        "key_events": (
            "— Henry llega al estudio y activa la Máquina de Tinta.\n"
            "— Descubre las ofrendas de los empleados alrededor de la máquina.\n"
            "— Primera aparición del Ink Demon.\n"
            "— Henry cae a un nivel inferior del estudio."
        ),
        "lore_revelations": (
            "— Joey Drew envió cartas a todos los exempleados para que volvieran al estudio.\n"
            "— Los empleados realizaban rituales alrededor de la Máquina de Tinta.\n"
            "— Algo salió terriblemente mal con los experimentos del estudio."
        ),
        "composer": "theMeatly",
        "trivia": (
            "— Es el capítulo más corto del juego, diseñado como tutorial.\n"
            "— El primer capítulo fue lanzado de forma independiente y gratuita en 2017, "
            "antes del lanzamiento completo del juego.\n"
            "— La canción 'Build Our Machine' se convirtió en un himno de la comunidad fandom."
        ),
        "reception_notes": (
            "Recibido con entusiasmo masivo por la comunidad de YouTube y Twitch. "
            "Su estética única y el misterio de su narrativa lo convirtieron en viral "
            "prácticamente de inmediato."
        ),
    },
    {
        "game_key": "batim",
        "number": 2,
        "title": "The Old Song",
        "art_theme": "music",
        "art_theme_explanation": (
            "El segundo capítulo está dedicado a la música y al departamento musical del estudio. "
            "El protagonismo de Sammy Lawrence como director musical, los instrumentos desperdigados "
            "por las salas y las grabaciones de audio que cuentan la historia reflejan la importancia "
            "de la música en la cultura de Joey Drew Studios."
        ),
        "release_date": "2017-04-18",
        "last_update_date": "2018-11-13",
        "synopsis": (
            "Henry explora el departamento de música del estudio y se encuentra con Sammy Lawrence, "
            "el antiguo director musical convertido en una criatura de tinta fanática. Sammy intenta "
            "sacrificar a Henry al Ink Demon Bendy como ofrenda ritual. Henry logra escapar y "
            "desciende aún más profundo en el estudio."
        ),
        "difficulty": "easy",
        "has_boss_fight": True,
        "boss_name": "Sammy Lawrence",
        "has_stealth_sections": True,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 45,
        "protagonist": "Henry Stein",
        "main_villain": "Sammy Lawrence",
        "new_characters_introduced": "Sammy Lawrence (físico), Boris (muerto), Inky the Searchers",
        "key_events": (
            "— Henry descubre el santuario de Sammy Lawrence al Ink Demon.\n"
            "— Sammy captura a Henry para sacrificarlo.\n"
            "— El Ink Demon interrumpe el ritual y destruye a Sammy.\n"
            "— Henry descubre el cadáver de Boris the Wolf y decide buscar a más supervivientes."
        ),
        "lore_revelations": (
            "— Sammy Lawrence fue convertido en tinta por la Máquina de Tinta.\n"
            "— Hay una religión formada alrededor del Ink Demon dentro del estudio.\n"
            "— La Máquina de Tinta transforma a las personas en criaturas."
        ),
        "composer": "theMeatly",
        "trivia": (
            "— La mecánica de sigilo introducida en este capítulo se convirtió en una "
            "de las más comentadas de la comunidad.\n"
            "— La sala del órgano de Sammy es uno de los escenarios más icónicos de la franquicia."
        ),
    },
    {
        "game_key": "batim",
        "number": 3,
        "title": "Rise and Fall",
        "art_theme": "literature",
        "art_theme_explanation": (
            "El tercer capítulo se ambienta en el departamento de guiones y diálogos, "
            "explorando el papel de la escritura y las voces en la creación animada. "
            "Las grabaciones de las actrices de voz, los guiones y las salas de grabación "
            "son el escenario de los horrores de este capítulo."
        ),
        "release_date": "2017-09-28",
        "last_update_date": "2018-11-13",
        "synopsis": (
            "Henry encuentra a Boris the Wolf vivo y juntos exploran el departamento de "
            "literatura y voces del estudio. Allí encuentran a Twisted Alice, una criatura "
            "que mezcla la apariencia de Alice Angel con una masa deforme de tinta. Alice "
            "actúa como aliada al principio, pero pronto revela sus verdaderas intenciones."
        ),
        "difficulty": "medium",
        "has_boss_fight": False,
        "has_stealth_sections": True,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 60,
        "protagonist": "Henry Stein",
        "main_villain": "Twisted Alice",
        "new_characters_introduced": "Twisted Alice, Boris (vivo), The Butcher Gang",
        "key_events": (
            "— Henry encuentra a Boris the Wolf vivo en una habitación segura.\n"
            "— Twisted Alice contacta con Henry y lo usa para recolectar almas.\n"
            "— Alice revela que quiere las partes de Boris para 'perfeccionarse'.\n"
            "— Henry y Boris escapan temporalmente de Alice."
        ),
        "lore_revelations": (
            "— Twisted Alice es Susie Campbell, la primera actriz de voz de Alice Angel.\n"
            "— La Máquina de Tinta intentó crear versiones animadas de personas reales.\n"
            "— El proceso de creación de criaturas fue el origen de los monstruos del estudio."
        ),
        "composer": "theMeatly",
    },
    {
        "game_key": "batim",
        "number": 4,
        "title": "Colossal Wonders",
        "art_theme": "scenography",
        "art_theme_explanation": (
            "El cuarto capítulo celebra la escenografía y el diseño de producción, "
            "con enormes sets de filmación, atrezzo teatral y los bastidores de un estudio "
            "de producción cinematográfica de los años 40. Los enormes espacios contrastan "
            "con la claustrofobia de los capítulos anteriores."
        ),
        "release_date": "2018-04-30",
        "last_update_date": "2018-11-13",
        "synopsis": (
            "Henry queda atrapado en las plantas inferiores del estudio mientras Twisted Alice "
            "captura a Boris. Henry debe abrirse paso por los enormes almacenes y sets de "
            "producción del estudio para rescatarlo, pero al encontrar a Boris descubre que "
            "ha sido transformado en 'Brute Boris' por Twisted Alice, que lo usa como jefe final."
        ),
        "difficulty": "hard",
        "has_boss_fight": True,
        "boss_name": "Brute Boris",
        "has_stealth_sections": False,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 75,
        "protagonist": "Henry Stein",
        "main_villain": "Twisted Alice / Brute Boris",
        "new_characters_introduced": "Brute Boris, Bertrum Piedmont",
        "key_events": (
            "— Henry es capturado y despierta en las plantas inferiores del estudio.\n"
            "— Descubre el parque de atracciones fallido de Bertrum Piedmont.\n"
            "— Derrota al jefe Bertrum Piedmont.\n"
            "— Encuentra a Boris convertido en Brute Boris y se ve obligado a derrotarlo."
        ),
        "lore_revelations": (
            "— Joey Drew encargó un parque de atracciones de Bendy que nunca llegó a abrirse.\n"
            "— Twisted Alice puede transformar y modificar a otras criaturas de tinta.\n"
            "— El estudio tiene niveles subterráneos de gran tamaño."
        ),
        "composer": "theMeatly",
        "trivia": (
            "— La batalla contra Bertrum Piedmont es una de las más elaboradas del juego.\n"
            "— La transformación de Boris en Brute Boris fue uno de los momentos más impactantes "
            "de la saga para la comunidad fandom."
        ),
        "reception_notes": (
            "El capítulo fue elogiado por expandir el lore y la escala del mundo, "
            "aunque la muerte de Boris generó división entre los fans."
        ),
    },
    {
        "game_key": "batim",
        "number": 5,
        "title": "The Last Reel",
        "art_theme": "film",
        "art_theme_explanation": (
            "El capítulo final rinde homenaje al séptimo arte y al cine. "
            "La sala de proyección, los rollos de película, los pasillos estilo teatro y "
            "la confrontación final con Joey Drew tienen la estructura dramática de un "
            "clímax cinematográfico clásico."
        ),
        "release_date": "2018-10-26",
        "synopsis": (
            "Henry llega a las profundidades finales del estudio y se enfrenta al origen "
            "de todo: Joey Drew en persona, un anciano que parece arrepentido de sus actos. "
            "Henry descubre la verdad sobre el Ciclo, sobre su propia naturaleza como réplica "
            "de tinta, y tiene la oportunidad de romper el ciclo o perpetuarlo. La decisión "
            "final determina el destino de Henry y todos los atrapados en el estudio."
        ),
        "difficulty": "boss_heavy",
        "has_boss_fight": True,
        "boss_name": "Beast Bendy (forma final del Ink Demon)",
        "has_stealth_sections": True,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 90,
        "protagonist": "Henry Stein",
        "main_villain": "Joey Drew / Beast Bendy",
        "new_characters_introduced": "Joey Drew (físico), Allison Angel, Tom",
        "key_events": (
            "— Henry descubre la sala de proyección final de Joey Drew.\n"
            "— Joey Drew revela la verdad sobre el Ciclo y la naturaleza de Henry.\n"
            "— Batalla final contra Beast Bendy.\n"
            "— Henry rompe el Ciclo y regresa a su casa con Linda."
        ),
        "lore_revelations": (
            "— Henry es una réplica de tinta del Henry real, atrapada en el Ciclo.\n"
            "— Joey Drew creó el Ciclo para revivir sus memorias y arrepentimientos eternamente.\n"
            "— Allison y Tom son versiones alternativas de Alice Angel y Boris con almas reales.\n"
            "— El Henry real nunca entró al estudio; fue la réplica quien vivió toda la aventura."
        ),
        "composer": "theMeatly",
        "trivia": (
            "— El final del juego fue interpretado de múltiples formas por la comunidad, "
            "generando debates sobre su significado durante años.\n"
            "— La inclusión de Allison y Tom en el final preparó el terreno para BATDR."
        ),
        "reception_notes": (
            "El capítulo final recibió críticas mixtas: elogios por la escala y las revelaciones "
            "del lore, pero algunas críticas por la complejidad de la narrativa y la ambigüedad "
            "del final."
        ),
    },
    # ── BATDR ─────────────────────────────────────────────────────────────────
    {
        "game_key": "batdr",
        "number": 1,
        "title": "Into the Dark",
        "art_theme": "none",
        "release_date": "2022-10-21",
        "synopsis": (
            "Audrey, animadora de un estudio de los años 60, es arrastrada al Estudio Oscuro: "
            "una versión sobrenatural y retorcida del antiguo Joey Drew Studios. Allí conoce a "
            "Wilson Arch, quien se presenta como un aliado que quiere ayudarla a escapar. "
            "Audrey debe aprender las reglas de este mundo de tinta para sobrevivir."
        ),
        "setting_description": (
            "Los pasillos de entrada del Estudio Oscuro: una mezcla opresiva de arquitectura "
            "industrial de los años 40 corrompida por la tinta negra y elementos sobrenaturales."
        ),
        "difficulty": "introductory",
        "has_boss_fight": False,
        "has_stealth_sections": True,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 60,
        "protagonist": "Audrey",
        "main_villain": "Ink creatures (hostigadores)",
        "new_characters_introduced": "Audrey, Wilson Arch, Buddy Bendy, Allison Angel, Tom",
        "key_events": (
            "— Audrey llega al Estudio Oscuro y conoce a Wilson Arch.\n"
            "— Primera aparición de Buddy Bendy como guía ambiguo.\n"
            "— Audrey descubre que tiene una conexión especial con la tinta.\n"
            "— Establecimiento del objetivo: encontrar la salida con la ayuda de Wilson."
        ),
        "lore_revelations": (
            "— El Estudio Oscuro es una versión viva y consciente del antiguo estudio de Joey Drew.\n"
            "— La tinta obedece a ciertas personas de formas inexplicables.\n"
            "— Wilson Arch conoce los secretos del estudio mejor de lo que aparenta."
        ),
        "composer": "theMeatly & NAB",
        "trivia": (
            "— BATDR fue desarrollado por Joey Drew Studios Inc. (ahora Kindly Beast) "
            "con un equipo mucho mayor que el del juego original.\n"
            "— El cambio de protagonista a una mujer fue muy bien recibido por la comunidad."
        ),
    },
    {
        "game_key": "batdr",
        "number": 2,
        "title": "The Ink Below",
        "art_theme": "none",
        "release_date": "2022-10-21",
        "synopsis": (
            "Audrey desciende a los niveles inferiores del Estudio Oscuro, donde descubre "
            "los orígenes de los experimentos de Joey Drew y los secretos de la Máquina de Tinta "
            "original. Wilson revela más información sobre el estudio, aunque sus verdaderas "
            "intenciones empiezan a ponerse en duda."
        ),
        "setting_description": (
            "Las plantas subterráneas del estudio: laboratorios de tinta, archivos y "
            "salas de máquinas que recuerdan los niveles profundos de BATIM."
        ),
        "difficulty": "medium",
        "has_boss_fight": True,
        "boss_name": "Nathan Arch",
        "has_stealth_sections": True,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 75,
        "protagonist": "Audrey",
        "main_villain": "Wilson Arch (traición emergente) / Nathan Arch",
        "new_characters_introduced": "Nathan Arch",
        "key_events": (
            "— Audrey explora los laboratorios de la Máquina de Tinta original.\n"
            "— Encuentro y combate con Nathan Arch.\n"
            "— Allison Angel revela sus dudas sobre Wilson.\n"
            "— Audrey descubre que sus poderes de tinta son más fuertes de lo normal."
        ),
        "lore_revelations": (
            "— Los hermanos Arch conocen el funcionamiento interno de la Máquina de Tinta.\n"
            "— Joey Drew tenía planes que van más allá de simplemente dar vida a sus personajes.\n"
            "— La tinta del estudio tiene su propia voluntad y 'elige' a ciertas personas."
        ),
        "composer": "theMeatly & NAB",
        "trivia": (
            "— Este capítulo contiene numerosas referencias y easter eggs para fans de BATIM.\n"
            "— Los objetos coleccionables de este capítulo revelan detalles sobre qué pasó "
            "entre los eventos de BATIM y BATDR."
        ),
    },
    {
        "game_key": "batdr",
        "number": 3,
        "title": "The Keep",
        "art_theme": "none",
        "release_date": "2022-10-21",
        "synopsis": (
            "Audrey penetra en 'The Keep', la fortaleza central del Estudio Oscuro controlada "
            "por Wilson Arch. Aquí la verdad sobre los planes de Wilson comienza a revelarse: "
            "no quiere ayudar a Audrey a escapar, sino usarla para sus propios fines. "
            "Audrey también descubre pistas sobre su verdadera identidad y su conexión "
            "con Joey Drew."
        ),
        "setting_description": (
            "Una fortaleza de tinta y metal en el corazón del Estudio Oscuro: "
            "arquitectura opresiva que combina lo industrial con lo sobrenatural."
        ),
        "difficulty": "medium",
        "has_boss_fight": True,
        "boss_name": "Ink creature guardian (mini-jefe de The Keep)",
        "has_stealth_sections": True,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 80,
        "protagonist": "Audrey",
        "main_villain": "Wilson Arch",
        "key_events": (
            "— Infiltración en The Keep.\n"
            "— Revelaciones sobre los planes de Wilson.\n"
            "— Audrey descubre pistas sobre su origen.\n"
            "— Buddy Bendy salva a Audrey en un momento crítico."
        ),
        "lore_revelations": (
            "— Wilson quiere usar a Audrey para tomar control absoluto del Estudio Oscuro.\n"
            "— Audrey tiene una conexión con la tinta que va más allá de lo normal.\n"
            "— Joey Drew puede haber creado a Audrey deliberadamente."
        ),
        "composer": "theMeatly & NAB",
    },
    {
        "game_key": "batdr",
        "number": 4,
        "title": "The Dark City",
        "art_theme": "none",
        "release_date": "2022-10-21",
        "synopsis": (
            "Audrey llega a la Ciudad Oscura, una vasta metrópolis de tinta que replica "
            "una ciudad de los años 60 corrompida por la tinta. Aquí las revelaciones sobre "
            "su identidad se completan: Audrey es hija de Joey Drew, creada a partir de tinta "
            "como su obra maestra personal. Wilson Arch revela su verdadera naturaleza y "
            "objetivos en su confrontación final."
        ),
        "setting_description": (
            "La Ciudad Oscura: calles, edificios y plazas de una ciudad imaginaria construida "
            "enteramente de tinta negra y componentes del estudio. Es el área más grande del juego."
        ),
        "difficulty": "hard",
        "has_boss_fight": True,
        "boss_name": "Wilson Arch (confrontación final)",
        "has_stealth_sections": False,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 90,
        "protagonist": "Audrey",
        "main_villain": "Wilson Arch",
        "key_events": (
            "— Exploración de la Ciudad Oscura.\n"
            "— Revelación completa del origen de Audrey como hija de tinta de Joey Drew.\n"
            "— Confrontación final con Wilson Arch.\n"
            "— Buddy Bendy y Audrey trabajan juntos contra Wilson."
        ),
        "lore_revelations": (
            "— Audrey es una creación de tinta de Joey Drew, su 'hija' más preciada.\n"
            "— Wilson Arch quería usar a Audrey para obtener los poderes de Joey sobre la tinta.\n"
            "— El Estudio Oscuro tiene un nivel de conciencia propio."
        ),
        "composer": "theMeatly & NAB",
        "trivia": (
            "— La Ciudad Oscura es el área más grande y visualmente impresionante de cualquier "
            "juego de la franquicia.\n"
            "— La revelación de la identidad de Audrey conecta narrativamente los dos juegos "
            "de manera íntima."
        ),
        "reception_notes": (
            "El giro del origen de Audrey fue el tema más debatido del juego. "
            "Algunos fans lo consideran la mejor revelación de la franquicia; "
            "otros preferían que Audrey fuera una protagonista sin conexión directa con Joey."
        ),
    },
]


class Command(BaseCommand):
    help = "Poblar la base de datos con juegos, personajes y capítulos de BATIM y BATDR"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Eliminar todos los datos existentes antes de insertar",
        )

    def handle(self, *args, **options) -> None:
        from bendy_app.models import Character, Chapter, Game

        if options["clear"]:
            self.stdout.write(self.style.WARNING("Eliminando datos existentes..."))
            Character.objects.all().delete()
            Chapter.objects.all().delete()
            Game.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Datos eliminados."))

        # ── 1. Juegos ──────────────────────────────────────────────────────────
        self.stdout.write("Insertando juegos...")
        game_cache: dict[str, Game] = {}

        for data in GAMES_DATA:
            game, created = Game.objects.update_or_create(
                key=data["key"],
                defaults=data,
            )
            game_cache[game.key] = game
            status = "creado" if created else "actualizado"
            self.stdout.write(f"  [{status}] {game.title}")

        self.stdout.write(self.style.SUCCESS(f"Juegos: {len(game_cache)} procesados."))

        # ── 2. Personajes ──────────────────────────────────────────────────────
        self.stdout.write("Insertando personajes...")
        characters_created = 0
        characters_updated = 0

        for data in CHARACTERS_DATA:
            primary_game_key: str = data.pop("primary_game_key")
            extra_game_keys: list[str] = data.pop("extra_game_keys", [])

            primary_game: Game = game_cache[primary_game_key]
            slug: str = slugify(data["name"])

            character, created = Character.objects.update_or_create(
                slug=slug,
                defaults={**data, "slug": slug, "primary_game": primary_game},
            )

            # Asignar juegos extra (M2M)
            if extra_game_keys:
                extra_games = [game_cache[k] for k in extra_game_keys if k in game_cache]
                character.extra_games.set(extra_games)
            else:
                character.extra_games.clear()

            if created:
                characters_created += 1
            else:
                characters_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Personajes: {characters_created} creados, {characters_updated} actualizados."
            )
        )

        # ── 3. Capítulos ───────────────────────────────────────────────────────
        self.stdout.write("Insertando capítulos...")
        chapters_created = 0
        chapters_updated = 0

        for data in CHAPTERS_DATA:
            game_key: str = data.pop("game_key")
            game: Game = game_cache[game_key]
            slug: str = slugify(f"{game_key}-chapter-{data['number']}-{data['title']}")

            chapter, created = Chapter.objects.update_or_create(
                game=game,
                number=data["number"],
                defaults={**data, "slug": slug, "game": game},
            )

            if created:
                chapters_created += 1
            else:
                chapters_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Capítulos: {chapters_created} creados, {chapters_updated} actualizados."
            )
        )

        self.stdout.write(self.style.SUCCESS("\n✓ Base de datos poblada correctamente."))