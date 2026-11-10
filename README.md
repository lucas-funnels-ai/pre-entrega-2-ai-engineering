# Pipeline de extracción técnica con LangChain

Recibe un párrafo de texto técnico (una arquitectura descrita o un log de error) y devuelve un objeto validado con Pydantic: tecnologías mencionadas, nivel de criticidad y resumen técnico.

## Archivos

- `schemas.py`: el esquema de Pydantic (el contrato de la salida).
- `chain.py`: el prompt, el modelo, la cadena con reintentos y la función asíncrona `process_text`.
- `main.py`: script de prueba que corre un ejemplo de punta a punta.

## Cómo correrlo

1. Instalá las librerías:

        pip install langchain langchain-anthropic pydantic python-dotenv

2. Creá un archivo `.env` en la misma carpeta con tu clave de Anthropic:

        ANTHROPIC_API_KEY=tu_clave_acá

3. Ejecutá el script:

        python main.py

Si lo corrés en Google Colab, guardá la clave en los Secretos con el nombre `ANTHROPIC_API_KEY` y activá el acceso desde el notebook.

## Ejemplo de salida

    {
      "tecnologias": ["Node.js", "PostgreSQL", "Redis"],
      "nivel_de_criticidad": "alta",
      "resumen_tecnico": "Una API en Node.js se conecta a PostgreSQL. Desde ayer, cuando Redis se queda sin memoria, el servicio responde con error 500 y los usuarios no pueden completar pagos."
    }

## Resiliencia

La cadena reintenta hasta 3 veces, con espera creciente, ante errores de red, límite de velocidad o una respuesta que no encaje en el esquema.
