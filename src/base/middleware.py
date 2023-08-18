from src.tinymce_editor.patched_external_link import patched_external_link


class ExternalLinkRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/admin/choose-external-link/':
            return patched_external_link(request)
        else:
            response = self.get_response(request)
            return response
