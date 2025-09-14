from django.core.management.base import BaseCommand
from outages.models import Community
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Command(BaseCommand):
    help = 'Triggers a test power outage notification.'

    def add_arguments(self, parser):
        parser.add_argument('community_id', type=int, help='The ID of the community to update.')
        parser.add_argument('status', type=str, help='The new power status (on/off).')

    def handle(self, *args, **options):
        community_id = options['community_id']
        status = options['status'].lower()

        try:
            community = Community.objects.get(pk=community_id)
        except Community.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Community with ID {community_id} does not exist.'))
            return

        if status == 'on':
            community.power_status = True
        elif status == 'off':
            community.power_status = False
        else:
            self.stdout.write(self.style.ERROR('Invalid status. Please use "on" or "off".'))
            return

        community.save()

        channel_layer = get_channel_layer()
        message = f'Power status for {community.name} has been updated to {status.upper()}.'

        async_to_sync(channel_layer.group_send)(
            'outages',
            {
                'type': 'outage_notification',
                'message': message
            }
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully triggered outage for {community.name}.'))
