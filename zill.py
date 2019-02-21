import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


class GetSearchResults(object):
    def __init__(self):
        self.base_url = 'http://www.zillow.com/webservice/GetSearchResults.htm'
        self.excel_name = 'Consumer Data_10394_Sample1.csv'
        self.zws_id = 'X1-ZWz1gwpzjo4npn_6v82r'
        self.excel_write()

    def price_read(self, address, citystatezip):
        url = '{}?zws-id={}&address={}&citystatezip={}'.format(self.base_url,self.zws_id, address, citystatezip)
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')
        valuation_low = soup.select('low')[0].contents[0]
        valuation_high = soup.select('high')[0].contents[0]
        return valuation_low, valuation_high

    def excel_read(self):
        address = []
        citystatezip = []
        with open(self.excel_name, newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                address.append(row[0].replace(" ", "+"))
                citystatezip.append(row[1].replace(" ", "%2C+"))
            csvfile.close()
        return address, citystatezip

    def excel_write(self):
        valuation_low = []
        valuation_high = []
        address, citystatezip = self.excel_read()
        for i in range(1,(len(address))):
            low,high = self.price_read(address[i],citystatezip[i])
            valuation_low.append(low)
            valuation_high.append(high)
        table = pd.read_csv(self.excel_name)
        table['VALUATION LOW'] = valuation_low
        table['VALUATION HIGH'] = valuation_high
        table.to_csv('Consumer Data.csv')


if __name__ == '__main__':
    GetSearchResults()

