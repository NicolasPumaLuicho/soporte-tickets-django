import random
import time

from tickets.models import CodigoPrueba


def llenar(n=100000):
    CodigoPrueba.objects.all().delete()
    codigos = list(range(1, n + 1))
    random.shuffle(codigos)
    CodigoPrueba.objects.bulk_create(
        [CodigoPrueba(sin_indice=c, con_indice=c) for c in codigos],
        batch_size=5000)
    print("Filas cargadas:", CodigoPrueba.objects.count())


def tiempo_ms(consulta, veces=50):
    inicio = time.perf_counter()
    for _ in range(veces):
        consulta.exists()
    return (time.perf_counter() - inicio) / veces * 1000


def medir(codigo):
    sin = CodigoPrueba.objects.filter(sin_indice=codigo)
    con = CodigoPrueba.objects.filter(con_indice=codigo)
    print("Sin índice:", sin.explain())
    print("Con índice:", con.explain())
    print(f"Tiempo sin índice: {tiempo_ms(sin):.3f} ms")
    print(f"Tiempo con índice: {tiempo_ms(con):.3f} ms")
