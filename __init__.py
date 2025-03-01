"""
This module initializes and sets up the containers plugin for CTFd.
"""

from flask import Flask
from flask.blueprints import Blueprint

from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.challenges import CHALLENGE_CLASSES

from .container_challenge import ContainerChallenge
from .setup import setup_default_configs
from .routes import register_app
from .logs import init_logs

def load(app: Flask) -> None:
    """
    Initialize and set up the containers plugin for CTFd.
    """
    app.config['RESTX_ERROR_404_HELP'] = False
    
    # Create tables with checking if they exist
    with app.app_context():
        if not app.db.engine.dialect.has_table(app.db.engine, "container_challenge_model"):
            app.db.create_all()
        if not app.db.engine.dialect.has_table(app.db.engine, "container_info_model"):
            app.db.create_all()
        if not app.db.engine.dialect.has_table(app.db.engine, "container_settings_model"):
            app.db.create_all()
            
    setup_default_configs()
    CHALLENGE_CLASSES["container"] = ContainerChallenge
    register_plugin_assets_directory(app, base_path="/plugins/containers/assets/")

    # Initialize logging for this plugin
    init_logs(app)

    # Get the blueprint from register_app and register it here
    containers_bp: Blueprint = register_app(app)
    app.register_blueprint(containers_bp)
