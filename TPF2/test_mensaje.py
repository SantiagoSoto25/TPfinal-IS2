import logging
import uuid
import unittest
from corporate_data import CorporateData
from corporate_log import CorporateLog

logging.basicConfig(level=logging.INFO)

class TestSingleton(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_logging_level = logging.getLogger().level
        logging.getLogger().setLevel(logging.INFO)
        logging.info("Inicio de pruebas: Activando logging en nivel INFO.")

    @classmethod
    def tearDownClass(cls):
        logging.getLogger().setLevel(cls.original_logging_level)
        logging.info("Fin de pruebas: Restaurando el nivel de logging original.")

    def test_corporate_data_singleton(self):
        data_instance_1 = CorporateData()
        data_instance_2 = CorporateData()

        session_uuid = str(uuid.uuid4())
        cpu_uuid = str(uuid.getnode())

        data = data_instance_1.getData(session_uuid, cpu_uuid, "5")
        logging.info(f"Datos obtenidos: {data}")

        cuit = data_instance_1.getCUIT(session_uuid, cpu_uuid, "5")
        logging.info(f"CUIT obtenido: {cuit}")

        seq_id = data_instance_1.getSeqID(session_uuid, cpu_uuid, "5")
        logging.info(f"ID de Secuencia: {seq_id}")

    def test_corporate_log_singleton(self):
        log_instance_1 = CorporateLog()
        log_instance_2 = CorporateLog()
        
        session_uuid = str(uuid.uuid4())
        log_instance_1.post(session_uuid, "getData")
        cpu_uuid = str(uuid.getnode())
        logs = log_instance_1.list(cpu_uuid)
        logging.info(f"Logs obtenidos: {logs}")

if __name__ == '__main__':
    unittest.main()
