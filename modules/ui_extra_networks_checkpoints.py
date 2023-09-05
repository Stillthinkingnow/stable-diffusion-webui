import html
import os

from modules import shared, ui_extra_networks, sd_models
from modules.ui_extra_networks import quote_js
from modules.ui_extra_networks_checkpoints_user_metadata import CheckpointUserMetadataEditor


class ExtraNetworksPageCheckpoints(ui_extra_networks.ExtraNetworksPage):
    def __init__(self):
        super().__init__('Checkpoints')

    def refresh(self):
        shared.refresh_checkpoints()

    def create_item(self, name, index=None, enable_filter=True):
        aliases = sd_models.checkpoint_aliases_prev if sd_models.checkpoint_aliases_prev is not None else sd_models.checkpoint_aliases
        checkpoint: sd_models.CheckpointInfo = aliases.get(name)
        if checkpoint is None:
            return None
        path, ext = os.path.splitext(checkpoint.filename)
        return {
            "name": checkpoint.name_for_extra,
            "filename": checkpoint.filename,
            "shorthash": checkpoint.shorthash,
            "preview": self.find_preview(path),
            "description": self.find_description(path),
            "search_term": self.search_terms_from_path(checkpoint.filename) + " " + (checkpoint.sha256 or ""),
            "onclick": '"' + html.escape(f"""return selectCheckpoint({quote_js(name)})""") + '"',
            "local_preview": f"{path}.{shared.opts.samples_format}",
            "metadata": checkpoint.metadata,
            "sort_keys": {'default': index, **self.get_sort_keys(checkpoint.filename)},
        }

    def list_items(self):
        names = sd_models.checkpoints_list_prev if sd_models.checkpoints_list_prev is not None else sd_models.checkpoints_list.copy()
        for index, name in enumerate(names):
            item = self.create_item(name, index)
            if item is not None:
                yield item

    def allowed_directories_for_previews(self):
        return [v for v in [shared.cmd_opts.ckpt_dir, sd_models.model_path] if v is not None]

    def create_user_metadata_editor(self, ui, tabname):
        return CheckpointUserMetadataEditor(ui, tabname, self)
