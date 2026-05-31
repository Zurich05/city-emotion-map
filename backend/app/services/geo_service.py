import re


def infer_geo(record: dict) -> dict:
    location = record.get("raw_location") or ""
    city = record.get("city") or ("武汉市" if "武汉" in location else None)
    district = record.get("district")
    if not district:
        match = re.search(r"([\u4e00-\u9fa5]{2,4}区)", location)
        district = match.group(1) if match else None
    return {
        "city": city,
        "district": district,
        "location_name": record.get("location_name"),
        "lat": record.get("lat"),
        "lng": record.get("lng"),
    }
