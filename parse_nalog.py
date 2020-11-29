import requests as req
import urllib3

urllib3.disable_warnings()


class EgrulNalogClient:
    def __init__(self):
        self.session = req.Session()
        self.base_host = 'https://egrul.nalog.ru'

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @staticmethod
    def _write_pdf(pdf, filename):
        import os
        with open(f'./data/{filename}.pdf', 'wb') as f:
            f.write(pdf)

    @staticmethod
    def _parse_get_params(params):
        params_dict = {x[0]: x[1] for x in [x.split("=") for x in params[1:].split("&")]}
        print(params_dict)

    def _get_url(self, endpoint):
        return self.base_host + endpoint

    def _make_request(self, method='GET', endpoint='', headers=None, cookies=None, **kwargs):
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0)'})
        if headers:
            self.session.headers.update(headers)

        if cookies:
            self.session.cookies.update(cookies)

        kwargs.update({'verify': False})

        response = self.session.request(method, self._get_url(endpoint), **kwargs)
        return response

    def _search_result(self, extract_id):
        response = self._make_request('GET', f'/search-result/{extract_id}').json()
        rows = response.get('rows')
        if not rows:
            return

        return rows[0]

    def _vyp_request(self, token):
        response = self._make_request('GET', f'/vyp-request/{token}').json()
        return response.get('t')

    def _vyp_status(self, token):
        return self._make_request('GET', f'/vyp-status/{token}').json()

    def _vyp_download(self, token):
        return self._make_request('GET', f'/vyp-download/{token}').text.encode()

    def download(self, query: str, regions: list, full_eq: bool = False):
        """
        vyp-request
        vyp-status
        vyp-download
        """

        info_id = self._search_info(query, regions, full_eq)
        if not info_id:
            return

        result = self._search_result(info_id)

        if not result:
            return

        company_token = result.get('t')
        ogrn = result.get('o')
        inn = result.get('i')
        token = self._vyp_request(company_token)
        response = self._vyp_status(token)

        if response.get('status') != 'ready':
            return

        return [ogrn, inn]

    def _search_info(self, query: str, regions: list, full_eq: bool = False):
        full_eq = 'on' if full_eq else 'off'
        regions = '%2c'.join([str(x) if len(str(x)) == 2 else '0' + str(x) for x in regions])
        data = {
            'query': query,
            'nameEq': full_eq,
            'region': regions,
        }

        info = self._make_request('POST', '/', data=data).json()

        if not info:
            print('Не могу получить сведения о компаниях')
            return

        info_id = info.get('t')
        captcha_id = info.get('captchaRequired')

        if 'captchaRequired' in info.keys() and captcha_id:
            print('Нужна капча')
            return

        return info_id


default_reg = list(range(1, 80))
default_reg += [87, 89, 91, 92, 99]


def get_ogrn_inn(query: str, regions: list = default_reg, full_eq: bool = False):
    client = EgrulNalogClient()
    a = client.download(query, regions, full_eq)
    return a

