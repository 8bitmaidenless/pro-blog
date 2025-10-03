import os
from pathlib import Path
from random import choice

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''
Configures the project to use the specified "theme" as the preferred CSS stylesheet for use across the project's pages. Must have a "theme.min.css" file for the requested theme located in the "frontend/static/css" directory. If your themes are not showing up there or won't work with this command, ensure that you have used the "make_css" command to run the SASS processor on each of the theme configurations located in the "themes" folder located in the parent folder of the project's BASE DIR folder.'''

    def add_arguments(self, parser):
        theme_path = settings.BASE_DIR / 'frontend/static/css'
        try:
            themes = os.listdir(theme_path)
            themes = [f for f in themes if f.endswith('.css')]
            themes = [t.replace('.min.css', '') for t in themes]
            themes.sort()
            self.theme_choices = themes
        except Exception as err:
            self.theme_choices = []
        parser.add_argument('--theme', dest='theme', type=str, required=False, choices=self.theme_choices)
        parser.add_argument('--random', dest='is_random', action='store_true')

    def handle(self, *args, **options):
        is_random = options.get('is_random', False)
        all_themes = self.theme_choices.copy()
        theme_env = settings.BULMA_THEME_ENV_PATH
        theme_env = Path(theme_env)
        if theme_env.is_dir():
            with open(theme_env, 'r') as file:
                current_theme = file.read().strip().lower()
        else:
            current_theme = 'none'
        theme = options.get('theme', None)
        if is_random or theme is None:
            if current_theme in all_themes:
                all_themes.remove(current_theme)
            theme = choice(all_themes)
        if not theme:
            self.stderr.write(f'\n\n{"-"*48}\nERROR: Could not parse theme name based on the provided args. Please try again and ensure you are passinga valid theme name to the "--theme" arg. Use the "show_themes" command to see valid values to pass to "--theme".')
            return False
        theme = theme.lower()
        all_themes.append(current_theme)
        if theme not in all_themes:
            self.stderr.write(
                f'\n\n{"-"*48}\nERROR: "{theme}" is not a valid theme name. Use "show_themes" to display a list of all of the currently detected theme files are currently in the static CSS folder.'
            )
            return False
        with open(theme_env, 'w') as file:
            self.stdout.write(f'\n\n{"-"*48}\nINFO: Currently writing theme name "{theme}" to the Bulma Theme .env file.\nNOTICE: Never modify this file manually, only use this command to make changes to project theme config.')
            file.write(theme)
            file.write('\n')
        self.stdout.write(
            f'\n\n{"-"*48}\nSUCCESS: The project\'s selected theme has been set from "{current_theme}" to "{theme}". You may refresh your browser in order to see these changes reflect on your site. If a refresh does not update the stylesheet in use, try reloading / restarting the server and / or clearing your browser cache of data for "localhost".'
        )
        return True
    
        