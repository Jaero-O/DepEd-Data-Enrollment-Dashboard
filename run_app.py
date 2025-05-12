from main.data_engineer.frontend.main_page import app
from main.data_engineer.frontend.cache_file import cache

cache.clear()
cache.close()
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
