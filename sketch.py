import pygame
import sys
import random

# Inicialize o Pygame
pygame.init()

# Defina as dimensões da tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))

# Defina a cor de fundo da tela
cor_fundo = (255, 255, 255)

# Defina o titulo da janela
pygame.display.set_caption("Snake.io")

# Defina as dimensões da cobra e da maçã
tamanho_celula = 20

# Velocidade inicial das cobras
velocidade = 10

# Direção inicial da cobra do jogador
direcao = (0, 0)

# Posição inicial da cobra do jogador
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

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimenta a cobra do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] and direcao != (0, 1):
        direcao = (0, -1)
    elif teclas[pygame.K_DOWN] and direcao != (0, -1):
        direcao = (0, 1)
    elif teclas[pygame.K_LEFT] and direcao != (1, 0):
        direcao = (-1, 0)
    elif teclas[pygame.K_RIGHT] and direcao != (-1, 0):
        direcao = (1, 0)

    # Movimenta a cobra inimiga
    direcao_inimiga = movimenta_cobra_inimiga()

    # Move a cobra do jogador
    x, y = cobra[0]
    nova_cabeca = ((x + direcao[0] * tamanho_celula) % largura, (y + direcao[1] * tamanho_celula) % altura)
    cobra.insert(0, nova_cabeca)

    # Move a cobra inimiga
    x, y = cobra_inimiga[0]
    nova_cabeca_inimiga = ((x + direcao_inimiga[0] * tamanho_celula) % largura, (y + direcao_inimiga[1] * tamanho_celula) % altura)
    cobra_inimiga.insert(0, nova_cabeca_inimiga)

    # Verifica se a cobra do jogador comeu a maçã
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

    # Desenha a cobra do jogador
    for parte in cobra:
        pygame.draw.rect(tela, (0, 128, 0), (*parte, tamanho_celula, tamanho_celula))

    # Desenha a cobra inimiga
    for parte in cobra_inimiga:
        pygame.draw.rect(tela, (128, 0, 0), (*parte, tamanho_celula, tamanho_celula))

    # Atualiza a tela
    pygame.display.flip()
    pygame.time.Clock().tick(velocidade)
