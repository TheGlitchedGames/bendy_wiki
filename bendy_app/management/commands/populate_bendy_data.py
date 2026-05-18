"""
Comando de gestión Django para poblar la base de datos con personajes y capítulos
de Bendy and the Ink Machine (BATIM) y Bendy and the Dark Revival (BATDR).

Uso:
    python manage.py populate_bendy_data
    python manage.py populate_bendy_data --clear   # Borra los datos existentes antes de insertar
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify

# Ajusta estos imports a la ruta real de tus modelos
# from wiki.models import Character, Chapter


CHARACTERS_DATA: list[dict] = [
    # ── PERSONAJES DE BATIM ────────────────────────────────────────────────────
    {
        "name": "Bendy",
        "alias": "Bendy the Dancing Demon, Ink Bendy, Ink Demon, The Beast Bendy",
        "game": "both",
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
            "cortos animados durante décadas. Joey Drew obsesionado con dar vida a sus personajes, "
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
        "game": "batim",
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
        "game": "both",
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
        "human_counterpart": "",
        "appears_in_chapters": "5 (BATIM, presencia física) | Mencionado en todos",
        "iconic_quote": "Henry, come visit the old workshop. There's something I need to show you.",
        "quote_source": "Carta de Joey Drew, inicio de BATIM",
        "is_alive_end": True,
        "is_playable": False,
    },
    {
        "name": "Boris the Wolf",
        "alias": "Buddy Boris, Boris",
        "game": "batim",
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
            "y orejas puntiagudas. Tiene mejillas negras y pecas en el hocico. "
            "Es el más alto de todas las criaturas del estudio."
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
        "game": "both",
        "role": "secondary_antagonist",
        "character_type": "ink_monster",
        "description": (
            "Twisted Alice es la forma corrompida de Susie Campbell, la actriz de voz original "
            "de Alice Angel, cuya alma fue atrapada en la Máquina de Tinta por Joey Drew. "
            "Obsesionada con ser 'perfecta' y hermosa, utiliza a Henry en el Capítulo 3 para "
            "conseguir partes de otras criaturas con las que mejorar su cuerpo. Es la antagonista "
            "principal de los capítulos 3 y 4 de BATIM y reaparece en BATDR."
        ),
        "appearance": (
            "Figura humanoide con cabello negro a la altura de los hombros, cejas finas y "
            "labios negros. Lleva un vestido negro y pajarita blanca idéntica a la de Bendy. "
            "Tiene halo de ángel y cuernos cortos simultáneamente. La mitad de su cara tiene "
            "aspecto de cadáver. Lleva guantes blancos con un agujero en la palma."
        ),
        "personality": (
            "Manipuladora, cruel y vanidosa. Finge amabilidad para conseguir lo que quiere "
            "y no duda en traicionar a quienes la ayudan. Su obsesión con la perfección "
            "y la belleza es su rasgo más definitorio."
        ),
        "human_counterpart": "Susie Campbell (actriz de voz)",
        "real_world_inspiration": "Betty Boop (Fleischer Studios)",
        "voice_actor_batim": "Courtney Shaw",
        "appears_in_chapters": "3, 4 (BATIM) | BATDR (antagonista secundaria)",
        "iconic_quote": (
            "I was reborn with my perfection stolen from me. To get it back, "
            "I'll rip this rotted world apart. Angels are beautiful. Angels are beautiful."
        ),
        "quote_source": "Bendy and the Ink Machine, Capítulo 3",
        "is_alive_end": False,
        "is_playable": False,
    },
    {
        "name": "Allison Angel",
        "alias": "Allison Pendle, The Good Alice",
        "game": "batim",
        "role": "ally",
        "character_type": "toon",
        "description": (
            "Allison Angel es la forma bondadosa de Alice Angel, basada en el alma de Allison "
            "Pendle, la segunda actriz de voz de Alice Angel. A diferencia de Twisted Alice, "
            "Allison conserva su humanidad y empatía. Aparece al final del Capítulo 4 como "
            "aliada de Henry junto a Tom. Cree que Henry es 'la esperanza' que el estudio "
            "estaba esperando."
        ),
        "appearance": (
            "Idéntica en forma a Twisted Alice pero con la cara perfectamente simétrica "
            "y sin el aspecto de cadáver. Irradia una presencia más amable y calmada."
        ),
        "personality": (
            "Valiente, empática y leal. Actúa como líder del dúo que forma con Tom. "
            "Confía en Henry cuando Tom desconfía de él. Puede mostrarse reacia ante "
            "situaciones de alto riesgo pero siempre actúa cuando es necesario."
        ),
        "human_counterpart": "Allison Pendle (segunda actriz de voz de Alice Angel)",
        "voice_actor_batim": "Ally Murphy",
        "appears_in_chapters": "4 (aparición), 5 (BATIM)",
        "iconic_quote": (
            "You're here for a reason Henry, there's always a reason! "
            "Even when you can't understand it. It's time, set us free!"
        ),
        "quote_source": "Bendy and the Ink Machine, Capítulo 5",
        "is_alive_end": True,
        "is_playable": False,
    },
    {
        "name": "Tom",
        "alias": "Tom Boris, Thomas Connor",
        "game": "batim",
        "role": "ally",
        "character_type": "toon",
        "description": (
            "Tom es la contraparte alternativa de Boris el Lobo, basado en el alma de Thomas "
            "Connor, un técnico del estudio. Aparece al final del Capítulo 4 junto a Allison. "
            "Desconfía profundamente de Henry en el Capítulo 5, pero acaba reconociendo su valor "
            "al ver cómo lucha. Es más agresivo y protector que Boris, y parece funcionar mejor "
            "con extraños en BATDR que en BATIM."
        ),
        "appearance": (
            "Casi idéntico a Boris pero con cejas más inclinadas y un brazo mecánico izquierdo "
            "que sustituye su antebrazo natural, construido con piezas de un animatrónico de Bendy. "
            "Lleva un cinturón en el torso. Sus ojos están más juntos que los de Boris."
        ),
        "personality": (
            "Silencioso, brusco y cauteloso. Enormemente protector con Allison. "
            "Desconfía de los desconocidos hasta que se lo ganan con acciones, no palabras."
        ),
        "human_counterpart": "Thomas Connor (técnico de mantenimiento del estudio)",
        "appears_in_chapters": "4 (aparición), 5 (BATIM)",
        "iconic_quote": (
            "I keep telling these people, if Mister Joey Drew keeps cutting corners like this, "
            "someone's sure to end up falling to their death. And it sure ain't gonna be me."
        ),
        "quote_source": "Grabación de Thomas Connor, BATIM",
        "is_alive_end": True,
        "is_playable": False,
    },
    {
        "name": "Sammy Lawrence",
        "alias": "Sammy, El Profeta de la Tinta",
        "game": "batim",
        "role": "secondary_antagonist",
        "character_type": "ink_monster",
        "description": (
            "Sammy Lawrence era el director musical de Joey Drew Studios, responsable de componer "
            "las bandas sonoras de las animaciones. Tras ser absorbido por la tinta, se convirtió "
            "en una criatura que venera a Ink Bendy como un dios, creyendo que si le ofrece un "
            "sacrificio, Bendy le liberará de su cuerpo de tinta. Captura a Henry en el Capítulo 2 "
            "para ofrecerlo como sacrificio. Reaparece en el Capítulo 5 sobreviviendo al ataque "
            "de Bendy, y muere a manos de Tom."
        ),
        "appearance": (
            "Criatura humanoide cubierta de tinta negra, sin rasgos faciales definidos. "
            "Lleva una máscara blanca con el rostro de Bendy. Viste los restos de un traje "
            "formal de director musical."
        ),
        "personality": (
            "Fanático y obsesivo en su devoción hacia Bendy. Alterna entre momentos de "
            "lucidez (donde reconoce su situación) y episodios de fervor religioso irracional."
        ),
        "human_counterpart": "Sammy Lawrence (director musical)",
        "appears_in_chapters": "2 (antagonista principal), 5 (reaparición, BATIM)",
        "iconic_quote": "Sheep, sheep, sheep. It's time for sleep. Rest your head. Now count those sheep.",
        "quote_source": "Bendy and the Ink Machine, Capítulo 2",
        "is_alive_end": False,
        "is_playable": False,
    },
    {
        "name": "The Butcher Gang",
        "alias": "Charley, Barley, Edgar",
        "game": "batim",
        "role": "antagonist",
        "character_type": "ink_monster",
        "description": (
            "The Butcher Gang es un trío de personajes animados secundarios que aparecen como "
            "enemigos recurrentes en los Capítulos 3 y 4. Son versiones corrompidas de los "
            "personajes de los cortos animados: Charley (el líder avaro), Barley (el pirata "
            "malhumorado) y Edgar (el pequeño infantil con un pato de juguete). Sus formas de "
            "tinta son deformes y agresivas."
        ),
        "appearance": (
            "Charley: figura esquelética con sombrero de copa deformado. "
            "Barley: pirata robusto con parche en el ojo. "
            "Edgar: pequeña criatura con patas de araña y cuerpo redondo."
        ),
        "personality": (
            "En los cortos originales: Charley es avaro y sin paciencia, Barley es serio y "
            "fuma en pipa, Edgar es adorable pero torpe. En sus formas de tinta actúan "
            "exclusivamente por agresión."
        ),
        "appears_in_chapters": "3, 4 (BATIM)",
        "iconic_quote": (
            "The disgusting wretches have wandered my halls, have gone unchecked! "
            "They're trying to drag me back to the darkness! Don't let them take your angel"
        ),
        "quote_source": "Twisted Alice refiriéndose a The Butcher Gang, BATIM Cap. 3",
        "is_alive_end": False,
        "is_playable": False,
    },
    {
        "name": "The Projectionist",
        "alias": "Norman Polk, El Proyeccionista",
        "game": "batim",
        "role": "antagonist",
        "character_type": "ink_monster",
        "description": (
            "El Proyeccionista es la versión corrompida de Norman Polk, el proyeccionista del "
            "estudio, absorbido por la tinta con un proyector de película fusionado en su cabeza. "
            "Patrulla las áreas oscuras del estudio proyectando luz, lo que lo convierte en un "
            "peligro único: su cono de luz detecta a Henry. Es asesinado por Ink Bendy en el "
            "Capítulo 4 en una de las escenas más impactantes del juego."
        ),
        "appearance": (
            "Criatura humanoide alta cubierta completamente de tinta negra con un proyector de "
            "película como cabeza. Largos cables negros cuelgan de su espalda. Viste restos de "
            "ropa de trabajo con mangas enrolladas y botas grandes. Tiene un altavoz en el pecho."
        ),
        "personality": (
            "No muestra personalidad propia en su forma monstruosa, actuando por instinto "
            "de patrulla. Las grabaciones de Norman Polk muestran que era un trabajador "
            "práctico y directo que advertía de los peligros del estudio."
        ),
        "human_counterpart": "Norman Polk (proyeccionista del estudio)",
        "appears_in_chapters": "3 (primero mencionado), 4 (antagonista, BATIM)",
        "iconic_quote": "It's just the nature of us projectionists to seek out the dark places.",
        "quote_source": "Grabación de Norman Polk, BATIM",
        "is_alive_end": False,
        "is_playable": False,
    },

    # ── PERSONAJES DE BATDR ────────────────────────────────────────────────────
    {
        "name": "Audrey",
        "alias": "Audrey Drew",
        "game": "batdr",
        "role": "protagonist",
        "character_type": "human",
        "description": (
            "Audrey es la protagonista jugable de Bendy and the Dark Revival. Empleada de "
            "Joey Drew Studios en su nueva encarnación corporativa, Audrey es arrastrada "
            "al Estudio Oscuro (Dark Studio) y debe escapar. A lo largo del juego descubre "
            "una conexión personal profunda con Joey Drew y con los orígenes de la Máquina "
            "de Tinta. Es hija biológica de Joey Drew, creada a partir de tinta."
        ),
        "appearance": (
            "Mujer joven con cabello oscuro corto y ropa de trabajo de los años 60. "
            "A medida que avanza la historia, su apariencia muestra señales de su "
            "verdadera naturaleza como criatura de tinta."
        ),
        "personality": (
            "Decidida, sarcástica y resiliente. Más activa y combativa que Henry, "
            "ya que puede atacar directamente a los enemigos. Mantiene su sentido del "
            "humor incluso en situaciones desesperadas."
        ),
        "appears_in_chapters": "Todos (BATDR)",
        "iconic_quote": "I'm done being someone's puppet.",
        "quote_source": "Bendy and the Dark Revival",
        "is_alive_end": True,
        "is_playable": True,
        "voice_actor_batdr": "Ally Murphy",
    },
    {
        "name": "Wilson Arch",
        "alias": "Wilson, El Profeta",
        "game": "batdr",
        "role": "antagonist",
        "character_type": "human",
        "description": (
            "Wilson Arch es el antagonista principal de Bendy and the Dark Revival. "
            "Antiguo empleado del estudio con poderes sobre la tinta, Wilson ha desarrollado "
            "una filosofía de control absoluto sobre el Estudio Oscuro. Cree que puede "
            "dominar el caos de la tinta y convertirse en su amo. Su relación con Audrey "
            "es compleja: la guía, la manipula y finalmente se convierte en su mayor amenaza."
        ),
        "appearance": (
            "Hombre de mediana edad con traje formal y una varita de madera que usa "
            "para canalizar sus poderes sobre la tinta. Su apariencia es la de un "
            "ejecutivo elegante que oculta algo siniestro."
        ),
        "personality": (
            "Carismático y autoritario. Habla con la seguridad de alguien que cree "
            "tener todas las respuestas. Su obsesión con el control lo corrompe "
            "progresivamente a lo largo del juego."
        ),
        "appears_in_chapters": "Todos (BATDR, como figura de fondo y antagonista final)",
        "iconic_quote": "Ink doesn't lie. Ink reveals what you truly are.",
        "quote_source": "Bendy and the Dark Revival",
        "is_alive_end": False,
        "is_playable": False,
        "voice_actor_batdr": "Todd Haberkorn",
    },
    {
        "name": "Gent Porter",
        "alias": "Porter",
        "game": "batdr",
        "role": "neutral",
        "character_type": "toon",
        "description": (
            "Los Gent Porters son robots de servicio con cabeza de Bendy que pueblan el "
            "Estudio Oscuro. Actúan como empleados corporativos de la nueva Gent Corporation, "
            "realizando tareas de transporte y servicio. Algunos son hostiles, otros pueden "
            "ser ignorados. Representan la corporatización del legado de Joey Drew."
        ),
        "appearance": (
            "Robots con cuerpo mecánico y una cabeza que imita la del personaje Bendy. "
            "Visten uniformes de empleado de la corporación Gent."
        ),
        "personality": (
            "Autómatas programados, sin personalidad propia. Los hostiles atacan "
            "a cualquier intruso. Los de servicio continúan sus rutinas independientemente "
            "de lo que ocurra a su alrededor."
        ),
        "appears_in_chapters": "Todos (BATDR)",
        "is_alive_end": None,
        "is_playable": False,
    },
    {
        "name": "Charley (BATDR)",
        "alias": "Charley, Ink Charley",
        "game": "batdr",
        "role": "antagonist",
        "character_type": "ink_monster",
        "description": (
            "Versión remasterizada de Charley de The Butcher Gang, ahora con un rol más "
            "prominente en BATDR. Actúa como mini-jefe y enemigo recurrente, con una "
            "inteligencia mayor que su versión de BATIM. Su diseño ha sido actualizado "
            "para resultar más amenazante."
        ),
        "appears_in_chapters": "Varios (BATDR)",
        "is_alive_end": False,
        "is_playable": False,
    },
    {
        "name": "Ink Bendy (BATDR)",
        "alias": "Buddy Bendy, Buddy",
        "game": "batdr",
        "role": "ally",
        "character_type": "hybrid",
        "description": (
            "En BATDR, el Ink Demon ha evolucionado hacia una entidad más consciente llamada "
            "'Buddy Bendy' o simplemente 'Buddy'. Actúa como guía ambiguo de Audrey, "
            "apareciendo en momentos clave para ayudarla o advertirla. Su relación con Audrey "
            "es central para la narrativa: parecen compartir un vínculo especial relacionado "
            "con la tinta y con el legado de Joey Drew."
        ),
        "appears_in_chapters": "Varios (BATDR, guía)",
        "iconic_quote": "My ink swells and boils. It consumes. I... am the Ink Demon.",
        "quote_source": "Bendy and the Dark Revival",
        "is_alive_end": True,
        "is_playable": False,
        "voice_actor_batdr": "Tyler Bunch",
    },
]

CHAPTERS_DATA: list[dict] = [
    # ── CAPÍTULOS DE BATIM ─────────────────────────────────────────────────────
    {
        "game": "batim",
        "number": 1,
        "title": "Moving Pictures",
        "art_theme": "animation",
        "art_theme_explanation": (
            "El primer capítulo hace referencia al arte de la animación y el dibujo, "
            "que es la base del estudio. Todo el entorno está diseñado como un taller de "
            "animación de los años 30, con mesas de dibujo, carteles y la icónica Máquina "
            "de Tinta como elemento central."
        ),
        "release_date": "2017-02-10",
        "synopsis": (
            "Henry regresa al estudio de animación de su viejo amigo Joey Drew tras recibir "
            "una carta misteriosa. Al llegar, encuentra el lugar abandonado e infestado de "
            "criaturas de tinta. Descubre la Máquina de Tinta y, al intentar activarla, "
            "desencadena la aparición del Ink Bendy. El suelo cede bajo sus pies y Henry "
            "cae inconsciente tras sufrir tres alucinaciones inquietantes."
        ),
        "aesthetics": (
            "Ambiente lúgubre y abandonado con iluminación tenue y amarillenta. El juego "
            "comenzó con paleta blanco y negro, pero en la actualización del Capítulo 4 "
            "el blanco fue reemplazado por tonos amarillos cálidos para evocar el cine "
            "antiguo. Los jumpscares con recortes de cartón de Bendy y la escena con "
            "el cuerpo de Boris establecen el tono de horror corporal del juego."
        ),
        "setting_description": (
            "Las plantas superiores de Joey Drew Studios: pasillos de madera, oficinas "
            "con mesas de animación, la sala de la Máquina de Tinta y los almacenes "
            "superiores del edificio."
        ),
        "difficulty": "introductory",
        "has_boss_fight": False,
        "has_stealth_sections": False,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 45,
        "protagonist": "Henry Stein",
        "main_villain": "Ink Bendy (primera aparición)",
        "new_characters_introduced": "Henry Stein, Joey Drew (carta), Boris (muerto), Ink Bendy",
        "key_events": (
            "— Llegada de Henry al estudio abandonado.\n"
            "— Descubrimiento y activación de la Máquina de Tinta.\n"
            "— Primera aparición del Ink Bendy.\n"
            "— Caída de Henry al nivel inferior."
        ),
        "lore_revelations": (
            "— El estudio de animación está infestado de tinta viva.\n"
            "— Existe un ritual con velas y figuras de Bendy.\n"
            "— El cuerpo de Boris en la sala de disección sugiere experimentos horribles.\n"
            "— La Máquina de Tinta requiere 'sacrificios' para funcionar."
        ),
        "soundtrack_notes": (
            "Melodía minimalista de cuatro notas que se repite, creando tensión sin resolución. "
            "El tema principal establece el leitmotiv del juego completo."
        ),
        "trivia": (
            "— Este fue el capítulo lanzado originalmente como demo en febrero de 2017, "
            "generando una enorme expectación viral.\n"
            "— El juego fue creado inicialmente por theMeatly solo, sin equipo.\n"
            "— El diseño está inspirado en Fleischer Studios, rival de Disney en los años 30.\n"
            "— Bendy está basado en Bimbo de Fleischer; Boris en Koko the Clown; Alice en Betty Boop."
        ),
        "reception_notes": (
            "El capítulo se volvió viral en YouTube gracias a creadores de contenido como Markiplier "
            "y Jacksepticeye. Su estética única y su atmósfera de horror retro lo convirtieron "
            "en un fenómeno de internet casi inmediatamente después de su lanzamiento."
        ),
    },
    {
        "game": "batim",
        "number": 2,
        "title": "The Old Song",
        "art_theme": "music",
        "art_theme_explanation": (
            "El segundo capítulo está dedicado a la música como forma de arte. "
            "El departamento de grabación musical del estudio es el escenario principal, "
            "y las grabaciones de audio de Sammy Lawrence articulan tanto la narrativa "
            "como el papel de la música en la cultura del estudio."
        ),
        "release_date": "2017-04-18",
        "synopsis": (
            "Henry despierta en el nivel inferior del estudio y busca una salida a través "
            "del departamento de música. Encuentra grabaciones de Sammy Lawrence que revelan "
            "su devoción enfermiza por Bendy. Sammy captura a Henry para ofrecerlo como "
            "sacrificio a Bendy, creyendo que así será liberado de su cuerpo de tinta. "
            "Bendy aparece pero mata a Sammy en lugar de liberarlo. Henry escapa y encuentra "
            "a un Boris vivo al final del capítulo."
        ),
        "aesthetics": (
            "La música es protagonista tanto diegética como extradiegéticamente. "
            "La melodía minimalista del juego alcanza su máxima expresión en este capítulo. "
            "El departamento musical tiene un ambiente de iglesia corrompida gracias a "
            "las decoraciones de Sammy, que ha convertido el lugar en un templo a Bendy."
        ),
        "setting_description": (
            "Departamento de música del estudio: salas de grabación, cabinas de control, "
            "almacenes de instrumentos y el santuario personal de Sammy Lawrence."
        ),
        "difficulty": "easy",
        "has_boss_fight": False,
        "has_stealth_sections": True,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 60,
        "protagonist": "Henry Stein",
        "main_villain": "Sammy Lawrence",
        "new_characters_introduced": "Sammy Lawrence (antagonista), Boris (vivo, final)",
        "key_events": (
            "— Exploración del departamento de música.\n"
            "— Captura de Henry por Sammy Lawrence.\n"
            "— Ritual de sacrificio interrumpido por el propio Bendy.\n"
            "— Bendy mata a Sammy (aparentemente).\n"
            "— Henry encuentra a Boris vivo al final."
        ),
        "lore_revelations": (
            "— Sammy Lawrence y otros empleados fueron absorbidos por la tinta.\n"
            "— Sammy venera a Bendy como una deidad.\n"
            "— La tinta puede 'poseer' a las personas y alterar su psique.\n"
            "— Existen supervivientes humanos en el estudio."
        ),
        "soundtrack_notes": (
            "El capítulo explora con más profundidad la banda sonora. Las grabaciones de "
            "Sammy incluyen fragmentos de las melodías originales del estudio, dando contexto "
            "a la cultura musical que existía antes del desastre."
        ),
        "trivia": (
            "— Sammy se convirtió rápidamente en el personaje favorito del fandom por su "
            "fanatismo exagerado hacia Bendy ('SHEEP SHEEP SHEEP').\n"
            "— El capítulo introdujo las secciones de sigilo, una novedad mecánica para el juego.\n"
            "— Boris sobreviviente fue la mayor sorpresa del capítulo."
        ),
        "reception_notes": (
            "Muy bien recibido por la comunidad. La escena del ritual de Sammy se convirtió "
            "en un meme popular. El personaje de Sammy generó una cantidad enorme de fan art."
        ),
    },
    {
        "game": "batim",
        "number": 3,
        "title": "Rise and Fall",
        "art_theme": "literature",
        "art_theme_explanation": (
            "El tercer capítulo está dedicado a la literatura y al arte de la voz y los "
            "diálogos. El departamento de grabación de voz es el escenario, y la narrativa "
            "se articula principalmente a través de diálogos con Twisted Alice y grabaciones "
            "que cuentan historias en primera persona."
        ),
        "release_date": "2017-09-14",
        "synopsis": (
            "Henry despierta en la 'Casa Segura', donde Boris lo llevó tras los eventos del "
            "capítulo anterior. Ambos exploran el estudio buscando una salida. Conocen a "
            "Twisted Alice, que se presenta como aliada a cambio de ayuda con varios recados. "
            "Tras completarlos, Alice traiciona a Henry y manipula el ascensor para matarlo "
            "mientras rapta a Boris para modificarlo en su búsqueda de 'perfección'."
        ),
        "aesthetics": (
            "Los diálogos de Alice dominan el capítulo, con una narración que alterna entre "
            "amenaza y manipulación. Las grabaciones de Susie Campbell revelan su historia "
            "de una manera desgarradora. El entorno de producción de voz tiene una estética "
            "de teatro abandonado."
        ),
        "setting_description": (
            "La Casa Segura de Boris, los pasillos del departamento de producción de voz, "
            "salas de grabación y el sistema de ascensores del edificio."
        ),
        "difficulty": "medium",
        "has_boss_fight": False,
        "has_stealth_sections": True,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 90,
        "protagonist": "Henry Stein",
        "main_villain": "Twisted Alice",
        "new_characters_introduced": (
            "Twisted Alice, The Butcher Gang (Charley, Barley, Edgar), The Projectionist (mencionado)"
        ),
        "key_events": (
            "— Henry y Boris exploran juntos el estudio.\n"
            "— Primera aparición y presentación de Twisted Alice.\n"
            "— Recados para Alice: búsqueda de partes y componentes.\n"
            "— Traición de Alice: ascensor saboteado.\n"
            "— Rapto de Boris por parte de Alice."
        ),
        "lore_revelations": (
            "— Twisted Alice es Susie Campbell, la primera actriz de voz de Alice Angel.\n"
            "— Joey Drew mató a Susie para usar su alma en la Máquina de Tinta.\n"
            "— Hay una sala secreta con una grabación del propio Henry.\n"
            "— La Máquina de Tinta puede usar almas para crear criaturas específicas."
        ),
        "soundtrack_notes": (
            "La voz de Twisted Alice actúa como instrumento musical en sí misma, "
            "con un timbre que oscila entre lo angelical y lo amenazante."
        ),
        "trivia": (
            "— Este capítulo es el más largo de BATIM hasta BATDR.\n"
            "— La relación Henry-Boris fue muy celebrada por el fandom.\n"
            "— The Butcher Gang aparece aquí por primera vez como enemigos activos."
        ),
        "reception_notes": (
            "Considerado por muchos fans como el mejor capítulo de BATIM por su equilibrio "
            "entre narrativa, exploración y mecánicas de juego."
        ),
    },
    {
        "game": "batim",
        "number": 4,
        "title": "Colossal Wonders",
        "art_theme": "scenography",
        "art_theme_explanation": (
            "El cuarto capítulo está dedicado a la escenografía y el diseño de producción, "
            "escenificado en el parque temático abandonado dentro del estudio, que representa "
            "el esfuerzo máximo de diseño de escenarios de Joey Drew Studios."
        ),
        "release_date": "2018-04-30",
        "last_update_date": "2018-04-30",
        "synopsis": (
            "Henry sobrevive al accidente del ascensor y llega a un parque de atracciones "
            "abandonado dentro del estudio. Allí se enfrenta al jefe del parque (una cabeza "
            "gigante en un tiovivo), evita a The Butcher Gang y escapa del Proyeccionista, "
            "que es asesinado por Bendy en un impactante momento. Al llegar al laboratorio "
            "de Alice, descubre que Boris ha sido convertido en una abominación (Brute Boris). "
            "Tras derrotarlo, Alice enfurecida ataca a Henry, pero es asesinada por Allison "
            "Angel y Tom."
        ),
        "aesthetics": (
            "Este capítulo fue el que introdujo la remasterización visual del juego: la "
            "paleta cambió de blanco y negro/amarillo claro a los tonos amarillos cálidos "
            "más pronunciados que se convirtieron en el estilo definitivo. El parque de "
            "atracciones añade una capa de ironía oscura al horror."
        ),
        "setting_description": (
            "Parque de atracciones abandonado dentro del estudio, laboratorios subterráneos "
            "de Twisted Alice y los pasillos que los conectan."
        ),
        "difficulty": "hard",
        "has_boss_fight": True,
        "boss_name": "Brute Boris (Boris corrompido por Twisted Alice)",
        "has_stealth_sections": True,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 75,
        "protagonist": "Henry Stein",
        "main_villain": "Twisted Alice",
        "new_characters_introduced": "Allison Angel, Tom, Brute Boris (jefe)",
        "key_events": (
            "— Exploración del parque de atracciones.\n"
            "— El Proyeccionista es asesinado por Ink Bendy.\n"
            "— Boss fight contra Brute Boris.\n"
            "— Muerte de Twisted Alice a manos de Allison y Tom.\n"
            "— Primera aparición de Allison Angel y Tom."
        ),
        "lore_revelations": (
            "— Alice puede modificar criaturas de tinta para crear monstruos más poderosos.\n"
            "— Existen otras versiones de los personajes animados (Allison vs. Alice).\n"
            "— Ink Bendy tiene control territorial sobre el estudio y ataca incluso a otras criaturas.\n"
            "— El parque temático revela el alcance de los sueños de Joey Drew."
        ),
        "trivia": (
            "— La muerte del Proyeccionista a manos de Bendy es considerada uno de los "
            "momentos más espectaculares del juego.\n"
            "— La remasterización visual de este capítulo fue retroactivamente aplicada "
            "a los capítulos anteriores.\n"
            "— Brute Boris generó mucha controversia por lo que le ocurrió al querido Boris."
        ),
        "reception_notes": (
            "Recibido con entusiasmo por la espectacularidad de sus momentos, aunque algunos "
            "fans lamentaron el destino de Boris. La introducción de Allison y Tom fue "
            "muy bien recibida."
        ),
    },
    {
        "game": "batim",
        "number": 5,
        "title": "The Last Reel",
        "art_theme": "film",
        "art_theme_explanation": (
            "El capítulo final está dedicado al séptimo arte: el cine y la proyección "
            "cinematográfica. El rollo de película 'THE END' es el MacGuffin del capítulo, "
            "y la resolución del juego es literalmente proyectar una película para acabar "
            "con Bendy. El ciclo narrativo del juego es también una referencia a los bucles "
            "de bobina del cine primitivo."
        ),
        "release_date": "2018-11-07",
        "synopsis": (
            "Henry está encarcelado en la casa de Allison y Tom. Escapan cuando Bendy ataca. "
            "Henry se reencuentra brevemente con Sammy (que sobrevivió), quien es asesinado "
            "por Tom. El grupo llega a la Ciudad de Tinta. Henry cae al despacho de Joey y "
            "descubre el rollo 'THE END'. Finalmente llegan a la Máquina de Tinta convertida "
            "en palacio. Henry proyecta el rollo, Bendy se transforma en una bestia, es "
            "derrotado y la historia se revela como un bucle eterno. Joey explica todo en "
            "una escena final con Henry, y el juego reinicia."
        ),
        "aesthetics": (
            "El capítulo final integra los cuatro temas artísticos anteriores. Las animaciones "
            "transitan entre lo terrorífico (transformación de Bendy en bestia) y lo íntimo "
            "(conversación final con Joey). El bucle temporal recuerda al mito de Sísifo: "
            "Henry empuja su piedra eternamente."
        ),
        "setting_description": (
            "La casa de Allison y Tom, la Ciudad de Tinta, el despacho de Joey Drew, "
            "el palacio de la Máquina de Tinta y, finalmente, la casa de Joey en el mundo real."
        ),
        "difficulty": "boss_heavy",
        "has_boss_fight": True,
        "boss_name": "Beast Bendy (forma final del Ink Demon)",
        "has_stealth_sections": True,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 120,
        "protagonist": "Henry Stein",
        "main_villain": "Ink Bendy / Beast Bendy",
        "new_characters_introduced": "Beast Bendy (forma final)",
        "key_events": (
            "— Fuga de la casa de Allison y Tom.\n"
            "— Reencuentro y muerte de Sammy Lawrence.\n"
            "— Descubrimiento del rollo 'THE END' en el despacho de Joey.\n"
            "— Boss fight contra Beast Bendy.\n"
            "— Proyección del rollo y derrota de Bendy.\n"
            "— Conversación final con Joey Drew.\n"
            "— Reinicio del ciclo: Henry vuelve al inicio del juego."
        ),
        "lore_revelations": (
            "— La historia entera es un bucle temporal que se repite indefinidamente.\n"
            "— Los mensajes ocultos que solo se ven con el espejo son escritos por Henry.\n"
            "— Joey Drew sabe lo que ha hecho y muestra arrepentimiento.\n"
            "— La escena postcréditos sugiere que todo puede haber sido una historia que Joey "
            "le cuenta a su sobrina, o un final feliz alternativo.\n"
            "— El rollo 'THE END' es el único objeto capaz de destruir a Bendy definitivamente."
        ),
        "soundtrack_notes": (
            "La banda sonora alcanza su climax con el enfrentamiento contra Beast Bendy, "
            "usando temas de capítulos anteriores en versiones más intensas. "
            "La escena final con Joey usa una melodía más suave y melancólica."
        ),
        "trivia": (
            "— El final en bucle generó enorme debate en la comunidad sobre su significado.\n"
            "— La escena postcréditos tiene dos interpretaciones completamente válidas.\n"
            "— Beast Bendy es significativamente más grande e intimidante que el Ink Demon estándar.\n"
            "— El despacho de Joey es una de las salas más ricamente decoradas del juego."
        ),
        "reception_notes": (
            "El final fue polémico: muchos fans esperaban una resolución más definitiva. "
            "Sin embargo, la comunidad acabó apreciando la profundidad filosófica del bucle "
            "y sus paralelismos con el mito de Sísifo y la alienación laboral marxista."
        ),
    },

    # ── CAPÍTULOS DE BATDR ─────────────────────────────────────────────────────
    {
        "game": "batdr",
        "number": 1,
        "title": "Into the Ink",
        "art_theme": "none",
        "release_date": "2022-10-21",
        "synopsis": (
            "Audrey, empleada de la nueva Joey Drew Studios (ahora una corporación llamada "
            "Gent), es arrastrada al Estudio Oscuro a través de un misterioso portal de tinta. "
            "Despierta en una versión distorsionada y más vasta del estudio original y debe "
            "orientarse en este nuevo mundo, encontrando los primeros Gent Porters y "
            "descubriendo las reglas de este nuevo entorno."
        ),
        "aesthetics": (
            "BATDR actualiza la estética a un motor más moderno manteniendo la paleta amarilla "
            "y negra. El Estudio Oscuro es más grande, más laberíntico y más opresivo que el "
            "estudio original de BATIM. La iluminación volumétrica y los efectos de tinta "
            "son significativamente más elaborados."
        ),
        "setting_description": (
            "La entrada al Estudio Oscuro: pasillos corporativos distorsionados que mezclan "
            "la estética de los años 60 con elementos sobrenaturales de tinta."
        ),
        "difficulty": "introductory",
        "has_boss_fight": False,
        "has_stealth_sections": False,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 50,
        "protagonist": "Audrey",
        "main_villain": "Wilson Arch (trasfondo)",
        "new_characters_introduced": "Audrey, Gent Porters, Buddy Bendy (primera aparición como guía)",
        "key_events": (
            "— Audrey es absorbida por el portal de tinta.\n"
            "— Exploración inicial del Estudio Oscuro.\n"
            "— Primer encuentro con los Gent Porters.\n"
            "— Primera visión de Buddy Bendy."
        ),
        "lore_revelations": (
            "— La nueva corporación Gent ha industrializado la tecnología de la Máquina de Tinta.\n"
            "— El Estudio Oscuro es una dimensión propia, no el estudio físico de BATIM.\n"
            "— Buddy Bendy parece querer ayudar a Audrey."
        ),
        "composer": "theMeatly & NAB",
        "trivia": (
            "— BATDR fue desarrollado por Joey Drew Studios Inc. (el estudio real, no el ficticio) "
            "y publicado por Rooster Teeth Games.\n"
            "— El juego usa Unreal Engine en lugar del motor propietario de BATIM.\n"
            "— Audrey puede atacar directamente a los enemigos, a diferencia de Henry."
        ),
        "reception_notes": (
            "Lanzado en octubre de 2022, fue bien recibido por los fans del original aunque "
            "algunos señalaron que la transición a un estudio más grande perdía parte de la "
            "claustrofobia del original."
        ),
    },
    {
        "game": "batdr",
        "number": 2,
        "title": "The Old Studio",
        "art_theme": "none",
        "release_date": "2022-10-21",
        "synopsis": (
            "Audrey llega a una sección del Estudio Oscuro que replica el estudio original "
            "de Joey Drew tal como era en los años 60. Descubre grabaciones y registros que "
            "le cuentan la historia del estudio desde una perspectiva diferente a la de Henry. "
            "Wilson Arch comienza a contactar con ella, presentándose como alguien que puede "
            "ayudarla a escapar."
        ),
        "setting_description": (
            "Réplica distorsionada del estudio original de BATIM: las mismas salas pero "
            "más corrompidas por la tinta y el tiempo."
        ),
        "difficulty": "easy",
        "has_boss_fight": False,
        "has_stealth_sections": True,
        "has_puzzle_sections": True,
        "approximate_duration_minutes": 60,
        "protagonist": "Audrey",
        "main_villain": "Wilson Arch (manipulador)",
        "new_characters_introduced": "Wilson Arch (primera comunicación directa)",
        "key_events": (
            "— Exploración del estudio original replicado.\n"
            "— Primeras grabaciones sobre la historia de Gent Corporation.\n"
            "— Wilson Arch contacta con Audrey por primera vez directamente."
        ),
        "lore_revelations": (
            "— Gent Corporation fue fundada sobre los restos de Joey Drew Studios.\n"
            "— La tecnología de la Máquina de Tinta fue patentada y comercializada.\n"
            "— Wilson tiene un plan específico para Audrey que aún no revela."
        ),
        "composer": "theMeatly & NAB",
        "trivia": (
            "— Este capítulo contiene numerosas referencias y easter eggs para fans de BATIM.\n"
            "— Los objetos coleccionables de este capítulo revelan detalles sobre qué pasó "
            "entre los eventos de BATIM y BATDR."
        ),
    },
    {
        "game": "batdr",
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
        "game": "batdr",
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
    help = "Poblar la base de datos con personajes y capítulos de BATIM y BATDR"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Eliminar todos los personajes y capítulos existentes antes de insertar",
        )

    def handle(self, *args, **options) -> None:
        # Importa aquí para evitar problemas de inicialización de Django
        from bendy_app.models import Character, Chapter  # ← ajusta a tu ruta real

        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Eliminando datos existentes..."))
            Character.objects.all().delete()
            Chapter.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Datos eliminados."))

        # ── Insertar personajes ────────────────────────────────────────────────
        self.stdout.write("Insertando personajes...")
        characters_created: int = 0
        characters_updated: int = 0

        for data in CHARACTERS_DATA:
            slug: str = slugify(data["name"])
            character, created = Character.objects.update_or_create(
                slug=slug,
                defaults={**data, "slug": slug},
            )
            if created:
                characters_created += 1
            else:
                characters_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Personajes: {characters_created} creados, {characters_updated} actualizados."
            )
        )

        # ── Insertar capítulos ─────────────────────────────────────────────────
        self.stdout.write("Insertando capítulos...")
        chapters_created: int = 0
        chapters_updated: int = 0

        for data in CHAPTERS_DATA:
            slug: str = slugify(
                f"{data['game']}-chapter-{data['number']}-{data['title']}")
            chapter, created = Chapter.objects.update_or_create(
                game=data["game"],
                number=data["number"],
                defaults={**data, "slug": slug},
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

        self.stdout.write(
            self.style.SUCCESS("\n✓ Base de datos poblada correctamente."))
