from cyberfusion.WordPressSupport.exceptions import CommandFailedError


def test_CommandFailedError_streams():
    STDOUT = "stdout"
    STDERR = "stderr"

    exception = CommandFailedError(
        command=["foobar"], return_code=1, stdout=STDOUT, stderr=STDERR
    )

    assert (
        exception.streams
        == f"Stdout:\n\n{exception.stdout}\n\nStderr:\n\n{exception.stderr}"
    )


def test_CommandFailedError_string():
    exception = CommandFailedError(
        command=["foobar"], return_code=1, stdout="stdout", stderr="stderr"
    )

    assert str(exception) == exception.streams
