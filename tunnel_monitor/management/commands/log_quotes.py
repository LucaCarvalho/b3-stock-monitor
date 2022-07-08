from django.core.management.base import BaseCommand, CommandError
from tunnel_monitor.utils.ticker import log_quotes

class Command(BaseCommand):
    help = "Logs the current price of all active tunnels"

    def add_arguments(self, parser):
        parser.add_argument("--interval", type=int)

    def handle(self, *args, **options):
        if options['interval']:
            self.stdout.write(f"Logging quotes for all tunnels with interval={options['interval']}")
            log_quotes(options["interval"])
        else:
            self.stderr.write("You must specify an interval with --interval")

    