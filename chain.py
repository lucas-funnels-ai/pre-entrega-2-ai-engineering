import logging

from anthropic import APIConnectionError, APITimeoutError, RateLimitError
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import ChatPromptTemplate
from pydantic import ValidationError

from schemas import ExtraccionTecnica

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("pipeline")

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Sos un analista técnico. Leés textos sobre sistemas, arquitecturas "
        "o errores y extraés datos precisos. No inventes información que "
        "no esté en el texto.",
    ),
    ("human", "Analizá este texto:\n\n{texto}"),
])

model = ChatAnthropic(model="claude-haiku-5-5")

structured_model = model.with_structured_output(ExtraccionTecnica).with_retry(
    retry_if_exception_type=(
        ValidationError,
        OutputParserException,
        RateLimitError,
        APIConnectionError,
        APITimeoutError,
    ),
    stop_after_attempt=3,
    wait_exponential_jitter=True,
)

chain = prompt | structured_model


async def process_text(text: str) -> ExtraccionTecnica:
    logger.info("Procesando texto de %d caracteres", len(text))
    try:
        resultado = await chain.ainvoke({"texto": text})
    except ValidationError as error:
        logger.error("Falló la validación del esquema: %s", error)
        raise
    except (RateLimitError, APIConnectionError, APITimeoutError) as error:
        logger.error("Falló la conexión con el modelo: %s", error)
        raise
    logger.info(
        "Validación correcta, criticidad: %s",
        resultado.nivel_de_criticidad.value,
    )
    return resultado
