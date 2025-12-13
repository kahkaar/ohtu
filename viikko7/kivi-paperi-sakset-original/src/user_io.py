class UserIO():
    """Class to handle user input and output."""

    def get(self, prompt: object = "", /) -> str:
        """Get input from user, strip whitespace and convert to lowercase."""
        return str(input(prompt)).strip().lower()

    def show(self, *values: object) -> None:
        """Display a message to the user."""
        print(*values)
