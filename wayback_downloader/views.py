from django.http import JsonResponse
from django.conf import settings

def download_site(request):
    """Download archived site using Wayback Machine."""
    # ✅ Delayed import to prevent circular import issues
    from wayback_downloader.wayback_downloader import download_archived_site

    domain = request.GET.get("domain", "")
    if not domain:
        return JsonResponse({"error": "No domain provided"}, status=400)

    download_archived_site(domain)
    return JsonResponse({"message": f"Archived data for {domain} downloaded successfully."})

def domain_analysis_view(request):
    """Analyze domain content for niche changes."""
    from wayback_downloader.wayback_downloader import analyze_domain_changes  # ✅ Delayed import

    domain = request.GET.get("domain", "")
    if not domain:
        return JsonResponse({"error": "Domain parameter is missing."}, status=400)

    API_KEY = getattr(settings, "AHREFS_API_KEY", None)
    if not API_KEY:
        return JsonResponse({"error": "API key is missing in settings."}, status=500)

    result = analyze_domain_changes(domain, API_KEY)

    message = "Yes, the domain has a different niche and content." if result["niche_changed"] else "There is no major change."

    return JsonResponse({"message": message, "data": result})
