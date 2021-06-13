import logging
import requests
import time
import os
from datetime import datetime
from requests.exceptions import ConnectionError,HTTPError,ProxyError,SSLError
import sys
sys.path.append('/usr/src/app')

import bot_config as cfg
import gcp_connect as gcp


def download(url):
    """ Captura os dados da pagina solicitada atraves de requests.get

    return: json data from the api request
    """
    try:
        get_url = requests.get(url, headers=cfg.hdr, verify=cfg.certif)
    except HTTPError as http_err:
        return logging.info(f"Ocorreu erro HTTP, verifique a URL: {http_err}")
    except ConnectionError as conn_err:
        return logging.info(f"Ocorreu erro de conexão, verifique a URL: {conn_err}")
    except ProxyError as proxy_err:
        return logging.info(f"Ocorreu erro de Proxy: {proxy_err}")
    except SSLError as ssl_err:
        return logging.info(f"Ocorreu erro de certificado SSL: {ssl_err}")
    except Exception as err:
        return logging.info(f'Ocorreu erro ao acessar a URL fornecida: {err}')
    else:
        data = get_url.text  
        logging.info("Download finalizado. URL: {}: ".format(url))
        return data


def upload_data(data, bucket, blob_name, blob_log_name, blob_path, log=False):
    """ Carrega os dados no bucket GCP
    
    return: None
    """
    try:
        if log == False:
            blob = gcp.blob_create(bucket, blob_path, blob_name)
            blob.upload_from_string(data, 'text/json')
            logging.info("Arquivo salvo no BUCKET: {} e BLOB: {}".format(bucket, blob))
        else:
            blob_log = gcp.blob_create(bucket, blob_path, blob_log_name)
            blob_log.upload_from_filename('temp.log')
    
    except Exception as expt:
        logging.exception("Ocorreu uma exceção.")
        pass


if __name__ == "__main__":
    ini = time.time()

    # instancia de log
    logger = logging.basicConfig(filename='temp.log', format='%(asctime)s - %(levelname)s - %(message)s',filemode='w', level=logging.INFO)
    
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M%S_")
    
    try:
        bucket = gcp.bucket_obj(cfg.project, cfg.bucket_name)
        logging.info('Conectado com sucesso no Bucket: ' + cfg.bucket_name)
        
        try:
            # download dos dados da URL fornecida
            data = download(cfg.url)       

            # definicao de BLOBS
            blob_name = dt_string + cfg.filename
            blob_log_name = dt_string + cfg.log_filename

            # uplodad de dados para GCS
            upload_data(data, bucket, blob_name, None, cfg.blob_path)

        except Exception as expt:
            logging.exception("Exception occurred.")
            pass
         
    except Exception as expt:
        logging.exception("Exception occurred.")
        pass

    finally:
        # uplodad de logs para GCS
        logging.info('Aplicação finalizada. Tempo de execução: ' + str(time.time()-ini) + 's')
        upload_data(None, bucket, None, blob_log_name, cfg.blob_path, log=True)

    logging.shutdown()
    os.remove('temp.log')