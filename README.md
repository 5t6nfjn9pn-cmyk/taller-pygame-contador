# Contador interactivo con Pygame

**Asignatura:** Programacion Orientada a Objetos
**Tema:** Interfaces graficas y programacion orientada a eventos
**Biblioteca seleccionada:** [Pygame](https://www.pygame.org/)

Aplicacion minima que muestra un contador en una ventana. El contador aumenta cuando el usuario hace clic en el boton **"Sumar +1"** (o presiona **ESPACIO**) y vuelve a cero con el boton **"Reiniciar"** (o la tecla **R**).

![Aplicacion funcionando](captura.png)

---

## 1. Investigacion

### Que es Pygame y cual es su proposito principal?
Pygame es una biblioteca libre y de codigo abierto para Python, construida sobre **SDL (Simple DirectMedia Layer)**, una libreria en C que da acceso a graficos, sonido, teclado, raton y joysticks. Su proposito principal es facilitar la creacion de **videojuegos y aplicaciones multimedia 2D** sin tener que programar a bajo nivel. Es un proyecto comunitario activo desde el 2000.

### Que tipo de aplicaciones permite desarrollar?
- Videojuegos 2D (plataformas, arcade, puzzles).
- Simulaciones y visualizaciones interactivas (fisica, animaciones).
- Aplicaciones educativas y prototipos con graficos, sonido y entrada del usuario.
- Interfaces graficas personalizadas (menus, botones y paneles dibujados a mano).

Funciona en Windows, macOS y Linux.

### Como se instala y que requisitos necesita?
Requisitos: **Python 3** (la version 2.6.1 exige Python >= 3.6; se recomienda la version mas reciente) y **pip**.

```bash
python -m pip install -U pygame
# Comprobar la instalacion con un ejemplo incluido:
python -m pygame.examples.aliens
```

Las ruedas (wheels) de pip ya incluyen SDL, asi que no se necesita instalar nada mas en la mayoria de los sistemas.

### Cuales son sus principales componentes o elementos graficos?
| Modulo / clase | Para que sirve |
|---|---|
| `pygame.display` | Crear y actualizar la ventana (`set_mode`, `flip`, `set_caption`). |
| `pygame.Surface` | "Lienzo" o imagen sobre la que se dibuja; la ventana tambien es una Surface. |
| `pygame.Rect` | Rectangulo para posicionar elementos y detectar colisiones/clics (`collidepoint`). |
| `pygame.draw` | Dibujar figuras: rectangulos, circulos, lineas, poligonos. |
| `pygame.font` | Renderizar texto como imagen. |
| `pygame.image` | Cargar y guardar imagenes (PNG, JPG...). |
| `pygame.event` | Cola de eventos del usuario y del sistema. |
| `pygame.sprite` | Clases `Sprite` y `Group` para organizar objetos del juego. |
| `pygame.mixer` | Reproducir sonidos y musica. |
| `pygame.time.Clock` | Controlar los cuadros por segundo (FPS). |

**Importante:** Pygame **no trae widgets listos** (botones, cajas de texto, etc.) como Tkinter: se construyen combinando `Rect`, `draw` y `font`, como el boton de este proyecto.

### Como maneja los eventos del usuario?
Pygame guarda todo lo que hace el usuario en una **cola de eventos**. El programa la lee en cada vuelta del **ciclo principal** con `pygame.event.get()` y revisa el tipo de cada evento:

| Evento | Atributos utiles | Cuando ocurre |
|---|---|---|
| `QUIT` | - | El usuario cierra la ventana. |
| `KEYDOWN` / `KEYUP` | `key`, `mod`, `unicode` | Se presiona / suelta una tecla. |
| `MOUSEBUTTONDOWN` / `MOUSEBUTTONUP` | `pos`, `button` | Se presiona / suelta un boton del raton. |
| `MOUSEMOTION` | `pos`, `rel`, `buttons` | Se mueve el raton. |

```python
for evento in pygame.event.get():
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if boton.rect.collidepoint(evento.pos):
            contador += 1
    elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
        contador += 1
```

A diferencia de Tkinter (donde se "enlaza" una funcion al boton con `command=` o `bind`), en Pygame **el programador escribe el ciclo de eventos** y decide que hacer con cada uno.

### Ventajas y limitaciones frente a Tkinter
| | Pygame | Tkinter |
|---|---|---|
| Instalacion | `pip install pygame` | Viene incluido con Python |
| Widgets listos (boton, entrada, menu) | No, hay que construirlos | Si |
| Ciclo de eventos | Lo escribe el programador (control total) | Automatico (`mainloop`) |
| Animacion, FPS, sprites | Excelente | Limitado |
| Sonido y joystick | Integrado | No |
| Formularios / apps de oficina | Poco practico | Ideal |
| Aspecto | Totalmente personalizable | Aspecto nativo / clasico |

**Ventajas de Pygame:** control total del dibujo y de la tasa de refresco, ideal para juegos y animaciones, manejo de sonido, imagenes y dispositivos de entrada, gran comunidad y muchos ejemplos.
**Limitaciones:** no tiene widgets estandar ni administradores de layout, por lo que hacer formularios o apps "de escritorio" cuesta mas; se redibuja la pantalla completa en cada cuadro; requiere instalacion adicional.

---

## 2. Instalacion y ejecucion

```bash
git clone https://github.com/5t6nfjn9pn-cmyk/taller-pygame-contador.git
cd taller-pygame-contador

# (Opcional) entorno virtual
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

pip install -r requirements.txt
python main.py
```

**Controles**
- Clic en **Sumar +1** o tecla **ESPACIO** -> suma 1.
- Clic en **Reiniciar** o tecla **R** -> vuelve a 0.
- **ESC** o cerrar la ventana -> salir.

---

## 3. Explicacion del funcionamiento

**Como se crea la ventana principal?**
En el constructor de `AplicacionContador` se inicializa Pygame con `pygame.init()` y se crea la ventana con `pygame.display.set_mode((640, 420))`, que devuelve una `Surface` donde se dibuja todo. `pygame.display.set_caption()` pone el titulo.

**Como se crean y muestran los componentes graficos?**
- El **texto** (titulo, numero y ayuda) se convierte en imagen con `fuente.render(...)` y se pega en la ventana con `blit`.
- Cada **boton** es un objeto `Boton` que tiene un `pygame.Rect` (posicion y medidas). En `Boton.dibujar()` se dibuja un rectangulo redondeado con `pygame.draw.rect` y el texto centrado encima; ademas cambia de color cuando el raton pasa por encima.
- En cada cuadro, `AplicacionContador.dibujar()` limpia la pantalla con `fill`, vuelve a dibujar todo y muestra el resultado con `pygame.display.flip()`.

**Que evento se implemento y como se detecta?**
- `MOUSEBUTTONDOWN`: clic del raton. `Boton.manejar_evento()` comprueba que sea el boton izquierdo (`evento.button == 1`) y que la posicion del clic este dentro del boton (`self.rect.collidepoint(evento.pos)`).
- `KEYDOWN`: tecla presionada. Se compara `evento.key` con `pygame.K_SPACE`, `pygame.K_r` y `pygame.K_ESCAPE`.
- `QUIT`: cierre de la ventana.

Todos se leen en `AplicacionContador.procesar_eventos()` con `pygame.event.get()`.

**Que funcion o metodo responde al evento?**
Cada boton recibe al crearse una funcion *callback* (`al_hacer_clic`). Cuando detecta el clic, la llama:
- Boton "Sumar +1" -> `AplicacionContador.sumar()` -> `Contador.incrementar()`.
- Boton "Reiniciar" -> `AplicacionContador.reiniciar()` -> `Contador.reiniciar()`.

Las teclas ESPACIO y R llaman a los mismos metodos.

**Como se modifica la interfaz despues de la interaccion?**
El metodo solo cambia el **dato** (`Contador._valor`). En la siguiente vuelta del ciclo, `dibujar()` vuelve a renderizar el numero con `str(self.contador.valor)`, asi que el usuario ve el nuevo valor de inmediato (el ciclo corre a 60 cuadros por segundo).

```
Ciclo principal (ejecutar):
  +--> procesar_eventos()  -> detecta clic/tecla -> sumar()/reiniciar() -> cambia Contador
  |   dibujar()           -> pinta el valor actual
  +-- reloj.tick(60)
```

---

## 4. Reto adicional: Programacion Orientada a Objetos

Pygame **si permite** construir interfaces con clases y objetos: la propia biblioteca esta hecha con clases (`Surface`, `Rect`, `Sprite`, `Group`, `Clock`) y la documentacion oficial anima a heredar de `pygame.sprite.Sprite` para crear objetos propios. Este proyecto esta organizado en tres clases:

| Clase | Responsabilidad |
|---|---|
| `Contador` | **Modelo.** Guarda el valor y define las reglas para cambiarlo (`incrementar`, `reiniciar`). Encapsula el dato (`_valor`) y lo expone solo para lectura con `@property`. No depende de Pygame. |
| `Boton` | **Componente visual reutilizable.** Sabe dibujarse, detectar si un clic cae dentro de su area y ejecutar la accion (callback) que se le asigno. Se puede crear cualquier cantidad de botones con distinto texto, color y accion. |
| `AplicacionContador` | **Controlador / ventana principal.** Crea la ventana y los componentes, ejecuta el ciclo principal, reparte los eventos y redibuja la interfaz. Conecta los botones con el modelo. |

Ventajas de esta estructura: cada clase tiene una sola responsabilidad, el boton se reutiliza sin copiar codigo, y la logica del contador se podria usar con otra interfaz (por ejemplo, Tkinter) sin cambiarla.

---

## 5. Evidencia

![Aplicacion funcionando despues de varios clics](captura.png)

---

## 6. Fuentes consultadas

- Pygame - Documentacion oficial: https://www.pygame.org/docs/
- Pygame - Getting Started (instalacion): https://www.pygame.org/wiki/GettingStarted
- Pygame - Modulo `pygame.event`: https://www.pygame.org/docs/ref/event.html
- Pygame - Modulo `pygame.display`: https://www.pygame.org/docs/ref/display.html
- Pygame - Clase `pygame.Rect`: https://www.pygame.org/docs/ref/rect.html
- Pygame - Modulo `pygame.sprite`: https://www.pygame.org/docs/ref/sprite.html
- Pygame - Tutorial de entrada (teclado y raton): https://www.pygame.org/ftp/contrib/input.html
- Pygame en PyPI: https://pypi.org/project/pygame/
- Documentacion de Tkinter (Python): https://docs.python.org/3/library/tkinter.html
