from src import init_app

app = init_app()
app.app_context().push()


if __name__ == '__main__':
    app.run(port=5000)
