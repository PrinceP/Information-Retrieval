import json
import requests


city_codes = {'ahmedabad': 'AMD', 'hyderabad': 'HYD', 'pantnagar': 'PGH', 'agatti island': 'AGX', 'kanpur': 'KNU', 'osmanabad': 'OMN', 'gorakhpur': 'GOP', 'agartala': 'IXA', 'ramagundam': 'RMD', 'car nicobar': 'CBD', 'cooch behar': 'COH', 'thanjavur': 'TJV', 'daman': 'NMB', 'khowai': 'IXN', 'dhanbad': 'DBD', 'agra': 'AGR', 'rupsi': 'RUP', 'pondicherry': 'PNY', 'ranchi': 'IXR', 'mumbai': 'BOM', 'kailashahar': 'IXH', 'bagdogra': 'IXB', 'dehra dun': 'DED', 'chennai/madras': 'MAA', 'raipur': 'RPR', 'amritsar': 'ATQ', 'lilabari': 'IXI', 'kandla': 'IXY', 'muzaffarnagar': 'MZA', 'puttaparthi': 'PUT', 'jaisalmer': 'JSA', 'coimbatore': 'CJB', 'bangalore': 'BLR', 'pathankot': 'IXP', 'ludhiana': 'LUH', 'dibrugarh': 'DIB', 'tirupati': 'TIR', 'jammu': 'IXJ', 'bhatinda': 'BUP', 'delhi': 'DEL', 'jabalpur': 'JLR', 'daparizo': 'DAE', 'jagdalpur': 'JGB', 'shillong': 'SHL', 'pasighat': 'IXT', 'allahabad': 'IXD', 'tuticorin': 'TCR', 'ratnagiri': 'RTC', 'hissar': 'HSS', 'warangal': 'WGC', 'kota': 'KTU', 'bellary': 'BEP', 'dimapur': 'DMU', 'gaya': 'GAY', 'surat': 'STV', 'zero': 'ZER', 'gwalior': 'GWL', 'akola': 'AKD', 'belgaum': 'IXG', 'keshod': 'IXK', 'bikaner': 'BKB', 'jaipur': 'JAI', 'mohanbari': 'MOH', 'diu': 'DIU', 'indore': 'IDR', 'kolhapur': 'KLH', 'mangalore': 'IXE', 'darjeeling': 'DAI', 'madurai': 'IXM', 'dharamsala': 'DHM', 'hubli': 'HBX', 'sholapur': 'SSE', 'chandigarh': 'IXC', 'rajahmundry': 'RJA', 'thiruvananthapuram': 'TRV', 'kozhikode': 'CCJ', 'jamshedpur': 'IXW', 'deparizo': 'DEP', 'salem': 'SXV', 'neyveli': 'NVY', 'khajuraho': 'HJR', 'aizawl': 'AJL', 'rewa': 'REW', 'malda': 'LDA', 'rajkot': 'RAJ', 'vishakhapatnam': 'VTZ', 'jeypore': 'PYB', 'jamnagar': 'JGA', 'balurghat': 'RGH', 'goa': 'GOI', 'bilaspur': 'PAB', 'vadodara': 'BDQ', 'guna': 'GUX', 'patna': 'PAT', 'silchar': 'IXS', 'kolkata': 'CCU', 'udaipur': 'UDR', 'kamalpur': 'IXQ', 'bhopal': 'BHO', 'simla': 'SLV', 'tezpur': 'TEZ', 'rourkela': 'RRK', 'jodhpur': 'JDH', 'muzaffarpur': 'MZU', 'bhuntar': 'KUU', 'leh': 'IXL', 'varanasi': 'VNS', 'satna': 'TNI', 'cityname': 'airport-code', 'port blair': 'IXZ', 'jorhat': 'JRH', 'nasik': 'ISK', 'vijayawada': 'VGA', 'porbandar': 'PBD', 'tiruchirapally': 'TRZ', 'aurangabad': 'IXU', 'along': 'IXV', 'srinagar': 'SXR', 'gawahati': 'GAU', 'bhubaneswar': 'BBI', 'pune': 'PNQ', 'imphal': 'IMF', 'lucknow': 'LKO', 'cuddapah': 'CDP', 'bhavnagar': 'BHU', 'nagpur': 'NAG', 'rajouri': 'RJI', 'bhuj': 'BHJ', 'mysore': 'MYQ', 'nanded': 'NDC', 'bareli': 'BEK', 'tezu': 'TEI', 'kochi': 'COK'}




api_key = "AIzaSyAADjRri8mKUJwPDRMdJkXQO1Kz-0uDlWg"
url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key
headers = {'content-type': 'application/json'}

import time

 


def makeparameters(par1_fromcity, par2_tocity, par3_date):
  par1 = city_codes.get(par1_fromcity)
  par2 = city_codes.get(par2_tocity)
  if par3_date == None:
    par3_date = (time.strftime("%Y-%m-%d"))

  params = {
  "request": {
    "slice": [
      {
        "origin": par1,
        "destination": par2,
        "date": par3_date
      }
    ],
    "passengers": {
      "adultCount": 1
    },
    "solutions": 1,
    "refundable": False
    }
  }
  response = requests.post(url, data=json.dumps(params), headers=headers)
  data = response.json()
  #print data
  return data





    






  




