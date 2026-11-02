"""Executa o fluxo completo do sistema de streaming."""

from dados import USUARIOS_POR_TAMANHO, gerar_musicas, gerar_usuarios
from inversoes import similaridade
from mediana import mediana, percentil
from par_proximo import musicas_mais_parecidas

TAMANHO_DEMONSTRACAO = 1000


def usuarios_mais_parecidos(usuarios):
    """Devolve o par de usuários com menor distância de Kendall tau."""
    if len(usuarios) < 2:
        raise ValueError("são necessários pelo menos dois usuários")

    melhor = None
    for i, usuario_a in enumerate(usuarios):
        for usuario_b in usuarios[i + 1:]:
            distancia = similaridade(usuario_a.ranking, usuario_b.ranking)
            resultado = (distancia, usuario_a.id, usuario_b.id, usuario_a, usuario_b)
            if melhor is None or resultado[:3] < melhor[:3]:
                melhor = resultado
    return melhor[3], melhor[4], melhor[0]


def executar(n=TAMANHO_DEMONSTRACAO):
    print("=== Sistema de Recomendação para Streaming de Música ===")
    print(f"\n1. Carregamento de dados (semente fixa): {n} músicas e {USUARIOS_POR_TAMANHO} usuários")
    musicas = gerar_musicas(n)
    usuarios = gerar_usuarios(USUARIOS_POR_TAMANHO, n)

    usuario_a, usuario_b, divergencia = usuarios_mais_parecidos(usuarios)
    print("\n2. Usuários mais parecidos — contagem de inversões")
    print(f"   Usuários {usuario_a.id} e {usuario_b.id}: distância normalizada = {divergencia:.4f}")

    musica_a, musica_b, distancia = musicas_mais_parecidas(musicas)
    print("\n3. Músicas mais parecidas — par de pontos mais próximo")
    print(f"   {musica_a.nome} e {musica_b.nome}: distância = {distancia:.6f}")

    duracoes = [musica.duracao for musica in musicas]
    plays = [musica.plays for musica in musicas]
    print("\n4. Valores típicos — mediana das medianas")
    print(
        f"   Duração: mediana = {mediana(duracoes):.1f} s; "
        f"P25 = {percentil(duracoes, 25):.1f} s; P75 = {percentil(duracoes, 75):.1f} s"
    )
    print(
        f"   Plays: mediana = {mediana(plays):.1f}; "
        f"P25 = {percentil(plays, 25):.1f}; P75 = {percentil(plays, 75):.1f}"
    )


if __name__ == "__main__":
    executar()
