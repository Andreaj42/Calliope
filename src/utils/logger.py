from logging import INFO, Logger, basicConfig, getLogger


def setup_logger(level=INFO) -> Logger:
    basicConfig(
        level=level,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return getLogger("Calliope")
