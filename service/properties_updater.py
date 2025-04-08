import os

from infra.shared.logger import Logger


class PropertiesUpdater:
    def __init__(self):
        self.properties_path = "./system.properties"

    def update_system_properties(self, source_dir, is_mobile):
        patch_properties = {"web": [], "mobile": [], "both": []}

        new_properties = self.read_file(f"{source_dir}/※Systemproperties 추가사항.txt")
        key = None
        for line in new_properties:
            if "※웹" in line:
                key = "web"
                continue
            if "※모" in line:
                key = "mobile"
                continue
            if "모두※" in line:
                key = "both"
                continue
            if line.startswith("#"):
                continue
            if "=" not in line:
                continue

            split = line.split("=")
            patch_properties[key].append([split[0], split[1]])

        old_properties = self.read_file(self.properties_path)

        self.writeProperties(old_properties, patch_properties, "both")
        if not is_mobile:
            self.writeProperties(old_properties, patch_properties, "web")
        if is_mobile:
            self.writeProperties(old_properties, patch_properties, "mobile")

        self.save_file(self.properties_path, old_properties)

    def writeProperties(self, old_properties, patch_properties, type):
        for values in patch_properties[type]:
            updated = False
            for i, line in enumerate(old_properties):
                if line.strip().startswith("#"):
                    continue
                if f"{values[0]}=" in line:
                    Logger().log(f"수정된 설정: {line} -> {values[0]}={values[1]}")
                    old_properties[i] = f"{values[0]}={values[1]}"
                    updated = True
                    continue

            if not updated:
                Logger().log(f"추가된 설정: {values[0]}={values[1]}")
                old_properties.append(f"{values[0]}={values[1]}")

    def read_file(self, file_path):
        if not os.path.exists(file_path):
            Logger().log(f"파일이 존재하지 않습니다: {file_path}")
            raise FileNotFoundError(f"파일이 존재하지 않습니다: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()

        return lines

    def save_file(self, file_path, contents):
        with open(file_path, 'w', encoding='utf-8') as f:
            for line in contents:
                f.write(line + "\n")

    def delete_system_properties(self):
        if os.path.exists(self.properties_path):
            os.remove("./system.properties")
