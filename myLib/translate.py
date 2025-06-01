"""Online translation library"""

from subprocess import check_output
import requests
import urllib.parse  # Import for URL encoding example print


def _trans_crow(source_lang: str, target_lang: str, source_text: str) -> str:
    """Using crow-translate to translate the text."""
    try:
        # crow-translate typically outputs to stdout. Decode assumes UTF-8.
        # Check the output for errors before returning. crow might print errors to stderr or stdout.
        # This basic check assumes any non-empty output is a successful translation.
        # More robust error handling might be needed depending on crow-translate's output format.
        output = check_output(
            ["crow", "-b", "-s", source_lang, "-t", target_lang, source_text],
            encoding="utf-8", # Use encoding instead of decoding after the fact
            text=True # Use text mode for check_output
        ).strip() # Strip leading/trailing whitespace

        # Basic check: if output is empty, maybe it failed? Or maybe the source text was empty?
        # This is a simple assumption, crow's specific error output would need to be handled more precisely.
        if not output:
             print(f"Warning: crow-translate returned empty output for text: '{source_text}'")
             # Consider raising an exception or returning a specific error indicator if empty output is always a failure
             # For now, we return empty string as original _trans_api did on some failures
             return ""

        return output

    except Exception as e:
        # Catch errors during subprocess execution
        print(f"Error during crow-translate execution: {e}")
        return f"Error: crow-translate failed - {e}"


