import logging,os

class Log:
    log_dir = 'Logs'
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H-%M-%S'

    def log(self, name:str, message:str, log_level:str='DEBUG', file_name:str='log', file_mode:str='a') -> None:
        os.makedirs(self.log_dir, exist_ok=True)
        logging.basicConfig(filename=os.path.join(self.log_dir, f"{file_name}.log"),filemode=file_mode, format=self.log_format)
        logger = logging.getLogger(name)
        if log_level=="DEBUG":
            logger.setLevel(logging.DEBUG)
            logger.debug(message)
        elif log_level=="INFO":
            logger.setLevel(logging.INFO)
            logger.info(message)
        elif log_level=="ERROR":
            logger.setLevel(logging.ERROR)
            logger.error(message)

###############################################
l1=Log()
# l1.log('deposit',f'{600} deposited','INFO','transaction','a')        
# l1.log('deposit',f'{600} deposited','DEBUG')   



# l1.log('withdraw',f'{6500} withdrawed','INFO','transaction','a')        
# l1.log('withdraw',f'{6500} withdrawed','DEBUG')      



l1.log('transfer',f'{700} transfered','INFO','transaction','a')        
l1.log('transfer',f'{700} transfered','DEBUG')      


# l1.log(f'{Exception.__class__}','WTF','ERROR')        
# l1.log(f'{Exception.__class__}','WTF' ,'ERROR','error','a')     