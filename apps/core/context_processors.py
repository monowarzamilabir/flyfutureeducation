from .models import SiteSettings


def site_settings(request):
    """Makes the singleton SiteSettings available in every template as `site_settings`."""
    return {"site_settings": SiteSettings.load()}
