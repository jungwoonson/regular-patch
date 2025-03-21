from service.config_reader import ConfigReader
from service.patch_manager import PatchManager
from ui.view import PatchGUI


def main():
    config_reader = ConfigReader("./config.json")
    config_list = config_reader.read_config()

    patch_manager = PatchManager()
    gui = PatchGUI(set_source_callback=patch_manager.set_source_dir)

    commands = {
        "send_list_import": patch_manager.send_patch_list_import,
        "start_db_patch": patch_manager.start_db_patch,
        "check_server_process": patch_manager.check_server_process,
        "start_server": patch_manager.start_server,
        "stop_server": patch_manager.stop_server,
        "start_server_log": patch_manager.start_server_log,
        "stop_server_log": patch_manager.stop_server_log,
        "deploy_properties": patch_manager.deploy_properties,
        "send_webroot": patch_manager.send_webroot,
        "send_classes": patch_manager.send_classes,
    }

    gui.create_config_buttons(config_list)
    gui.init_action_buttons(config_list, commands)
    gui.run()


if __name__ == "__main__":
    main()
