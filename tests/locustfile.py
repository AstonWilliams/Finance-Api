import sys
import os

#  locust -f locustfile.py --host=http://localhost:8000
# Append the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def metrics(self):
        self.client.get("/metrics")

    @task
    def metrics_json(self):
        self.client.get("/metrics_json")

    @task
    def health(self):
        self.client.get("/health")

    @task
    def read_yahoo_finance_data_1(self):
        self.client.get("/yahoofinance?symbol=VTSMX")

    @task
    def read_yahoo_finance_data_2(self):
        self.client.get("/yahoofinance?symbol=VTSMX&name=Vanguard%20Total%20Stock%20Mkt%20Idx%20Inv")

    @task
    def read_yahoo_finance_data_3(self):
        self.client.get("/yahoofinance?symbol=VTSMX&price=144.16")

    @task
    def read_yahoo_finance_data_4(self):
        self.client.get("/yahoofinance?symbol=VTSMX&price=144.16&change=%2B1.34")

    @task
    def read_yahoo_finance_data_5(self):
        self.client.get("/yahoofinance?symbol=VTSMX&price=144.16&change=%2B1.34&change_percent=%2B0.94%25")

    @task
    def read_yahoo_finance_data_6(self):
        self.client.get("/yahoofinance?symbol=VTSMX&price=144.16&change=%2B1.34&change_percent=%2B0.94%25&ytd_return=%2B1.29%25")

    @task
    def read_yahoo_finance_data_7(self):
        self.client.get("/yahoofinance?symbol=VTSMX&price=144.16&change=%2B1.34&change_percent=%2B0.94%25&ytd_return=%2B1.29%25&three_mo_return=%2B2.24%25")

    @task
    def read_yahoo_finance_data_8(self):
        self.client.get("/yahoofinance?symbol=VTSMX&price=144.16&change=%2B1.34&change_percent=%2B0.94%25&ytd_return=%2B1.29%25&three_mo_return=%2B2.24%25&one_year=%2B25.89%25")

    @task
    def read_yahoo_finance_data_9(self):
        self.client.get("/yahoofinance?symbol=VTSMX&price=144.16&change=%2B1.34&change_percent=%2B0.94%25&ytd_return=%2B1.29%25&three_mo_return=%2B2.24%25&one_year=%2B25.89%25&three_year_return=%2B25.59%25")

    @task
    def read_yahoo_finance_data_10(self):
        self.client.get("/yahoofinance?symbol=VTSMX&price=144.16&change=%2B1.34&change_percent=%2B0.94%25&ytd_return=%2B1.29%25&three_mo_return=%2B2.24%25&one_year=%2B25.89%25&three_year_return=%2B25.59%25&five_year_return=%2B30.65%25")

    @task
    def read_yahoo_finance_data_11(self):
        self.client.get("/yahoofinance?symbol=VTSMX&price=144.16&change=%2B1.34&change_percent=%2B0.94%25&ytd_return=%2B1.29%25&three_mo_return=%2B2.24%25&one_year=%2B25.89%25&three_year_return=%2B25.59%25&five_year_return=%2B30.65%25&net_expense_ratio=0.04")

    @task
    def read_yahoo_finance_data_12(self):
        self.client.get("/yahoofinance?symbol=VTSMX&price=144.16&change=%2B1.34&change_percent=%2B0.94%25&ytd_return=%2B1.29%25&three_mo_return=%2B2.24%25&one_year=%2B25.89%25&three_year_return=%2B25.59%25&five_year_return=%2B30.65%25&net_expense_ratio=0.04&gross_expense_ratio=0.04")

    @task
    def read_yahoo_finance_data_13(self):
        self.client.get("/yahoofinance?symbol=VTSMX&price=144.16&change=%2B1.34&change_percent=%2B0.94%25&ytd_return=%2B1.29%25&three_mo_return=%2B2.24%25&one_year=%2B25.89%25&three_year_return=%2B25.59%25&five_year_return=%2B30.65%25&net_expense_ratio=0.04&gross_expense_ratio=0.04&net_assets=1.778T")

    @task
    def read_yahoo_finance_data_14(self):
        self.client.get("/yahoofinance?symbol=VTSMX&price=144.16&change=%2B1.34&change_percent=%2B0.94%25&ytd_return=%2B1.29%25&three_mo_return=%2B2.24%25&one_year=%2B25.89%25&three_year_return=%2B25.59%25&five_year_return=%2B30.65%25&net_expense_ratio=0.04&gross_expense_ratio=0.04&net_assets=1.778T&fifty_day_avg=143.53")

    @task
    def read_yahoo_finance_data_15(self):
        self.client.get("/yahoofinance?symbol=VTSMX&price=144.16&change=%2B1.34&change_percent=%2B0.94%25&ytd_return=%2B1.29%25&three_mo_return=%2B2.24%25&one_year=%2B25.89%25&three_year_return=%2B25.59%25&five_year_return=%2B30.65%25&net_expense_ratio=0.04&gross_expense_ratio=0.04&net_assets=1.778T&fifty_day_avg=143.53&two_hundred_day_avg=134.03")

    @task
    def read_yahoo_finance_data_16(self):
        self.client.get("/yahoofinance?name=Vanguard%20Total%20Stock%20Mkt%20Idx%20Inv")

    @task
    def read_yahoo_finance_data_17(self):
        self.client.get("/yahoofinance?name=Vanguard%20Total%20Stock%20Mkt%20Idx%20Inv&change=%2B1.34")

    @task
    def read_yahoo_finance_data_18(self):
        self.client.get("/yahoofinance?name=Vanguard%20Total%20Stock%20Mkt%20Idx%20Inv&change=%2B1.34&change_percent=%2B0.94%25")

    @task
    def read_yahoo_finance_data_19(self):
        self.client.get("/yahoofinance?name=Vanguard%20Total%20Stock%20Mkt%20Idx%20Inv&change=%2B1.34&change_percent=%2B0.94%25&price=144.16")

    @task
    def read_yahoo_finance_data_20(self):
        self.client.get("/yahoofinance?name=Vanguard%20Total%20Stock%20Mkt%20Idx%20Inv&change=%2B1.34&change_percent=%2B0.94%25&price=144.16&ytd_return=%2B1.29%25")

    @task
    def read_yahoo_finance_data_21(self):
        self.client.get("/yahoofinance?name=Vanguard%20Total%20Stock%20Mkt%20Idx%20Inv&change=%2B1.34&change_percent=%2B0.94%25&price=144.16&ytd_return=%2B1.29%25&three_mo_return=%2B2.24%25")
