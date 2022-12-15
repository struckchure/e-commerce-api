import abc

from e_commerce.decorators import raise_errors


class Platform(abc.ABC):
    """Abstract base class for platform implementations."""

    @raise_errors()
    @abc.abstractmethod
    def initiate_payment(self, *args, **kwargs):
        """Initiate payment for a user."""
        raise NotImplementedError

    @raise_errors()
    @abc.abstractmethod
    def verify_payment(self, *args, **kwargs):
        """Verify payment for a user."""
        raise NotImplementedError

    @raise_errors()
    @abc.abstractmethod
    def get_payment_status(self, *args, **kwargs):
        """Get payment status for a user."""
        raise NotImplementedError

    @raise_errors()
    @abc.abstractmethod
    def get_payment_details(self, *args, **kwargs):
        """Get payment details for a user."""
        raise NotImplementedError
