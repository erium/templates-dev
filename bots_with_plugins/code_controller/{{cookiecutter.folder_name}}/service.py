from flask import Flask, request, jsonify
import os
import re
import subprocess
from subprocess import PIPE, STDOUT
from ipykernel.kernelapp import IPKernelApp
import asyncio

app = Flask(__name__)


class MyIPKernelApp(IPKernelApp):
    def init_signal(self):
        pass


@app.route('/start_kernel', methods=['POST'])
def start_kernel():
    """
    Starts the IPython kernel.

    Returns:
        dict: A dictionary containing the result status of the request (success or error).
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        kernel = MyIPKernelApp.instance()
        kernel.initialize([])
        return jsonify({'success': 'Kernel started! '}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/stop_kernel', methods=['POST'])
def stop_kernel():
    """
    Stops the IPython kernel.

    Returns:
        tuple: A tuple containing the result of the request and the status code.
    """
    try:
        kernel = IPKernelApp.instance()
        kernel.close()
        return jsonify({'success': 'Kernel stopped! '}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/execute_kernel_command', methods=['POST'])
def execute_kernel_command():
    """
    Executes a command in a running IPython kernel.

    Args:
        command (str): the shell command that should be run in the IPython Kernel (e.g.: ls)

    Returns:
        tuple: A tuple containing the result of the command and the status code.
    """
    try:
        data = request.get_json()
        if 'command' in data:
            command = data['command']
            kernel = IPKernelApp.instance()
            result = kernel.shell.run_cell(command)
            return jsonify({'output': str(result.result)}), 200
        else:
            return jsonify({'error': 'No command provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/alive', methods=['POST'])
def alive():
    """
    Returns a simple "Hello World!" message to see if the service is running.

    Returns:
        tuple: A tuple containing the message and the status code.
    """
    return 'Hello World!', 200


@app.route('/execute_command', methods=['POST'])
def execute_command():
    """
    Executes a command in the shell (i.e. bash).

    Args:
        command (str): the shell command (e.g.: ls).

    Returns:
        tuple: A tuple containing the result of the command and the status code.
    """
    try:
        data = request.get_json()
        if 'command' in data:
            command = data['command']
            result = subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT, text=True)
            return jsonify({'output': result.strip()}), 200
        else:
            return jsonify({'error': 'No command provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/apt_get_install', methods=['POST'])
def apt_get_install():
    """
    Downloads and installs a package via the advanced package tool.

    Args:
        package (str): the package that should be installed.

    Returns:
        tuple: A tuple containing the result of the command and the status code.
    """
    try:
        data = request.get_json()
        if 'package' in data:
            package = data['package']
            
            update = ['sudo', 'apg-get', 'update']
            subprocess.Popen(update, stdout=PIPE, stderr=PIPE)

            command = ['sudo', 'apt-get', 'install', '-y', '-qq']
            command.append(package)
            result = subprocess.Popen(
                command, stdout=PIPE, stderr=PIPE)
            result.wait()
            exit_code = result.returncode
            if exit_code != 0:
                output = result.stderr.read().decode()
            else:
                output = "success"
            return jsonify({'output': output}), 200
        else:
            return jsonify({'error': 'No command provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/write_to_file', methods=['POST'])
def write_to_file():
    """
    Creates a file and writes the given contents to it.

    Args:
        contents (any): the contents of the file (e.g. "Hey there! This will be a text file").
        filename (str): the filename of the file without the fileextension (e.g.: hello_world).
        filetype (str): the filetype of the file (e.g.: txt).

    Returns:
        tuple: A tuple containing the result of the command and the status code.
    """
    try:
        data = request.get_json()
        if 'contents' in data and 'filetype' in data and 'filename' in data:
            with open(f"{data['filename']}.{data['filetype']}", 'w') as f:
                f.write(data['contents'])
            return jsonify({'output': f'Successfully wrote contents to file {data["filename"]}.{data["filetype"]}!'})
        else:
            return jsonify({'error': 'Missing parameters'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_apps_url', methods=['POST'])
def get_apps_url():
    """
    Returns the URL of Apps running from Halerium.

    Returns:
        tuple: A tuple containing the URL and the status code.
    """
    try:
        url = subprocess.check_output(
            'get_apps_url.sh', shell=True, stderr=subprocess.STDOUT)
        url = url.decode('utf-8')
        regex_full_url = re.search('^(.*?)<', url)
        clean_url = regex_full_url.group(1)
        port = 8501
        return clean_url + str(port), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500


@app.route('/start_streamlit_app', methods=['POST'])
def start_streamlit_app():
    """
    Starts a Streamlit app.

    Args:
        filename (str): the filename of the streamlit app (for example: "app.py").

    Returns:
        tuple: A tuple containing the result of the command and the status code.
    """
    try:
        data = request.get_json()
        if 'filename' in data:
            filename = data['filename']
            if os.path.exists(filename):
                subprocess.Popen(["python", "-m" "streamlit", "run",
                                 filename], stderr=subprocess.STDOUT, text=True)
                port = 8501
                runner_id = os.getenv('HALERIUM_ID')
                base_url = os.getenv('HALERIUM_BASE_URL')
                app_url = base_url + "/apps/" + runner_id + "/" + str(port)
                return jsonify({'success': f'Streamlit app is running! You can use it at {app_url}'}), 200
            else:
                return jsonify({'error': f'File not found: {filename}.'}), 400
        else:
            return jsonify({'error': 'No filename provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8498)
