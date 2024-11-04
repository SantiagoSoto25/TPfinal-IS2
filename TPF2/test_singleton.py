from corporate_data import CorporateData
from corporate_log import CorporateLog
import uuid
import logging

logging.basicConfig(level=logging.INFO)

data_instance_1 = CorporateData()
data_instance_2 = CorporateData()
assert data_instance_1 is data_instance_2
print(data_instance_1 is data_instance_2)

log_instance_1 = CorporateLog()
log_instance_2 = CorporateLog()
assert log_instance_1 is log_instance_2
print(log_instance_1 is log_instance_2)

session_uuid = str(uuid.uuid4())
cpu_uuid = str(uuid.getnode())

data = data_instance_1.getData(session_uuid, cpu_uuid, "5")
logging.info(f"Datos obtenidos: {data}")

cuit = data_instance_1.getCUIT(session_uuid, cpu_uuid, "5")
logging.info(f"CUIT obtenido: {cuit}")

seq_id = data_instance_1.getSeqID(session_uuid, cpu_uuid, "5")
logging.info(f"ID de Secuencia: {seq_id}")

log_instance_1.post(session_uuid, "getData")
logs = log_instance_1.list(cpu_uuid)
logging.info(f"Logs obtenidos: {logs}")

