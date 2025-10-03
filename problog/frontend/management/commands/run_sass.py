import os
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''Runs the SASS preprocessor on any specified (or all) of the detected SASS configurations located in the "themes" folder. The generated (and minified) CSS asset for each processed SASS theme will be written to the "frontend/static/css" folder, it should be named the same as it was found in the "themes" folder, with a ".min.css" file extension. Use --theme to specify a specfic theme to process, --missing to only run it on themes who aren't already in the static CSS folder, and --make-all to run SASS on every theme in the "themes" directory even if it has already been processed before.'''

    def add_arguments(self, parser):
        parent_dir = settings.BASE_DIR.absolute().parent
        theme_dir = parent_dir / 'themes'
        try:
            theme_list = os.listdir(theme_dir)
            theme_path_list = [theme_dir / path for path in theme_list]
            theme_list = [f.stem for f in theme_path_list if f.is_dir()]
            theme_list.sort()
            self.theme_choices = theme_list
            self.theme_dir = theme_dir
        except:
            self.theme_choices = []
            self.theme_dir = None
        parser.add_argument(
            '--theme',
            dest='theme',
            required=False,
            type=str,
            choices=self.theme_choices,
        )
        parser.add_argument(
            '--missing',
            dest='missing_only',
            type=bool,
            action='store_true'
        )
        parser.add_argument(
            '--make-all',
            dest='make_all',
            type=bool,
            action='store_true'
        )

    def handle(self, *args, **options):
        theme = options.get('theme', None)
        missing = options.get('missing_only', False)
        make_all = options.get('make_all', False)
        target_themes = []
        if not (make_all or missing):
            if not theme:
                self.stderr.write(f'\n\n{"-"*48}\nERROR: Missing required argument: "--theme". You must provide a theme name if not using the --missing or --make-all flags!')
                return False
            target_themes.append(theme)
            css_files = os.listdir(self.theme_dir)
            css_files = [css.replace('.min.css', '') for css in css_files]
            if theme in css_files:
                existing = 1
        else:
            if missing:
                target_themes = self.theme_choices
                css_files = os.listdir(self.theme_dir)
                for css in css_files:
                    name = css.replace('.min.css', '')
                    if name in target_themes:
                        target_themes.remove(name)
                existing = 0
            else:
                target_themes = self.theme_choices
                existing = 0
                for t in target_themes:
                    css_files = os.listdir(self.theme_dir)
                    css_files = [css.replace('.min.css', '') for css in css_files]
                    if t in css_files:
                        existing += 1
        self.stdout.write(f'\n\n{"-"*48}\nINFO: Preparing to run SASS processor on {len(target_themes)} SASS themes.\n{existing} of the target theme configs already have a corresponding ".min.css" asset located in the static CSS folder. Next time to omit these existing themes from this command, use the --missing flag.')
        target_themes = [
            self.theme_dir / target
            for target in target_themes
        ]
        target_themes = [target for target in target_themes if target.is_dir()]
        failures = 0
        finished = []
        for th in target_themes:
            scss_path = target / 'theme.scss'
            if not scss_path.exists():
                self.stderr.write(f'\n\n{"-"*48}\nERROR: The "theme.scss" file is missing for the theme: "{th}". Please ensure the necessary SCSS resources are located in each theme\'s folder, otherwise this command will fail on it.')
                self.stdout.write(f'\n\n{"-"*48}\nSkipping "{th}" and continuing to next target in list.')
                failures += 1
                continue
            out_path = settings.BASE_DIR / 'frontend/static/css'
            if not out_path.is_dir():
                self.stderr.write(f'\n\n{"-"*48}\nERROR: The output destination for Bulma themes should be located at "{out_path}", but it cannot be located at this time. Please ensure that the folder exists at the specified path and is spelled correctly.\nCannot continue without valid output destination, aborting...')
                return False
            outfile = f'{th.stem}.min.css'
            out_path = out_path / outfile
            command = f'sass --no-source-map --style=compressed {scss_path.as_posix()} {out_path.as_posix()}'
            try:
                subprocess.call(
                    command,
                    shell=True,
                    stderr=subprocess.STDOUT,
                    cwd=Path('.').absolute().parent
                )
            except Exception as err:
                self.stderr.write(f'\n\n{"-"*48}\nERROR: The following error was caught while trying to process theme "th":\n{err}')
                failures += 1
                self.stdout.write(f'\n\n{"-"*48}\nSkipping "{th}" and continuing to next target in list.')
                continue
            css_path = Path(f'frontend/static/css/{th.stem}.min.css')
            if not css_path.exists():
                self.stderr.write(f'\n\n{"-"*48}\nERROR: Command executed for theme "{th}" without error, but cannot find corresponding ".css" asset from output. Try again with a different theme, if that does not work, try running the SASS command manually and seeing if that illuminates the cause of the issue.')
                self.stderr.write(f'\n\nSASS Command: "{command}"\nRun the above command in the parent dir of the project and see if it works or throws a specific error.')
                failures += 1
                continue
            self.stdout.write(f'Successfully made CSS stylesheet from SASS configuration: "{th.stem}".\nYou may now use the "set_theme" command to enable this theme for this project.')
            finished.append(th)
        self.stdout.write(f'\n\n{"-"*48}\nSUCCESS: Finished processing {len(finished)} themes into usable CSS files. Encountered {failures} failures along the way. You will need to ensure the failed themes are configured correctly in their SASS resources. If that does not correct the issue, try manually running SASS on the failed theme and taking note of any specific errors thrown or issues encountered.')
        return True
