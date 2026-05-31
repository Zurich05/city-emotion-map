import re


HTML_RE = re.compile(r"<[^>]+>")
URL_RE = re.compile(r"https?://\S+|www\.\S+")
PHONE_RE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
ID_CARD_RE = re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)")
ADDRESS_RE = re.compile(r"[\u4e00-\u9fa5]{2,}(?:路|街|巷|道|弄|村|小区|大厦|楼|号楼)?\d+(?:号|栋|层|室|单元)")
ALLOWED_RE = re.compile(r"[^\u4e00-\u9fa5A-Za-z0-9，。！？、,.!?：:；;（）()\-\s]")
SPACE_RE = re.compile(r"\s+")


def clean_text(text: str, min_length: int = 3) -> str:
    if not text:
        return ""
    cleaned = HTML_RE.sub(" ", text)
    cleaned = URL_RE.sub(" ", cleaned)
    cleaned = PHONE_RE.sub(" ", cleaned)
    cleaned = ID_CARD_RE.sub(" ", cleaned)
    cleaned = ADDRESS_RE.sub(" ", cleaned)
    cleaned = ALLOWED_RE.sub(" ", cleaned)
    cleaned = SPACE_RE.sub(" ", cleaned).strip()
    return cleaned if len(cleaned) >= min_length else ""
