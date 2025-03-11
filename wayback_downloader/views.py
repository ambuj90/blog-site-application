from django.http import JsonResponse
from .wayback_downloader import download_archived_site

def download_site(request):
    domain = request.GET.get("domain", "")
    if not domain:
        return JsonResponse({"error": "No domain provided"}, status=400)

    download_archived_site(domain)
    return JsonResponse({"message": f"Archived data for {domain} downloaded successfully."})
