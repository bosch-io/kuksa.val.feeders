import zenoh, time, logging, sys
from signal import SIGINT, SIGTERM, signal

log = logging.getLogger("subscriber")

def process_sample(sample: zenoh.Sample) -> None:
    str_value = sample.payload.decode('utf-8')
    log.info(
        "received sample [key: %s, value: %s, ts: %s]",
        sample.key_expr, str_value, sample.timestamp)

if __name__ == "__main__":
    key = "Vehicle/**"
    logging.basicConfig(level="INFO")
    zenoh.init_logger()
    session = zenoh.open()
    subscriber = session.declare_subscriber(key, process_sample)
    global running
    running = True

    def signal_handler(signal_received, frame):
        log.info("Received signal %s, stopping...", signal_received)
        subscriber.undeclare()
        session.close()
        global running
        running = False

    signal(SIGINT, signal_handler)
    signal(SIGTERM, signal_handler)

    log.info("listening for samples matching key %s", key)
    while running:
        time.sleep(1)
