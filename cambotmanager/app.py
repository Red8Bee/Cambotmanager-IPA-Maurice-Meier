import flask
from flask import Flask, request
from robot_manager.manager import Manager
import json

app = Flask(__name__)
manager = Manager()


@app.route('/')
def hello_world():  # put application's code here
    # Return UI
    return 'Hello World!'


# /status
@app.route('/status', methods=['get'])
def get_status():
    status = manager.get_status()
    response = app.response_class(
        response=json.dumps(status),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/status/reset', methods=['post'])
def reset_cambot():
    manager.reset_cambot()
    status = manager.get_status()
    response = app.response_class(
        response=status.toJSON(),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/status/snapshot', methods=['get'])
def make_single_snapshot():
    return


# /config
@app.route('/config', methods=['post'])
def create_config():
    args = request.headers
    config_str = args.get('object')
    config_json = json.loads(config_str)
    created = manager.create_config(config_json)
    if created:
        response = app.response_class(
            response="Created",
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response="Duplicate name",
            status=401,
            mimetype='application/json'
        )
    return response


@app.route('/config', methods=['get'])
def get_all_configs():
    configs = manager.get_all_configs()
    response = app.response_class(
        response=json.dumps(configs),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/config/<string:config_name>', methods=['get'])
def get_config_settings(config_name):
    config = manager.get_config(config_name)
    if config is None:
        response = app.response_class(
            response='config not found',
            status=404,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=config.toJSON(),
            status=200,
            mimetype='application/json'
        )
    return response


@app.route('/config/<string:config_name>', methods=['delete'])
def delete_config(config_name):
    config = manager.delete_config(config_name)
    if config is None:
        response = app.response_class(
            response="config not found",
            status=404,
            mimetype='application/json'
        )
    elif config.is_in_use:
        response = app.response_class(
            response="config in use",
            status=403,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response="deleted",
            status=200,
            mimetype='application/json'
        )
    return response


# /inventory
@app.route('/inventory', methods=['post'])
def create_inventory_item():
    args = request.args
    config_id = args.get("config", type=str)
    id_tag = args.get("id", type=str)
    config = manager.get_config(config_id)
    if config is not None:
        config.is_in_use = True
        created = manager.create_inventory_item(config, id_tag)
        if created:
            response = app.response_class(
                response="item created",
                status=201,
                mimetype='application/json'
            )
        else:
            response = app.response_class(
                response="internal server error",
                status=500,
                mimetype='application/json'
            )
    else:
        response = app.response_class(
            response="bad input parameter",
            status=400,
            mimetype='application/json'
        )
    return response


@app.route('/inventory', methods=['get'])
def get_whole_inventory():
    args = request.args
    storage_status = args.get('storageStatus', type=str)
    status = args.get('status', type=str)
    inventory = manager.get_whole_inventory(status, storage_status)
    if inventory is None:
        response = app.response_class(
            response="bad input parameter",
            status=400,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps(inventory),
            status=200,
            mimetype='application/json'
        )
    return response


@app.route('/inventory/<string:id_tag>', methods=['get'])
def get_metadata_of_inventory(id_tag):
    inventory_item = manager.get_inventory_item(id_tag)
    if inventory_item is None:
        response = app.response_class(
            response="Inventory ID not found",
            status=401,
            mimetype='application/json'
        )
    elif inventory_item == "id_invalid":
        response = app.response_class(
            response='bad input parameter',
            status=400,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=inventory_item.toJSON(),
            status=200,
            mimetype='application/json'
        )
    return response


@app.route('/inventory/<string:id_tag>', methods=['delete'])
def delete_item(id_tag):
    inventory_item = manager.delete_inventory_item(id_tag)
    if inventory_item is None:
        response = app.response_class(
            response="Inventory ID not found",
            status=401,
            mimetype='application/json'
        )
    elif inventory_item == "id_invalid":
        response = app.response_class(
            response='bad input parameter',
            status=400,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response='item deleted',
            status=200,
            mimetype='application/json'
        )
    return response


@app.route('/inventory/<string:id_tag>/zip', methods=['get'])
def get_zip_of_item(id_tag):
    zip = manager.create_zip_from_item(id_tag)
    if zip is not None:
        response = flask.send_file(zip, mimetype='application/zip', as_attachment=True,
                                   attachment_filename="cambot_item_" + id_tag + ".zip")
    else:
        response = app.response_class(
            response='Item not found',
            status=404,
            mimetype='application/json'
        )
    return response


@app.route('/inventory/<string:id_tag>', methods=['put'])
def trigger_single_event(id_tag):
    return


@app.route('/inventory/<string:id_tag>/snapshot/<string:snapshot_time>', methods=['get'])
def get_metadata_of_snapshot(id_tag, snapshot_time):
    snapshot = manager.get_snapshot_from_item(id_tag, snapshot_time)
    if snapshot == "id_invalid":
        response = app.response_class(
            response='bad input parameter',
            status=400,
            mimetype='application/json'
        )
    elif snapshot is None:
        response = app.response_class(
            response="Inventory ID not found",
            status=401,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=snapshot.toJSON,
            status=200,
            mimetype='application/json'
        )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
