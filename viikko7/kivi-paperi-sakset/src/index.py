from kps_app import KPSApp
from user_io import UserIO


def main():
    io = UserIO()
    app = KPSApp(io)

    try:
        app.run()
    except ValueError as e:
        # Handle value errors gracefully
        io.show(f"An error occured while running the application: {e}")


if __name__ == "__main__":
    main()
