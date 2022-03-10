from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    # Return UI
    return 'Hello World!'


# /status
@app.route('/status', methods=['get'])
def get_status():
    return


@app.route('/status/reset', methods=['post'])
def reset_cambot():
    return


@app.route('/status/snapshot', methods=['get'])
def make_single_snapshot():
    return


# /config
@app.route('/config', methods=['post'])
def create_config():
    return


@app.route('/config', methods=['get'])
def get_all_configs():
    return


@app.route('/config/<string:config_name>', methods=['get'])
def get_config_settings(config_name):
    return


@app.route('/config/<string:config_name>', methods=['delete'])
def delete_config(config_name):
    return


# /inventory
@app.route('/inventory', methods=['post'])
def create_inventory_item():
    return


@app.route('/inventory', methods=['get'])
def get_whole_inventory():
    return


@app.route('/inventory/<string:id_tag>', methods=['get'])
def get_metadata_of_inventory():
    return


@app.route('/inventory/<string:id_tag>', methods=['delete'])
def delete_item():
    return


@app.route('/inventory/<string:id_tag>/zip', methods=['get'])
def get_zip_of_item():
    return


@app.route('/inventory/<string:id_tag>', methods=['put'])
def trigger_single_event():
    return


@app.route('/inventory/<string:id_tag>/snapshot/<string:id_tag>', methods=['get'])
def get_metadata_of_snapshot():
    return


if __name__ == '__main__':
    app.run()
