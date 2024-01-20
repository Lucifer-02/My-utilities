"""Online translation library"""

from subprocess import check_output
import requests


def _trans_crow(source_lang: str, target_lang: str, source_text: str) -> str:
    """Using crow-translate to translate the text."""
    return check_output(
        ["crow", "-b", "-s", source_lang, "-t", target_lang, source_text]
    ).decode("utf-8")


def _get_trans(
    source_lang: str, target_lang: str, source_text: str
) -> requests.Response:
    """Getting translation with given text using Google Translate API."""

    base_url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "ie": "UTF-8",
        "oe": "UTF-8",
        "dt": "t",
        "sl": source_lang,
        "tl": target_lang,
        "q": source_text,
    }
    response = requests.get(base_url, params=params, timeout=3)
    return response


def _trans_api(source_lang: str, target_lang: str, source_text: str) -> str:
    """Using Google Translate API directly to translate the text.

    Raise:
        Exception: An Error occurred getting translation.
    """

    try:
        response = _get_trans(
            source_lang=source_lang,
            target_lang=target_lang,
            source_text=source_text,
        )

        # paragraph will be split to phrases by google translate
        chunks = response.json()[0]
        translation_chunks = [chunks[i][0] for i in range(len(chunks))]

        translation = "".join(translation_chunks)

        return "" if translation is None else translation
    except Exception as error:
        print("Translating error: ", error)

    return ""


def trans(
    source_lang: str, target_lang: str, source_text: str, translator="api"
) -> str:
    """Translate give text."""

    if translator == "crow":
        return _trans_crow(
            source_lang=source_lang,
            target_lang=target_lang,
            source_text=source_text,
        )
    if translator == "api":
        return _trans_api(
            source_lang=source_lang,
            target_lang=target_lang,
            source_text=source_text,
        )
    return ""
