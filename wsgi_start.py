from app import create_app
from app.utils.file_utils import cleanup

app = create_app()

if __name__ == "__main__":
    cleanup()
    app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False, threaded=True)
