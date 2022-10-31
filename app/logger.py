from flask import request, current_app
from flask_login import current_user


class Logger:
    @staticmethod
    def print_load_page_log(page: str):
        current_app.logger.debug(
            f"[{request.method}] Load - '{page}' ")

    @staticmethod
    def print_form_error_log(opt: str):
        current_app.logger.warning(
            f"[{request.method}] '{opt}' - Bad form ")

    @staticmethod
    def print_sys_opt_fail_log(opt: str):
        current_app.logger.error(
            f"[{request.method}] System {opt} - fail ")

    @staticmethod
    def print_sys_opt_success_log(opt: str):
        current_app.logger.warning(
            f"[{request.method}] System {opt} - success ")

    @staticmethod
    def print_user_opt_fail_log(opt: str):
        current_app.logger.debug(
            f"[{request.method}] User {opt} - fail ")

    @staticmethod
    def print_user_opt_success_log(opt: str):
        current_app.logger.debug(
            f"[{request.method}] User {opt} - success ")

    @staticmethod
    def print_user_opt_error_log(opt: str):
        current_app.logger.warning(
            f"[{request.method}] User {opt} - system fail ")

    @staticmethod
    def print_import_user_opt_success_log(opt: str):
        current_app.logger.info(
            f"[{request.method}] User {opt} - success ")

    @staticmethod
    def print_user_not_allow_opt_log(opt: str):
        current_app.logger.info(
            f"[{request.method}] User '{opt}' - reject ")