# request gas accident XML from web
import requests
import urllib.parse

accidentUrl = "http://safemap.go.kr/openApiService/data/getGasAcdntOccrrncStatsData.do"  # URL
accidentParams = {
    "serviceKey": "IAAEO1QQ-IAAE-IAAE-IAAE-IAAEO1QQTP",  # Service Key
    "pageNo": "1",  # page number
    "numOfRows": "5048",  # results per page
    "type": "xml"
}

accident_encoded_params = urllib.parse.urlencode(accidentParams)
accident_full_url = accidentUrl + "?" + accident_encoded_params
print(accident_full_url)
accident_data = requests.get(accident_full_url)
################################################################################
import pandas as pd
from xml.etree import ElementTree as ET

if accident_data.status_code == 200:
    root = ET.fromstring(accident_data.content)

    emd_codes = [element.text for element in root.findall(".//EMD_CD")]
    x_values = [element.text for element in root.findall(".//X")]
    y_values = [element.text for element in root.findall(".//Y")]
    total_accidents = [element.text for element in root.findall(".//TOT")]
    ctprvn_names = [element.text for element in root.findall(".//CTPRVN_NM")]
    sgg_names = [element.text for element in root.findall(".//SGG_NM")]
    emd_names = [element.text for element in root.findall(".//EMD_NM")]

    valid_emd_codes = []
    valid_x_values = []
    valid_y_values = []
    valid_total_accidents = []
    valid_ctprvn_names = []
    valid_sgg_names = []
    valid_emd_names = []

# Remove cases with no accidents
    for i in range(len(emd_codes)):
        if total_accidents[i] != '0':
            valid_emd_codes.append(emd_codes[i])
            valid_x_values.append(x_values[i])
            valid_y_values.append(y_values[i])
            valid_total_accidents.append(total_accidents[i])
            valid_ctprvn_names.append(ctprvn_names[i])
            valid_sgg_names.append(sgg_names[i])
            valid_emd_names.append(emd_names[i])
################################################################################
# pass emd code as argument: return mean age of bulidings in area
import pandas as pd
from xml.etree import ElementTree as ET
def meanAgeBuilding(emd_code):
  url = "http://openapi.nsdi.go.kr/nsdi/BuildingAgeService/attr/getBuildingAge"  # URL
  params = {
    "authkey": "ff16d2ca3883bf51100041",  # Service Key
    "pnu": emd_code,  # 건물고유번호 (8자리 이상 기입)
    "format": "xml",
    "numOfRows": "10000",
  }

  encoded_params = urllib.parse.urlencode(params)
  full_url = url + "?" + encoded_params
  print(full_url)
  response = requests.get(full_url)
  root = ET.fromstring(response.content)
  buildingAge = [element.text for element in root.findall(".//buldAge")]
  buildingAgeSum = 0
  for i in buildingAge:
        buildingAgeSum = buildingAgeSum + int(i)
  try:
      meanAge = float(buildingAgeSum) / len(buildingAge)
      print(meanAge)
      return meanAge
  except ZeroDivisionError:
      print('No building data available for this area.')
      return 0

# retrieve mean age for all area accidents
valid_buildingAge = []
for code in valid_emd_codes:
    valid_buildingAge.append(meanAgeBuilding(code))
################################################################################


# extract data and save as csv
data = {
    'CTPRVN_NM': valid_ctprvn_names,
    'SGG_NM': valid_sgg_names,
    'EMD_NM': valid_emd_names,
    'EMD_CD': valid_emd_codes,
    'X': valid_x_values,
    'Y': valid_y_values,
    'TOT': valid_total_accidents,
    'BDG_AGE' : valid_buildingAge
}

df = pd.DataFrame(data)
################################################################################
csv_file_path = 'total.csv'

# Write the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False, encoding='utf-8')



