import os
import warnings
from pathlib import Path

import hydra
import pytorch_lightning as pl
import torch
from hydra.utils import get_original_cwd
from omegaconf import DictConfig, OmegaConf
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint

from dl4cv.utils.technical_utils import load_obj
from dl4cv.utils.utils import save_useful_info, set_seed

warnings.filterwarnings("ignore")


def run(cfg: DictConfig) -> None:
    """
    Run pytorch-lightning model

    Args:
        new_dir:
        cfg: hydra config

    """
    set_seed(cfg.training.seed)
    run_name = os.path.basename(os.getcwd())
    cfg.callbacks.model_checkpoint.params.dirpath = Path(
        os.getcwd(), cfg.callbacks.model_checkpoint.params.dirpath
    ).as_posix()
    callbacks = []
    for callback in cfg.callbacks.other_callbacks:
        if callback.params:
            callback_instance = load_obj(callback.class_name)(**callback.params)
        else:
            callback_instance = load_obj(callback.class_name)()
        callbacks.append(callback_instance)

    loggers = []
    if cfg.logging.log:
        for logger in cfg.logging.loggers:
            if "experiment_name" in logger.params.keys():
                logger.params["experiment_name"] = run_name
            loggers.append(load_obj(logger.class_name)(**logger.params))

    callbacks.append(EarlyStopping(**cfg.callbacks.early_stopping.params))
    callbacks.append(ModelCheckpoint(**cfg.callbacks.model_checkpoint.params))

    trainer = pl.Trainer(
        logger=loggers,
        callbacks=callbacks,
        **cfg.trainer,
    )

    dm = load_obj(cfg.datamodule.datamodule_name)(cfg=cfg)
    dm.setup()

    model = load_obj(cfg.training.lightning_module_name)(cfg=cfg)
    trainer.fit(model, dm)

    if cfg.general.save_pytorch_model:
        os.makedirs("saved_models", exist_ok=True)
        if cfg.general.save_best:
            best_path = trainer.checkpoint_callback.best_model_path  # type: ignore
            # extract file name without folder
            save_name = os.path.basename(os.path.normpath(best_path))
            model = model.load_from_checkpoint(best_path, cfg=cfg, strict=False)
            model_name = Path(
                cfg.callbacks.model_checkpoint.params.dirpath,
                f"best_{save_name}".replace(".ckpt", ".pth"),
            ).as_posix()
            torch.save(model.model.state_dict(), model_name)
        else:
            model_name = "saved_models/last.pth"
            torch.save(model.model.state_dict(), model_name)

    if cfg.general.predict:
        trainer.test(model, datamodule=dm, ckpt_path="best")


@hydra.main(config_path="../configs", config_name="config_training")
def run_model(cfg: DictConfig) -> None:
    os.makedirs("logs", exist_ok=True)
    print(OmegaConf.to_yaml(cfg))
    if cfg.general.log_code:
        save_useful_info(os.path.basename(__file__))
    run(cfg)


if __name__ == "__main__":
    run_model()
