import asyncio

from chain import process_text

TEXTO = (
    "Nuestra API en Node.js se conecta a una base PostgreSQL. "
    "Desde ayer, cada vez que Redis se queda sin memoria, el servicio "
    "devuelve error 500 y los usuarios no pueden pagar."
)


async def main():
    resultado = await process_text(TEXTO)
    print(resultado.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
