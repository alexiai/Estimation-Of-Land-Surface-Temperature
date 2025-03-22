from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/run-lst', methods=['POST'])
def run_lst():
    data = request.json
    coordinates = data['coordinates']
    start_date = data['startDate']
    end_date = data['endDate']
    cloud_percentage = data['cloudPercentage']

    # Here you can pass the input to your gee.py script and run it
    try:
        # Example: Running gee.py with subprocess
        result = subprocess.run(['python3', 'gge.py'], capture_output=True, text=True)
        return jsonify({
            'message': 'LST calculation completed successfully!',
            'output': result.stdout
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)