def _fetch_json(url: str, params: dict,  timeout: int = 10, headers: dict| None = None):
    """
    Helper function to perform an HTTP GET request and return JSON data or error.

    Args:
        url (str): The base URL for the request.
        params (dict): Dictionary of URL parameters.
        headers (dict, optional): Dictionary of HTTP headers. Defaults to None.
        timeout (int, optional): Timeout in seconds. Defaults to 10.

    Returns:
        dict | str: The parsed JSON response on success, or an error string on failure.
    """
    try:
        response = requests.get(
            url, params=params, headers=headers, timeout=timeout
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Error Connecting: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"An unexpected Request Error occurred: {err}"
    except Exception as e:
        # Catch potential JSONDecodeError or other unexpected issues
        return f"An unexpected error occurred after request: {e}"


def _google_trans(source_lang: str, target_lang: str, source_text: str) -> str:
    """Using Google Translate API directly to translate the text (older API).

    Raise:
        Exception: An Error occurred getting translation.
    """
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

    json_data = _fetch_json(base_url, params)

    if isinstance(json_data, str):
        # _fetch_json returned an error string
        print(f"Translating error: {json_data}")
        return "" # Return empty string on error, consistent with original behavior

    try:
        # Expecting a structure like [[["translated text","original text",...]],...]
        # The first element [0] should contain a list of chunks/sentences.
        # Each chunk [i][0] should contain the translated text for that chunk.
        if isinstance(json_data, list) and len(json_data) > 0 and isinstance(json_data[0], list):
             chunks = json_data[0]
             translation_chunks = [chunk[0] for chunk in chunks if isinstance(chunk, list) and len(chunk) > 0]
             translation = "".join(translation_chunks)
             return "" if translation is None else translation
        else:
             # Unexpected JSON structure
             print(f"Translating error: Unexpected JSON structure from _trans_api: {json_data}")
             return "" # Return empty string for unexpected structure


    except Exception as error:
        # Catch errors during JSON parsing
        print(f"Translating error during JSON parsing: {error}")
        return "" # Return empty string on parsing error


def _google_trans_new(
    source_text: str, source_lang: str = "auto", target_lang: str = "en"
) -> str:
    """
    Attempts to translate text using an unofficial Google Translate endpoint.

    WARNING: This method is highly unstable and not recommended for production use.
    It relies on an undocumented API and a hardcoded key, which can break at any time.

    Args:
        text (str): The text to translate.
        source_lang (str): The source language code (e.g., 'en', 'es', 'fr', 'auto').
        target_lang (str): The target language code (e.g., 'en', 'es', 'fr').

    Returns:
        str: The translated text, or an error/warning string if translation fails or response is unexpected.
    """
    # --- Configuration (based on the original class) ---
    UNOFFICIAL_ENDPOINT = "https://translate-pa.googleapis.com/v1/translate"
    # HARDCODED_API_KEY: This key is known to be unstable and potentially invalid.
    # Using this endpoint and key is a hack and will likely break.
    HARDCODED_API_KEY = "AIzaSyDLEeFI5OtFBwYBIoK_jj5m32rZK5CkCXA"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 "
        "Safari/537.36",
    }

    params = {
        "params.client": "gtx",
        "query.source_language": source_lang,
        "query.target_language": target_lang,
        "query.display_language": "en-US",
        "data_types": "TRANSLATION",
        "key": HARDCODED_API_KEY, # This key is likely expired or invalid
        "query.text": source_text,
    }

    # --- Print the full URL Request ---
    # 1. Option: Manually construct the URL to see what it *should* look like
    # print(f"--- Manually constructed URL (before request) ---")
    # print(f"{UNOFFICIAL_ENDPOINT}?{urllib.parse.urlencode(params)}") # Use urllib.parse

    json_data = _fetch_json(UNOFFICIAL_ENDPOINT, params, headers=headers, timeout=10)

    # Check if _fetch_json returned an error string
    if isinstance(json_data, str):
        print(f"\n--- Actual Full URL Requested (after request sent) ---")
        # Note: We don't have the exact URL from requests object here,
        # as _fetch_json only returns the data or error string.
        # A more advanced _fetch_json could return (data, url) tuple on success.
        # For now, we'll just print the base URL and parameters.
        print(f"{UNOFFICIAL_ENDPOINT}?{urllib.parse.urlencode(params)}")
        print(f"----------------------------------------------------\n")
        return json_data # Return the error string directly

    # If we got JSON data, print the URL anyway for debugging
    print(f"\n--- Actual Full URL Requested (after request sent) ---")
    # Again, approximating the URL.
    print(f"{UNOFFICIAL_ENDPOINT}?{urllib.parse.urlencode(params)}")
    print(f"----------------------------------------------------\n")


    # The response structure for this unofficial API can vary.
    # Common structures include:
    # 1. A nested list structure like [[["translated text","original text",...]],...]
    # 2. A 'translation' key (less common for this specific endpoint structure historically)
    # 3. A 'sentences' key with 'trans' for each sentence

    try:
        # Attempt parsing structure 1: [[["translated text",...]],...]
        if (
            isinstance(json_data, list)
            and len(json_data) > 0
            and isinstance(json_data[0], list)
            and len(json_data[0]) > 0
            and isinstance(json_data[0][0], list)
            and len(json_data[0][0]) > 0
        ):
            return json_data[0][0][0]  # Accesses the first translated segment

        # Attempt parsing structure 2: {"translation": "translated text"}
        elif isinstance(json_data, dict) and "translation" in json_data:
            return json_data["translation"]

        # Attempt parsing structure 3: {"sentences": [{"trans": "part1"}, {"trans": "part2"}, ...]}
        elif (
            isinstance(json_data, dict)
            and "sentences" in json_data
            and isinstance(json_data["sentences"], list)
        ):
            translated_sentences = [
                s["trans"] for s in json_data["sentences"] if isinstance(s, dict) and "trans" in s
            ]
            return "".join(translated_sentences)

        # If none of the expected structures match
        return f"Warning: Unexpected JSON response structure from _google_trans_new: {json_data}"

    except Exception as e:
        # Catch errors during JSON parsing
        return f"Error parsing JSON response from _google_trans_new: {e}"


# --- Function to perform translation ---
def trans(
    source_lang: str, target_lang: str, source_text: str, translator="api"
) -> str:
    """Translate give text."""

    # Basic validation for empty source text
    if not source_text.strip():
        return ""

    if translator == "crow":
        return _trans_crow(
            source_lang=source_lang,
            target_lang=target_lang,
            source_text=source_text,
        )
    if translator == "api": # Keep "api" for the older Google Translate endpoint
        return _google_trans(
            source_lang=source_lang,
            target_lang=target_lang,
            source_text=source_text,
        )

    if translator == "google_new": # Keep "google_new" for the unofficial endpoint
        return _google_trans_new(
            source_text=source_text, # Note: _google_trans_new signature is text, src, tgt
            source_lang=source_lang,
            target_lang=target_lang,
        )

    # Handle unknown translator option
    print(f"Warning: Unknown translator option '{translator}' requested.")
    return f"Error: Unknown translator option '{translator}'."
