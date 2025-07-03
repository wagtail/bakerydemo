import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django management command to show all template paths in the project.
    """
    help = 'Show the current configuration of Viewless'

    def add_arguments(self, parser):
        parser.add_argument(
            '--absolute',
            action='store_true',
            help='Show absolute paths to templates (default is relative to project root)',
        )

    def get_project_root_from_config(self):
        """Validate and return the project root Path from VIEWLESS_CONFIG, or print error and return None."""
        viewless_config = getattr(settings, 'VIEWLESS_CONFIG', None)
        if not viewless_config:
            self.stdout.write(self.style.ERROR('VIEWLESS_CONFIG must be set in your settings.'))
            return None
        project_root = viewless_config.get('PROJECT_ROOT')
        if not isinstance(project_root, str):
            self.stdout.write(self.style.ERROR('PROJECT_ROOT must be set as a string in VIEWLESS_CONFIG.'))
            return None
        return Path(project_root).resolve()

    def get_template_paths(self, project_root: Path, absolute: bool = False):
        """Return a list of template paths (absolute or relative to project_root)."""
        template_paths = []
        for root, dirs, files in os.walk(project_root):
            if os.path.basename(root) == 'templates':
                for dirpath, _, filenames in os.walk(root):
                    for filename in filenames:
                        if filename.endswith('.html'):
                            abs_path = Path(dirpath, filename).resolve()
                            if absolute:
                                template_paths.append(str(abs_path))
                            else:
                                rel_path = abs_path.relative_to(project_root)
                                template_paths.append(str(rel_path))
        return template_paths

    def handle(self, *args, **options):
        """Entrypoint for the management command."""
        project_root = self.get_project_root_from_config()
        if not project_root:
            return
        show_absolute = options.get('absolute', False)
        template_paths = self.get_template_paths(project_root, show_absolute)
        if not template_paths:
            self.stdout.write(self.style.WARNING('No templates found in the project.'))
            return
        self.stdout.write(self.style.SUCCESS(
            f"Templates found (project root: {project_root}):"
        ))
        for path in sorted(template_paths):
            self.stdout.write(path)