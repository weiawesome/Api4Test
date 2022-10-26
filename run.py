from App import app

@app.route('/')
def index():
    return 'Flask API started'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=587, debug=False)
