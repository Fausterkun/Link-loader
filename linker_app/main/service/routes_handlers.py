import dataclasses

from urllib.parse import urlparse, parse_qs


class ValidationError(ValueError):
    pass


@dataclasses.dataclass
class FetchResponse:
    errors: dict
    result: dict


@dataclasses.dataclass
class Link:
    protocol: str
    domain: str
    zone: str
    params: dict


def handle_link(link: str):
    print("handle link", link)
    # parse link
    # try:
    parsed_link = urlparse(link)
    print(parsed_link)
    protocol = parsed_link.scheme
    print("protocol:", protocol)
    domain_with_zone = parsed_link.path
    print("dom with zone:", domain_with_zone)
    domain, domain_zone = domain_with_zone.rsplit(".", 1)
    params = parse_qs(parsed_link.query)
    fragment = parsed_link.fragment
    # if fields are empty, assume that this one isn't link at all
    # if not protocol and not domain_with_zone:
    #     raise ValidationError("Invalid link format")
    response = FetchResponse(
        result={
            "protocol": protocol,
            "domain_with_zone": domain_with_zone,
            "domain": domain,
            "domain_zone": domain_zone,
            "params": params,
            "fragment": fragment,
        },
        errors={},
    )
    # except ValueError as e:
    #     print(e, e.args)
    #     response = FetchResponse(result={}, errors={'Validation Error': "Invalid link format."})
    print("Max here")
    return response


# save to db


# see if any errors
# save to db if no errors
# else return to user
