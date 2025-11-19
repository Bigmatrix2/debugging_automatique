# logging_utils.py
import logging
from pathlib import Path

def setup_logger(log_file: str):
    """Configure le logger global pour le projet."""
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger("debugger")

def log_execution(logger, script_path, result):
    """Log l'exécution d'un script et ses résultats."""
    logger.info(f"Exécution du script: {script_path}")
    logger.info(f"stdout: {result['stdout']}")
    logger.info(f"stderr: {result['stderr']}")
    logger.info(f"returncode: {result['returncode']}")

def log_ai_response(logger, response):
    """Log la réponse brute de l'IA."""
    logger.info("Réponse IA reçue:")
    logger.info(response)

def log_corrections(logger, corrections):
    """Log les corrections proposées par l'IA."""
    for corr in corrections:
        logger.info(f"Correction: ligne {corr['line_number']} | {corr['type']} | {corr['reason']}")

def log_patch(logger, file_path, backup_path):
    """Log l'application des corrections."""
    logger.info(f"Corrections appliquées sur {file_path}. Backup créé: {backup_path}")