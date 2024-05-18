import logging,os,datetime

class Log:
    log_dir = 'Files\logs'
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H-%M-%S'

    @classmethod
    def log_info(cls, logger:str, message:str) -> None:
        os.makedirs(cls.log_dir, exist_ok=True)
        logging.basicConfig(filename=os.path.join(cls.log_dir, f"{datetime.datetime.now().strftime(cls.date_format)}_log.log"),
                    filemode='w', format=cls.log_format, level=logging.INFO)
        logger = logging.getLogger(logger)
        logger.info(message)