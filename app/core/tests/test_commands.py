# Test custom django management commands

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

# Command that we'll be mocking to simulate response
# Adding a patch here will add a new argument to methods
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    # Test commands
    def test_wait_for_db_ready(self, patched_check):
        # Test waiting for database if database ready
        # When check is called, we want to make sure it returns a value
        patched_check.return_value = True
        call_command('wait_for_db')

        # Ensures that mocked method is called with mock params
        patched_check.assert_called_once_with(databases=['default'])

    # Test what happens if db isn't ready yet
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        # Test waiting for DB when getting operational error
        # We make it raise an exception using side_effect.
        # Allows us to define various values that happen each time we call it in the order we call it.
        # First two times we call mocked method we want it to raise the Psycopg2 error
        # Then, we raise 3 operational errors
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
