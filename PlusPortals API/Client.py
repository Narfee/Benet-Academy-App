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
 
import json
import requests
from urllib.parse import urljoin
from lxml import html

from Headers import Headers

URL = "https://plusportals.com/"

class Client:

    def __init__(self, school_name, email, password):
        self.school_name = school_name
        self.email = email
        self.password = password

        self.session = requests.Session()
        self.school_url = urljoin(URL, self.school_name)
        self.headers = Headers(self.session, self.school_name)
        self.token = None

    def get_token(self):
        """
        Retrieves an authorization token 

        Returns: 
            str = the reponse authorization token

        Raises: 
            TokenError : when there is an error retrieving the token
        """

        # logs in to plusportals 
        data = [
            ("UserName", self.email),
            ("Password", self.password),
            ("RememberMe", "true"),
            ("btnsumit", "Sign In"),
        ]
        response = self.session.post(self.school_url, headers=dict(self.headers.base, **self.headers.login_headers), data=data)


        # retrieves the request verification token
        response = self.session.post(urljoin(URL, f'ParentStudentDetails/{self.school_name}'), headers=dict(self.headers.base, **self.headers.token_headers))
        tree = html.fromstring(response.text)

        try:
            token = tree.xpath("/html/body/input/@value")[0]
        except:
            raise type("TokenError", (Exception, ), {})("Error retrieving token")

        return token


    def get_grades(self):
        """
        Retrieves the grades for the current person

        Returns: 
            list[dict] = a list of marking periods and grades for that period

        Raises: 
            GradeError : when the grades could not be correctly retrieved
        """

        # gets the token and the special headers
        token = self.token or self.refresh_token()
        spec_headers = self.headers.grade_headers(token)

        # retrieves the grades for each marking period and combines them
        try: 
            response = self.session.post(urljoin(URL, 'ParentStudentDetails/GetMarkingPeriod'), headers=dict(self.headers.base, **spec_headers))
            marking_periods = json.loads(response.content.decode('utf-8'))[1:]
        except:
            raise type("GradeError", (Exception, ), {})("Error retrieving grades") 


        # goes through the marking periods and builds a list of grades
        grades = []
        for period in marking_periods:
            mp_grade = {}
            response = self.session.post(
                urljoin(URL, f'ParentStudentDetails/ShowGridProgressInfo?markingPeriodId={period["MarkingPeriodId"]}&isGroup=false'),
                headers=dict(self.headers.base, **spec_headers)
            )

            mp_grade["period_id"] = period["MarkingPeriodId"]
            mp_grade["period_name"] = period["MarkingPeriodName"]

            data = []
            courses = json.loads(response.content.decode('utf-8'))["Data"]

            for course in courses:
                data.append({"name": course["CourseName"],
                             "average": course["Average"],
                             "symbol": course["GradeSymbol"]
                             })

            mp_grade["data"] = data

            grades.append(mp_grade)

        return grades

    def clear_token(self): 
        """Clears the current token"""
        self.token = None
    
    def refresh_token(self): 
        """Refreshes the current token"""
        self.clear_token()
        self.token = self.get_token()
        return self.token