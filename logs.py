import logging as log

def register_log(message):
    log.basicConfig(level=logging.INFO, filename='app.log', format=f"{asctime} {levelname}:{message}")
    log.info(f"{message} logged in")

def got_calibration(message):
    pass
def got_articled(message):
    pass
def rated(message):
    pass

