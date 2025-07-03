from click.testing import CliRunner
import traceback

from ..main import run


def test_main():
    """Test the main package entry-point."""
    runner = CliRunner()
    result = runner.invoke(run, ["--help"])
    # Fail early and loudly if there was an exception
    if result.exception:
        # Print the full traceback for easier debugging
        traceback.print_exception(type(result.exception), result.exception, result.exception.__traceback__)
        raise result.exception  # Explicitly raise the exception to fail the test
    assert result.exit_code == 0
    assert "Main package entry-point" in result.output
    assert "Options:" in result.output
    assert "Commands:" in result.output
