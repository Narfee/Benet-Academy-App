# MIT License

# Copyright (c) 2021 Nicholas Papciak
# Copyright (c) 2020 Dhruv Bisla

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

class Headers: 
    base = {
        "authority": "plusportals.com",
        "accept": "*/*",
        "x-newrelic-id": "XQEDUV5SGwUDXFhXBQc=",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://plusportals.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-language": "en-US,en;q=0.9",
    }

    def __init__(self, session, school_name): 
        self.session = session
        self.__school_name = school_name

        self.__cfduid = session.cookies.get_dict().get("__cfduid")
        self.__uguid = self.session.cookies.get_dict().get("UGUID")
        self.__requestverificationtoken = session.cookies.get_dict().get("__RequestVerificationToken")
        self.__sessionid = session.cookies.get_dict().get("ASP.NET_SessionId")
        self.__emailoption = session.cookies.get_dict().get("emailoption")
        self.__ppusername = session.cookies.get_dict().get("ppusername")
        self.__aspxauth = session.cookies.get_dict().get(".ASPXAUTH")

         
    @property
    def login_headers(self):
        return {
            "accept": "text/html,application/xhtml xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "cookie": f"__cfduid={self.__cfduid}; ppschoollink={self.__school_name}; UGUID={self.__uguid}; __RequestVerificationToken={self.__requestverificationtoken}; _pps=-480"
            }

    @property
    def token_headers(self):
        return {'cookie': f'__cfduid={self.__cfduid}; ppschoollink={self.__school_name}; __RequestVerificationToken={self.__requestverificationtoken}; _pps=-480; ASP.NET_SessionId={self.__sessionid}; emailoption=RecentEmails; UGUID={self.__uguid}; ppusername={self.__ppusername}; .ASPXAUTH={self.__aspxauth}'}

    def grade_headers(self, token): 
        self.reload()
        return {'__requestverificationtoken': token, 'cookie': f'__cfduid={self.__cfduid}; ppschoollink={self.__school_name}; __RequestVerificationToken={self.__requestverificationtoken}; _pps=-480; ASP.NET_SessionId={self.__sessionid}; emailoption={self.__emailoption}; UGUID={self.__uguid}; ppusername={self.__ppusername}; .ASPXAUTH={self.__aspxauth}'}

    def reload(self):
        self.__cfduid = self.session.cookies.get_dict().get("__cfduid")
        self.__uguid = self.session.cookies.get_dict().get("UGUID")
        self.__requestverificationtoken = self.session.cookies.get_dict().get(
            "__RequestVerificationToken"
        )
        self.__sessionid = self.session.cookies.get_dict().get("ASP.NET_SessionId")
        self.__emailoption = self.session.cookies.get_dict().get("emailoption")
        self.__ppusername = self.session.cookies.get_dict().get("ppusername")
        self.__aspxauth = self.session.cookies.get_dict().get(".ASPXAUTH")