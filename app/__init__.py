from flask import Flask, render_template, Response, request
from flask.logging import default_handler
import logging
import logging.handlers
import os
import sys

from config import conf
from .logger import Logger
from .login import login


if conf["DEBUG_PROFILE"]:
    from werkzeug.middleware.profiler import ProfilerMiddleware


class ClashFlask(Flask):
    def __init__(self, import_name):
        super(ClashFlask, self).__init__(import_name)
        self.update_configure()
        self.profile_setting()
        self.logging_setting()
        self.blueprint()

        login.init_app(self)

        @self.context_processor
        def inject_base():
            """ app默认模板变量 """
            return {"conf": conf,
                    "get_icp": self.get_icp}

    @staticmethod
    def get_icp():
        for i in conf["ICP"]:
            if i in request.host:
                return conf["ICP"][i]

    def blueprint(self):
        from .index import index
        self.register_blueprint(index, url_prefix="/")

        from .auth import auth
        self.register_blueprint(auth, url_prefix="/auth")

        from .clash import clash
        self.register_blueprint(clash, url_prefix="/clash")


    def profile_setting(self):
        if conf["DEBUG_PROFILE"]:
            self.wsgi_app = ProfilerMiddleware(self.wsgi_app, sort_by=("cumtime",))

    def logging_setting(self):
        self.logger.removeHandler(default_handler)
        self.logger.setLevel(conf["LOG_LEVEL"])
        self.logger.propagate = False  # 不传递给更高级别的处理器处理日志

        if len(conf["LOG_HOME"]) > 0:
            handle = logging.handlers.TimedRotatingFileHandler(
                os.path.join(conf["LOG_HOME"], f"flask.log"), backupCount=10)
            handle.setFormatter(logging.Formatter(conf["LOG_FORMAT"]))
            self.logger.addHandler(handle)

        if conf["LOG_STDERR"]:
            handle = logging.StreamHandler(sys.stderr)
            handle.setFormatter(logging.Formatter(conf["LOG_FORMAT"]))
            self.logger.addHandler(handle)

    def update_configure(self):
        """ 更新配置 """
        self.config.update(conf)
