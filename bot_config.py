from datetime import datetime
now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")

### Configuration CASAS DE CAMBIO 

## GCP pointing ------------

# GCP project name
project = 'dev-data'

# GCP bucket name
bucket_name = 'bvs-bigdata-datalake-stage-external-cadastral-rf-dev'

# Blob path
blob_path = 'datalake/stage/external/cadastral/rf/data/CASASCAMBIO/ partitions/monthly/' + str(year) + '/' + str(month) + '/'



## File Names ------------

# file name to save logging information
log_filename = "casasCambio.log'"

# File name to save scrapped data 
filename = 'casasCambio.json'



## Scrap definitions ------------

# Download URL 
url='https://www3.bcb.gov.br/vet/rest/v2/listaPontoCambio?cnpj=00000000'

# Headers necessarry to request the data from Processos api webpage
hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'} 

# Boolean for request certification on data request
certif = True