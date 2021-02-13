from pathlib import Path

import i18n

translations_folder = Path(__file__).parent.with_name("db") / "translations"
i18n.load_path.append(translations_folder.as_posix())
i18n.set("error_on_missing_translation", True)
