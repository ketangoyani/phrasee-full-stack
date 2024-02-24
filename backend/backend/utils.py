from django.contrib.sites.models import Site

def build_absolute_url(path: str) -> str:
    """
    Builds an absolute URL using the current request's host, including
    subdomain if any.
    Appends the given path to the URL.

    :param path: the path to append to the URL
    :return: the absolute URL
    """

    site = Site.objects.get_current()
    domain = site.domain
    protocol = "https"  # by default
    # Modify protocol and domain based on subdomain
    if domain == "example.com":  # We assume you're running locally
        domain = "localhost:8000"
        protocol = "http"
    return f"{protocol}://{domain}/{path}"