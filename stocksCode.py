from bs4 import BeautifulSoup
import requests
import datetime

class Business:

    def __init__(self, name):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    
        self.name = name

    def get_growth_rate(self):
        # create url
        url1 = 'https://uk.finance.yahoo.com/quote/'
        url2 = '/analysis?p='
        url = url1 + self.name + url2 + self.name

        #get html
        response = requests.get(url, headers=self.headers)

        #create soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # find class
        tags = soup.find_all(string = 'Next 5 years (per annum)')
        # parent of class is table
        p = tags[0].parent.parent.parent
        # within table class find data
        num = p.find('td', class_='Ta(end) Py(10px)')

        # return
        rate = num.string
        rate = rate[:-1]
        out = float(rate)
        return out 
    


    def get_income(self):
        # create url
        url1 = 'https://finance.yahoo.com/quote/'
        url2 = '/financials?p='
        url = url1 + self.name + url2 + self.name
        #get html
        response = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        tags = soup.find_all(string = 'Net Income Common Stockholders')
        p = tags[0].parent.parent.parent.parent
        num = p.find('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)')
        income = num.string

        new_income = income.replace(',', '')
        return new_income

    def get_shares(self):
        # create url
        url1 = 'https://finance.yahoo.com/quote/'
        url2 = '/key-statistics?p='
        url = url1 + self.name + url2 + self.name
        #get html
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # find shares
        tags = soup.find_all(string = 'Shares Outstanding')
        p = tags[0].parent.parent.parent
        num = p.find('td', class_=  'Fw(500) Ta(end) Pstart(10px) Miw(60px)')
        shares = num.string
        
        # need to convert inton int 
  
        #  into correct format
        length = len(shares) - 1
        if shares[length] == 'B':
            shares = shares[:-1]
            int = float(shares)
            finial = int * 1000000000
            return finial
        elif shares[length] == 'M':
            shares = shares[:-1]
            int = float(shares)
            finial = int * 1000000
            return finial

    
    def get_debt(self):
        # create url
        url1 = 'https://finance.yahoo.com/quote/'
        url2 = '/key-statistics?p='
        url = url1 + self.name + url2 + self.name
        #get html
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        #find debt
        tags2 = soup.find_all(string = 'Total Debt')
        p2  = tags2[0].parent.parent.parent
        num = p2.find('td', class_ = 'Fw(500) Ta(end) Pstart(10px) Miw(60px)')
        debt = num.string

        #  into correct format
        length = len(debt) - 1
        if debt[length] == 'B':
            debt = debt[:-1]
            int = float(debt)
            finial = int * 1000000000
            return finial
        elif debt[length] == 'M':
            debt = debt[:-1]
            int = float(debt)
            finial = int * 1000000
            return finial


    def get_share_price(self):
        # create url
        url1 = 'https://finance.yahoo.com/quote/'
        url2 = '/key-statistics?p='
        url = url1 + self.name + url2 + self.name
    
        #get html
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # see if makret open or closed
        now = datetime.datetime.now()
        today8am = now.replace(hour=21, minute=0, second=0, microsecond=0)
        if now < today8am:
            tags = soup.find('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)')
            price = tags.string
            return price
        else:
            tags = soup.find_all(string = 'After hours:')
            p = tags[0].parent.parent.parent
            num = p.find('fin-streamer', class_ = 'C($primaryColor) Fz(24px) Fw(b)')
            price = num.string
            return price


    def get_discount_rate(self):
        #get html
        response = requests.get('http://www.worldgovernmentbonds.com/country/united-states/', headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        tags = soup.find_all(string = '10 years')
        p = tags[0].parent.parent.parent.parent
        num = p.find('td', class_ = 'w3-center w3-extralight-gray')
        rate = num.string

        # return
        rate = num.string
        rate = rate[:-1]
        out = float(rate)
        return out 

    def calculate_cash_flow(self):
        cash_flow = self.get_income()
        growth_rate = (self.get_growth_rate()) / 100
        cash_flows = []
        int_growth = int(growth_rate)
        projected_cash_flow = int(cash_flow)

        for i in range (1, 11):
            cash_flows.append(projected_cash_flow)
            projected_cash_flow = int(projected_cash_flow * (1 + growth_rate))
        
        last_year = cash_flows[9]
        return cash_flows
    
    def calculate_terminal_year(self):
        years = self.calculate_cash_flow()
        last_year = years[9]
        terminal_year = (last_year * 0.02) + last_year
        return int(terminal_year)
    
    def calculate_discount_cash(self):
        discount_rate = (self.get_discount_rate()) / 100
        cash_flow = self.calculate_cash_flow()
        discounted_cashflow = []

        for i, year in enumerate(cash_flow):
            discounted = float(year) / (1 + discount_rate) ** (i+1)
            discounted_cashflow.append(int(discounted))
        
        return sum(discounted_cashflow)
    
    def calculate_total_pv_cashflow(self):
        terminal_year = self.calculate_terminal_year()
        discount_rate = self.get_discount_rate()
        discounted_cashflow_total = self.calculate_discount_cash()

        terminal_year2 = 82426367614
        discount_rate2 = 0.05
        terminal_growth_rate = 0.002

        terminal_value = (terminal_year2 * (1 + terminal_growth_rate)) / (discount_rate2 - terminal_growth_rate)

        total_pv_cashflow = terminal_value + discounted_cashflow_total

        return int(total_pv_cashflow)

    def calculate_intrinsiv_value(self):
        total_pv = self.calculate_total_pv_cashflow()
        debt = int(self.get_debt())
        shares = int(self.get_shares())
        price = float(self.get_share_price())

        intrinsic_value = (total_pv - debt) / shares
        margin_of_safety = (-intrinsic_value * 0.30) + intrinsic_value
        margin_percent = (intrinsic_value - price) / intrinsic_value

        x = margin_percent * 100
        g = float("{0:.2f}".format(x))
        
        return g

        

def main():
    ticker = input('Enter ticker symbol: ')
    try:
        business = Business(ticker)
        print('====================================')
        print('Business:', ticker)
        print('====================================')
        print('Finance:')
        print('------------------------------------')
        print('Debt:', business.get_debt())
        print('Shares:', business.get_shares())
        print('Growth rate:', business.get_growth_rate())
        print('Income:', business.get_income())
        print('Share Price:', business.get_share_price())
        print('------------------------------------')
        print('Valuation:', business.calculate_intrinsic_value())
        print('------------------------------------')
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()