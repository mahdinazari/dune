from application.app import create_app


app = create_app('application.config.DevelopConfig')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

