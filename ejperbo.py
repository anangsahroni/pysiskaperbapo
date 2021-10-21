import requests
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm
import time

pd.options.mode.chained_assignment = None  # default='warn'

class EJPERBO:
    URL="https://siskaperbapo.jatimprov.go.id/harga/tabel"
    PASAR_ENDPOINT="https://siskaperbapo.jatimprov.go.id/harga/pasar.json/"
    ENDPOINT="https://siskaperbapo.jatimprov.go.id/harga/tabel.nodesign/"
    data = pd.DataFrame(dict(JENIS=[],NAMA=[],SATUAN=[],HARGA_KMRN=[],HARGA_SKRG=[],
                             PERUB_RP=[], PERUB_PERSEN=[], KAB=[], TANGGAL=[], PASAR=[]))
    market_data=[]

    def __init__(self, min_date, max_date, region):
        self.min_date=min_date
        self.max_date=max_date
        self.region=region
        self._market_parse(init=True)

    def _market_parse(self, init=False):
        with requests.session() as rs:
            rs.get(self.URL)
            rp=rs.get(self.PASAR_ENDPOINT+self.region)
        market_names=[rp.json()[i]['psr_nama'] for i in range(len(rp.json()))]
        market_id=[rp.json()[i]['psr_id'] for i in range(len(rp.json()))]
        if init:
            print("SISKAPERBO East Java Python Client (unofficial)")
            print("="*50)
            if self.region[-3:] == "kab":
                print("Selected region: ", self.region[:-3].capitalize())
            else:
                print("Selected region: ", self.region[:-4].capitalize())
            print("Time range: {} - {}".format(self.min_date, self.max_date))
            print("Available market: ", market_names)
            self.market_data=dict(m_names=market_names,m_id=market_id)
        else:
            return dict(m_names=market_names,m_id=market_id)

    def _time_parse(self, days):
        min_date_l = [int(d) for d in self.min_date.split("-")]
        max_date_l = [int(d) for d in self.max_date.split("-")]
        min_date_dt = datetime.date(min_date_l[0], min_date_l[1], min_date_l[2])
        max_date_dt = datetime.date(max_date_l[0], max_date_l[1], max_date_l[2])
        time_dif = max_date_dt-min_date_dt
        num_days = time_dif.days
        if days=="all":
            time_list=[(min_date_dt+datetime.timedelta(i)).strftime("%Y-%m-%d")\
                   for i in range(num_days)]
        else:
            time_list=[]
            for i in range(num_days):
                date=min_date_dt+datetime.timedelta(i)
                if date.strftime("%A") in days:
                    time_list.append(date.strftime("%Y-%m-%d"))
        return time_list

    def _single_query(self, payload, market_data):
        with requests.session() as rs:
            rs.get(self.URL)
            rp = rs.post(self.ENDPOINT, payload, allow_redirects=False)
            df=pd.read_html(rp.text)
            data=df[0]
            data.columns=["NO","NAMA_BAHAN_POKOK","SATUAN","HARGA_KEMARIN","HARGA_SEKARANG","PERUBAHAN_RP","PERUBAHAN_PERSEN"]

            bool_bhn=data['NO'].notnull()
            bhn_name=data['NAMA_BAHAN_POKOK']

            bhn_name_list=[]
            bhn_name_first=bhn_name[0]
            for bobh, bhnm in zip(bool_bhn, bhn_name):
                if bobh:
                    bhn_name_first=bhnm
                    bhn_name_list.append(bhn_name_first)
                else:
                    bhn_name_list.append(bhn_name_first)

            data.replace('-', np.NaN,inplace=True)
            data['NAMA_BAHAN_POKOK'] = data['NAMA_BAHAN_POKOK'].str.replace('- ','',regex=False)
            data['BHN_PKK']=bhn_name_list
            data['BHN_PKK'] = data['BHN_PKK'].str.replace('- ','',regex=False)
            data['SATUAN']=data['SATUAN'].str.lower()

            data['HARGA_KEMARIN'] = data['HARGA_KEMARIN'].astype(str).str.replace('.','',regex=False)
            data['HARGA_SEKARANG'] = data['HARGA_SEKARANG'].astype(str).str.replace('.','',regex=False)
            data['PERUBAHAN_RP'] = data['PERUBAHAN_RP'].astype(str).str.replace('.','',regex=False)
            data['PERUBAHAN_PERSEN'] = data['PERUBAHAN_PERSEN'].astype(str).str.replace('.','', regex=False)
            data['PERUBAHAN_PERSEN'] = data['PERUBAHAN_PERSEN'].astype(str).str.replace(',','.', regex=False)
            data['PERUBAHAN_PERSEN'] = data['PERUBAHAN_PERSEN'].astype(str).str.replace('%','', regex=False)
            
            data[['HARGA_KEMARIN', 'HARGA_SEKARANG','PERUBAHAN_RP','PERUBAHAN_PERSEN']] = \
                 data[['HARGA_KEMARIN', 'HARGA_SEKARANG','PERUBAHAN_RP','PERUBAHAN_PERSEN']].astype(float)
            data.insert(0, 'BHN_PKKS', data['BHN_PKK'])

            #get backup for NO nonull
            NO_nonull=data[data['NO'].notnull()]
            SATUAN_nonull=NO_nonull[NO_nonull['SATUAN'].notnull()]
            SATUAN_nonull.drop(columns=['NO', 'BHN_PKK'], inplace=True)

            data=data[data['NO'].isnull()]
            data.drop(columns=['NO', 'BHN_PKK'], inplace=True)

            #append
            data=data.append(SATUAN_nonull)

            data.columns=['JENIS','NAMA','SATUAN','HARGA_KMRN','HARGA_SKRG',"PERUB_RP","PERUB_PERSEN"]
            data['KAB'] = [payload['kabkota'][:-3].capitalize() if payload['kabkota'][-3:] == "kab" \
                           else payload['kabkota'][:4].capitalize() for i in range(len(data['JENIS']))]
            data['TANGGAL'] = [payload['tanggal'] for i in range(len(data['JENIS']))]

            #pasar
            market_index=np.where(np.array(market_data['m_id']) == payload['pasar'])[0][0]
            data['PASAR'] = [market_data['m_names'][market_index] for i in range(len(data['JENIS']))]
            return data

    def query(self, delay=2, market="all", days="all"):
        for date in tqdm(self._time_parse(days=days)):
            if market == "all":
                market_data=self.market_data
                for market_id, market_name in zip(market_data['m_id'], market_data['m_names']):
                    payload={"tanggal": date,
                             "kabkota": self.region,
                             "pasar": market_id}
                    element_day=self._single_query(payload, market_data)
                    self.data = self.data.append(element_day)
                    time.sleep(delay)
            else:
                market_data=self.market_data
                market_id, market_name = market_data['m_id'], market_data['m_names']
                market_id_index = np.where(np.array(market_name) == market)[0][0]
                payload={"tanggal": date,
                         "kabkota": self.region,
                         "pasar": market_id[market_id_index]}

                element_day=self._single_query(payload, market_data)
                self.data = self.data.append(element_day)
                time.sleep(delay)
