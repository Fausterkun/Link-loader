import json
from urllib.parse import urlparse, parse_qs
from linker_app.service.exceptions import UrlValidationError


def parse_url(link: str) -> dict:
    """parse str url and serialize it to dict object"""
    try:
        parsed_link = urlparse(link)
        protocol = parsed_link.scheme
        path = parsed_link.path
        domain_with_zone = parsed_link.netloc
        domain, domain_zone = domain_with_zone.rsplit(".", 1)
        params = parse_qs(parsed_link.query)
        parsed = {
            "url": link,
            "protocol": protocol,
            "path": path,
            "domain": domain,
            "domain_zone": domain_zone,
            "params": json.dumps(params),
        }
    except ValueError:
        raise UrlValidationError("Value not a link.")

    return parsed
