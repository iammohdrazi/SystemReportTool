import logging
from datetime import datetime
import time
import random
import os

def setup_logger():
    """Configure logging: create 'log' directory and setup log file."""
    log_dir = os.path.join(os.path.dirname(__file__), "log")
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"execution_log_{timestamp}.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    return log_file

def dummy_task():
    """A simulated task with random warning and error generation."""
    logging.debug("Entered dummy_task function.")

    logging.info("Starting task execution...")
    time.sleep(1)  # Simulate work

    warning_chance = random.random()
    logging.debug(f"Generated warning_chance = {warning_chance:.4f}")
    if warning_chance < 0.3:
        logging.warning("Low memory detected. Proceeding with caution...")

    error_chance = random.random()
    logging.debug(f"Generated error_chance = {error_chance:.4f}")
    if error_chance < 0.2:
        logging.critical("A critical error is about to be raised.")
        raise RuntimeError("Simulated task failure due to unexpected error.")

    logging.info("Task completed successfully.")
    logging.debug("Exiting dummy_task function.")
    return "Success"

def main():
    """Main function to control program flow."""
    logging.info("Program started.")

    try:
        result = dummy_task()
        logging.info(f"Task result: {result}")
    except Exception as e:
        logging.error("An exception occurred during execution.", exc_info=True)
    finally:
        logging.info("Program finished execution.")

if __name__ == "__main__":
    log_path = setup_logger()
    main()
    print(f"\nLog file created at: {log_path}")
