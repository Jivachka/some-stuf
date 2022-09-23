from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class Convertor(object):
    @classmethod
    def clean_marcket_volume(cls, _) -> int:
        try:
            if '€' in _:
                _ = _.replace('€', '')
            if ',' in _:
                _ = _.replace(',', '')
            return int(_)
        except Exception as e:
            print('Convertor-clean_marcket_volume\n', e)

    @classmethod
    def str_to_int(cls, _) -> int:
        try:
            return int(_)
        except Exception as e:
            print('Convertor-str_to_int\n', e)

    @classmethod
    def clean_time(cls, _: str):
        try:
            if "'" in _:
                _ = _.replace("'", '')
            if _ in [str(i) for i in range(140)]:
                return int(_)
            return _
        except Exception as e:
            print('Convertor-clean_time\n', e)

class BaseParseBF(object):
    PATH = r'C:\Users\admin\Desktop\selen\chromedriver\chromedriver.exe'
    # PATH = '/home/pi/Desktop/selenium/cromedriver/chromedriver'
    SITE = 'https://www.betfair.com/exchange/plus/inplay/football'
    FIND_TABLE = 'coupon-table'
    FIND_MARKET = 'mod-event-line'
    MARKET_VOLUME = 'matched-amount-value'
    NAME_MARKET = 'name'
    PLAYER_2 = 'away'
    PLAYER_1 = 'home'
    TIME_PLAY = 'middle-label'

    def __init__(self):
        self.chrome_options = Options()
        self.changer = Changer_types()
        self.chrome_options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(self.PATH, options=self.chrome_options)
        self.driver.wait = WebDriverWait(self.driver, 2)
        self._inplay_markets = []
        self._soonplay_markets = []

    def _connect(self):
        print(f'Connect to:{self.SITE}')
        try:
            self.driver.get(self.SITE)
            print(f'Connect is DONE')
            sleep(2)
        except Exception as e:
            print('Error', e)

    def _end(self):
        sleep(2)
        self.driver.quit()
        print(f'Session from {self.SITE} The end')

class InplayMarkerFinder(BaseParseBF):
    def __find_coupon_table(self) -> list:
        return self.driver.wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, self.FIND_TABLE)))

    def __find_markets(self):
        __coupon_table = self.__find_coupon_table()
        if len(__coupon_table) > 1:
            self._inplay_markets = __coupon_table[0]
            self._soonplay_markets = __coupon_table[1]
        elif len(__coupon_table) == 1:
            self._soonplay_markets = __coupon_table[0]
        else:
            raise NoSuchElementException('No have markets')

    def __find_true_markets(self, _list: list) -> list:
        result = _list
        for count, value in enumerate(result):
            try:
                value.find_element_by_class_name(self.TIME_PLAY).text
            except NoSuchElementException:
                delat = result.pop(count)
                print(delat)
        return result

    def __inplay_market(self):
        # self.__find_markets()
        result = self._inplay_markets.find_elements_by_class_name(self.FIND_MARKET)
        return result

    def __inplay_len(self, _list: list):
        print(f'To find {len(_list)} inplay markens,man!')

    def _markets_info_in_list(self, _list: list):
        out_all_list = []
        text_list = [f'Date: {datetime.today().day}.{datetime.today().month}.{datetime.today().year}\n']
        for i in _list:
            try:
                in_time = i.find_element_by_class_name(self.TIME_PLAY).text
                home_score = i.find_element_by_class_name(self.PLAYER_1).text
                away_score = i.find_element_by_class_name(self.PLAYER_2).text
                amaunt = i.find_element_by_class_name(self.MARKET_VOLUME).text
                runners = i.find_elements_by_class_name(self.NAME_MARKET)
                home_runner = runners[0].text
                away_runner = runners[1].text
                out_marker_list = [
                    Convertor.clean_marcket_volume(amaunt),
                    Convertor.clean_time(in_time),
                    Convertor.str_to_int(home_score),
                    Convertor.str_to_int(away_score),
                    home_runner,
                    away_runner
                ]
                out_all_list.append(out_marker_list)
                print()
            except Exception as e:
                print('_markets_info_in_list',e)
        return out_all_list

    def turn_on(self):
        try:
            self._connect()
            # print(self.__find_coupon_table())
            self.__find_markets()
            # print(self.__inplay_market())
            # print(self._inplay_markets)
            inplay_markets = self.__find_true_markets(self.__inplay_market())
            res = self._markets_info_in_list(inplay_markets)
            print(res)

            # self.__inplay_sorted_market = self.__find_true_markets(self.__inplay_market())
            # print(self._view(self.__inplay_sorted_market))

        except Exception as e:
            print(e)

    def turn_off(self):
        try:
            self._end()
        except:
            print('erorr to exit')


# class BaseView(object):
#     def _view(self, _list: list):
#         self.text_list = [f'Date: {datetime.today().day}.{datetime.today().month}.{datetime.today().year}\n']
#         for i in _list:
#             try:
#                 self.in_time = i.find_element_by_class_name(self.TIME_PLAY).text
#                 self.home_score = i.find_element_by_class_name(self.PLAYER_1).text
#                 self.away_score = i.find_element_by_class_name(self.PLAYER_2).text
#                 self.amaunt = i.find_element_by_class_name(self.MARKET_VOLUME).text  ###
#                 self.amaunt_int = self.changer.to_int(self.amaunt)
#                 self.runners = i.find_elements_by_class_name(self.NAME_MARKET)
#                 self.home_runner = self.runners[0].text
#                 self.away_runner = self.runners[1].text
#                 self.text = f'{self.amaunt}\n{self.in_time}\n' \
#                             f'{self.home_score} {self.home_runner}\n{self.away_score} {self.away_runner}\n\n'
#                 self.text_list.append(self.text)
#             except:
#                 print('error')
#         self.text_join = ' '.join(self.text_list)
#         return self.text_join

class Changer_types:
    def __del_charge(self, text: str):
        return text[1:]

    def __replace_dot(self, _):
        text = self.__del_charge(_)
        res = text.replace(',', '')
        return res

    def to_int(self, _):
        text = int(self.__replace_dot(_))
        return text


class BaseMarket(object):
    pass


if __name__ == "__main__":
    browser = InplayMarkerFinder()
    browser.turn_on()
    browser.turn_off()
