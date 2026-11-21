import pygame

ANCHO, ALTO = (640, 420)
FPS = 60
COLOR_FONDO = (245, 247, 252)
COLOR_TEXTO = (30, 35, 60)
COLOR_SUAVE = (110, 115, 140)
COLOR_PRIMARIO = (98, 76, 214)
COLOR_PRIMARIO_HOVER = (120, 100, 235)
COLOR_SECUNDARIO = (200, 205, 220)
COLOR_SECUNDARIO_HOVER = (180, 186, 205)


class Contador:

    def __init__(self, valor_inicial: int = 0) -> None:
        self._valor = valor_inicial

    @property
    def valor(self) -> int:
        return self._valor

    def incrementar(self) -> None:
        self._valor += 1

    def reiniciar(self) -> None:
        self._valor = 0


class Boton:

    def __init__(
        self,
        texto,
        x,
        y,
        ancho,
        alto,
        fuente,
        al_hacer_clic,
        color=COLOR_PRIMARIO,
        color_hover=COLOR_PRIMARIO_HOVER,
        color_texto=(255, 255, 255),
    ) -> None:
        self.texto = texto
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.fuente = fuente
        self.al_hacer_clic = al_hacer_clic
        self.color = color
        self.color_hover = color_hover
        self.color_texto = color_texto

    def manejar_evento(self, evento: pygame.event.Event) -> None:
        if (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        ):
            self.al_hacer_clic()

    def dibujar(self, superficie: pygame.Surface) -> None:
        encima = self.rect.collidepoint(pygame.mouse.get_pos())
        color = self.color_hover if encima else self.color
        pygame.draw.rect(superficie, color, self.rect, border_radius=12)
        etiqueta = self.fuente.render(self.texto, True, self.color_texto)
        superficie.blit(etiqueta, etiqueta.get_rect(center=self.rect.center))


class AplicacionContador:

    def __init__(self) -> None:
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Contador interactivo - Pygame")
        self.reloj = pygame.time.Clock()
        self.ejecutando = True
        self.fuente_titulo = pygame.font.SysFont(None, 40)
        self.fuente_numero = pygame.font.SysFont(None, 140)
        self.fuente_boton = pygame.font.SysFont(None, 32)
        self.fuente_ayuda = pygame.font.SysFont(None, 24)
        self.contador = Contador()
        self.botones = [
            Boton(
                "Sumar +1",
                130,
                290,
                180,
                60,
                self.fuente_boton,
                al_hacer_clic=self.sumar,
            ),
            Boton(
                "Reiniciar",
                330,
                290,
                180,
                60,
                self.fuente_boton,
                al_hacer_clic=self.reiniciar,
                color=COLOR_SECUNDARIO,
                color_hover=COLOR_SECUNDARIO_HOVER,
                color_texto=COLOR_TEXTO,
            ),
        ]

    def sumar(self) -> None:
        self.contador.incrementar()

    def reiniciar(self) -> None:
        self.contador.reiniciar()

    def procesar_eventos(self) -> None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.sumar()
                elif evento.key == pygame.K_r:
                    self.reiniciar()
                elif evento.key == pygame.K_ESCAPE:
                    self.ejecutando = False
            for boton in self.botones:
                boton.manejar_evento(evento)

    def dibujar(self) -> None:
        self.pantalla.fill(COLOR_FONDO)
        titulo = self.fuente_titulo.render("Contador interactivo", True, COLOR_TEXTO)
        self.pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 50)))
        numero = self.fuente_numero.render(
            str(self.contador.valor), True, COLOR_PRIMARIO
        )
        self.pantalla.blit(numero, numero.get_rect(center=(ANCHO // 2, 170)))
        for boton in self.botones:
            boton.dibujar(self.pantalla)
        ayuda = self.fuente_ayuda.render(
            "Clic en los botones  |  ESPACIO = +1  |  R = reiniciar  |  ESC = salir",
            True,
            COLOR_SUAVE,
        )
        self.pantalla.blit(ayuda, ayuda.get_rect(center=(ANCHO // 2, 385)))
        pygame.display.flip()

    def ejecutar(self) -> None:
        while self.ejecutando:
            self.procesar_eventos()
            self.dibujar()
            self.reloj.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    AplicacionContador().ejecutar()
