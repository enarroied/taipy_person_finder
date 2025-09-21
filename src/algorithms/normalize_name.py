import re
import unicodedata


def normalize_name(name):
    """Normalize name for comparison: lowercase, remove accents,
    trim, replace non-letters with dash
    """
    if name is None or name == "":
        return ""

    name = str(name).lower().strip()
    name = unicodedata.normalize("NFD", name)
    name = "".join(char for char in name if unicodedata.category(char) != "Mn")
    # Replace non-letters with a dash
    name = re.sub(r"[^a-z\s]", "-", name)
    # Replace multiple spaces/dashes with a single dash
    name = re.sub(r"[\s\-]+", "-", name)

    return name.strip("-")
