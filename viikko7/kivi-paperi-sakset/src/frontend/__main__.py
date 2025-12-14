import errno
import socket

from .app import create_app


def _is_port_free(host: str, port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((host, port))
        return True
    except OSError as e:
        if e.errno in (errno.EADDRINUSE, 48, 98):
            return False
        raise
    finally:
        sock.close()


def _pick_port(host: str, start_port: int, max_tries: int) -> int:
    for port in range(start_port, start_port + max_tries):
        if _is_port_free(host, port):
            return port
    raise RuntimeError(
        f"No free port found in range {start_port}..{start_port + max_tries - 1}"
    )


def main() -> None:
    app = create_app()
    host = "127.0.0.1"
    default_port = 5000
    port = _pick_port(host=host, start_port=default_port, max_tries=20)
    if port != default_port:
        print(f"Port {default_port} is in use; switching to {port}.")
    print(f"Starting server on http://{host}:{port}")

    # When debug=True, Flask enables the reloader by default. The reloader runs the
    # application twice (parent + child), which breaks dynamic port selection and
    # leads to confusing logs. Disable it to ensure the chosen port is the port used.
    app.run(debug=True, host=host, port=port, use_reloader=False)


if __name__ == "__main__":
    main()
