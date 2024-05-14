import pygame
import sys
import random
from pygame.locals import *

# Inicialize o Pygame
pygame.init()

# Defina as dimensões da tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))

# Defina a cor de fundo da tela
cor_fundo = (255, 255, 255)

# Defina as dimensões da cobra e da maçã
tamanho_celula = 20

# Velocidade inicial das cobras
velocidade_jogador = 10

# Direção inicial da sua cobra
direcao = (0, 0)

# Posição inicial da sua cobra
cobra = [(largura // 2, altura // 2)]

# Posição inicial da maçã
maça = (random.randint(0, largura - tamanho_celula) // tamanho_celula * tamanho_celula,
        random.randint(0, altura - tamanho_celula) // tamanho_celula * tamanho_celula)

# Posição inicial da cobra inimiga
cobra_inimiga = [(random.randint(0, largura - tamanho_celula) // tamanho_celula * tamanho_celula,
                  random.randint(0, altura - tamanho_celula) // tamanho_celula * tamanho_celula)]

# Função para movimentar a cobra inimiga em direção à maçã
def movimenta_cobra_inimiga():
    x, y = cobra_inimiga[0]
    maça_x, maça_y = maça

    # Calcula a direção da cobra inimiga em relação à maçã
    if x < maça_x:
        direcao_x = 1
        direcao_y = 0
    elif x > maça_x:
        direcao_x = -1
        direcao_y = 0
    elif y < maça_y:
        direcao_x = 0
        direcao_y = 1
    elif y > maça_y:
        direcao_x = 0
        direcao_y = -1
    else:
        direcao_x = 0
        direcao_y = 0

    # Se a cobra inimiga está muito próxima do jogador, tenta desviar
    if abs(x - cobra[0][0]) < tamanho_celula * 2 and abs(y - cobra[0][1]) < tamanho_celula * 2:
        if random.random() < 0.5:
            if direcao_x == 0:
                if x < cobra[0][0]:
                    direcao_x = 1
                else:
                    direcao_x = -1
                direcao_y = 0
            else:
                direcao_x = 0
                if y < cobra[0][1]:
                    direcao_y = 1
                else:
                    direcao_y = -1

    # Com uma certa probabilidade, muda a direção da cobra inimiga
    if random.random() < 0.2:
        direcoes_possiveis = [(direcao_x, 0), (0, direcao_y)]
        direcao_x, direcao_y = random.choice(direcoes_possiveis)

    return direcao_x, direcao_y

# Verifica se há pelo menos um controle conectado
if pygame.joystick.get_count() > 0:
    # Inicializa o primeiro controle encontrado
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Controle:", joystick.get_name())
else:
    print("Nenhum controle encontrado.")

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Movimenta a sua cobra com o teclado
        if evento.type == KEYDOWN:
            if evento.key == K_UP and direcao != (0, 1):
                direcao = (0, -1)
            elif evento.key == K_DOWN and direcao != (0, -1):
                direcao = (0, 1)
            elif evento.key == K_LEFT and direcao != (1, 0):
                direcao = (-1, 0)
            elif evento.key == K_RIGHT and direcao != (-1, 0):
                direcao = (1, 0)

        # Movimenta a sua cobra com o controle
        if evento.type == JOYAXISMOTION:
            if evento.axis == 0:  # Eixo X
                if evento.value > 0.5 and direcao != (-1, 0):
                    direcao = (1, 0)
                elif evento.value < -0.5 and direcao != (1, 0):
                    direcao = (-1, 0)
            elif evento.axis == 1:  # Eixo Y
                if evento.value > 0.5 and direcao != (0, -1):
                    direcao = (0, 1)
                elif evento.value < -0.5 and direcao != (0, 1):
                    direcao = (0, -1)

        # Processa os botões pressionados
        elif evento.type == JOYBUTTONDOWN:
            if evento.button == 0:
                # Ação do botão 0
                pass
            elif evento.button == 1:
                # Ação do botão 1
                pass

    # Movimenta a cobra inimiga
    direcao_inimiga = movimenta_cobra_inimiga()

    # Move a sua cobra
    x, y = cobra[0]
    nova_cabeca = ((x + direcao[0] * tamanho_celula) % largura, (y + direcao[1] * tamanho_celula) % altura)
    cobra.insert(0, nova_cabeca)

    # Move a cobra inimiga
    x, y = cobra_inimiga[0]
    nova_cabeca_inimiga = ((x + direcao_inimiga[0] * tamanho_celula) % largura, (y + direcao_inimiga[1] * tamanho_celula) % altura)
    cobra_inimiga.insert(0, nova_cabeca_inimiga)

    # Verifica se a sua cobra comeu a maçã
    if nova_cabeca == maça:
        maça = (random.randint(0, largura - tamanho_celula) // tamanho_celula * tamanho_celula,
                random.randint(0, altura - tamanho_celula) // tamanho_celula * tamanho_celula)
    else:
        cobra.pop()

    # Verifica se a cobra inimiga comeu a maçã
    if nova_cabeca_inimiga == maça:
        maça = (random.randint(0, largura - tamanho_celula) // tamanho_celula * tamanho_celula,
                random.randint(0, altura - tamanho_celula) // tamanho_celula * tamanho_celula)
    else:
        cobra_inimiga.pop()

    # Verifica colisão entre as cobras
    if nova_cabeca_inimiga in cobra:
        pygame.quit()
        sys.exit()
    elif nova_cabeca in cobra_inimiga:
        pygame.quit()
        sys.exit()

    # Preenche a tela com a cor de fundo
    tela.fill(cor_fundo)

    # Desenha a maçã
    pygame.draw.rect(tela, (255, 0, 0), (*maça, tamanho_celula, tamanho_celula))

    # Desenha a sua cobra
    for parte in cobra:
        pygame.draw.rect(tela, (0, 128, 0), (*parte, tamanho_celula, tamanho_celula))

    # Desenha a cobra inimiga
    for parte in cobra_inimiga:
        pygame.draw.rect(tela, (128, 0, 0), (*parte, tamanho_celula, tamanho_celula))

    # Atualiza a tela
    pygame.display.flip()
    pygame.time.Clock().tick(velocidade_jogador)
