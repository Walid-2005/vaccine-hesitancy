from django.test.runner import DiscoverRunner

class NoDbTestRunner(DiscoverRunner):
    """
    A Django test runner that bypasses test database creation and destruction.

    This runner allows tests to run against the existing configured
    `DATABASES['default']` without creating a new test database. It is useful
    when working with read-only databases or when the test environment already
    has the required data.

    Note:
        Use with caution — running tests against a live database may lead to
        unintended data modifications.

    Overrides:
        - setup_databases: Does nothing and returns an empty list.
        - teardown_databases: Does nothing.
    """

    def setup_databases(self, **kwargs):
        """
        Skip test database creation.

        Args:
            **kwargs: Additional keyword arguments (ignored).

        Returns:
            list: An empty list indicating no test databases were set up.
        """
        # Override the default behavior to skip DB creation
        return []

    def teardown_databases(self, old_config, **kwargs):
        """
        Skip test database destruction.

        Args:
            old_config (Any): Previous database configuration (ignored).
            **kwargs: Additional keyword arguments (ignored).
        """
        # Override the default behavior to skip DB teardown
        pass
