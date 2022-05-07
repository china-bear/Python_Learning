from __future__ import absolute_import
import os
import logging
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import logging
from bs4 import BeautifulSoup


# 把当前文件所在文件夹的父文件夹路径加入到PYTHONPATH

# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class NotLoggedOnError(Exception):
    pass


class SessionError(Exception):
    pass


class LoginError(Exception):
    pass


class UploadError(Exception):
    pass


class ExecuteError(Exception):
    pass


class CancelError(Exception):
    pass


class ScheduleError(Exception):
    pass


class FetchFlowsError(Exception):
    pass


class FetchScheduleError(Exception):
    pass


class FetchSLAError(Exception):
    pass


class UnscheduleError(Exception):
    pass


class CreateError(Exception):
    pass


class FetchProjectsError(Exception):
    pass


class AddPermissionError(Exception):
    pass


class RemovePermissionError(Exception):
    pass


class ChangePermissionError(Exception):
    pass


class FetchFlowExecutionError(Exception):
    pass


class FetchJobsFromFlowError(Exception):
    pass


class FetchFlowExecutionUpdatesError(Exception):
    pass


class FetchExecutionsOfAFlowError(Exception):
    pass


class FetchExecutionJobsLogError(Exception):
    pass


class ResumeFlowExecutionError(Exception):
    pass


class FetchRunningExecutionsOfAFlowError(Exception):
    pass


def login_request(session, host, user, password):
    """Login request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str host: Hostname where the request should go
    :param str user: The user name
    :param str password: The user password
    :return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """

    response = session.post(
        host,
        data={
            u'action': u'login',
            u'username': user,
            u'password': password
        }
    )

    logging.debug("Response: \n%s", response.text)

    return response


def fetch_flows_request(session, host, session_id, project):
    """Fetch flows of a project request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str host: Hostname where the request should go
    :param str session_id: An id that the user should have when is logged in
    :param str project: Project name whose flows will be fetched on Azkaban
    :return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """

    response = session.get(
        host + '/manager',
        params={
            u'session.id': session_id,
            u'ajax': 'fetchprojectflows',
            u'project': project
        }
    )

    logging.debug("Response: \n%s", response.text)

    return response


def fetch_projects_request(session, host, session_id, user):
    """Fetch all projects request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str host: Hostname where the request should go
    :param str session_id: An id that the user should have when is logged in
    :param user:
    :return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """
    if user is None:
        response = session.get(
            host + '/index?all',
            params={
                u'session.id': session_id
            }
        )
    else:
        response = session.get(
            host + '/index?ajax=fetchuserprojects',
            params={
                u'user': user,
                u'session.id': session_id
            }
        )

    logging.debug("Response: \n%s", response.text)

    return response


def fetch_all_projects_request(session, host, session_id):
    """Fetch all projects request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str host: Hostname where the request should go
    :param str session_id: An id that the user should have when is logged in
    :param user:
    :return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """
    response = session.get(
        host + '/index?all',
        params={
            u'session.id': session_id
        }
    )

    logging.debug("Response: \n%s", response.text)

    return response


def fetch_schedule_request(session, host, session_id, project_id, flow):
    """Fetch flow of a project request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str host: Hostname where the request should go
    :param str session_id: An id that the user should have when is logged in
    :param str project_id: Project ID whose flow schedule will be fetched on Azkaban
    :param str flow: Flow name whose schedule will be fetched on Azkaban
    :return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """

    response = session.get(
        host + '/schedule',
        params={
            u'session.id': session_id,
            u'ajax': 'fetchSchedule',
            u'projectId': project_id,
            u'flowId': flow
        }
    )

    logging.debug("Response: \n%s", response.text)

    return response


class SpyderAz(object):
    def __init__(self):
        # Session ignoring SSL verify requests
        session = requests.Session()
        session.verify = False
        urllib3.disable_warnings(InsecureRequestWarning)

        self.__session = session
        self.__host = None
        self.__user = None
        self.__session_id = None

    def __catch_response_status_error(self, exception, response_json):
        """ PRIVATE
        Verify error in response, catch response status.
        :raise: exception(error_msg), when error exists and status equals a error, with the 'error_msg'.
        """
        response_status = response_json.get('status')
        if response_status == u'error':
            error_msg = response_json[u'message']
            raise exception(error_msg)

    def __catch_response_error_msg(self, exception, response_json):
        """ PRIVATE
        Catches the error message when 'error' exists in the response keys.
        :raise: SessionError, when error_msg equals a 'sessions', or exception(error_msg).
        """
        if u'error' in response_json.keys():
            error_msg = response_json[u'error']
            if error_msg == "session":
                raise SessionError(error_msg)
            raise exception(error_msg)

    def __catch_empty_response(self, exception, response_json):
        """ PRIVATE
        Does not allow an empty response.
        :raise: exception
        """
        if response_json == {}:
            raise exception('Empty response')

    def __catch_login(self, response):
        """ PRIVATE
        Private method to call login_text and login_html from response.
        """
        self.__catch_login_text(response)
        self.__catch_login_html(response)

    def __catch_login_text(self, response):
        """ PRIVATE
        Do not allow an empty login attempt.
        :raise: SessionError("Login error. Need username and password")
        """
        if response.text == "Login error. Need username and password":
            raise SessionError(response.text)

    def __catch_login_html(self, response):
        """ PRIVATE
        Checks the content in the verification is in at least one line of the response.
        :raise: SessionError when content not in response lines.
        """
        if "  <script type=\"text/javascript\" src=\"/js/azkaban/view/login.js\"></script>" in \
                response.text.splitlines():
            raise SessionError(response.text)

    def __catch_response_error(self, response, exception, ignore_empty_responses=False):
        """ PRIVATE
        Try to get the answer json. If an error occurs, define response_json as an empty json, send it
        together with the input to the error functions.
        """
        self.__catch_login(response)

        # Some ajax api operations don"t have return body making response.json() raise a ValueError exception
        # The try block enable the __catch_empty_response raise the correct exception
        try:
            response_json = response.json()
        except Exception:
            response_json = {}

        self.__catch_response_error_msg(exception, response_json)
        self.__catch_response_status_error(exception, response_json)

        # Don't raise a exception if we know the request has a empty body
        if not ignore_empty_responses:
            self.__catch_empty_response(exception, response_json)

    def __validate_host(self, host):
        """ PRIVATE
        Receives a host and when the host ends with '/', will we return a host without the '/'.
        :param host:
        :return: host:
        :rtype: str:
        """
        valid_host = host

        while valid_host.endswith(u'/'):
            valid_host = valid_host[:-1]

        return valid_host

    def __check_if_logged(self):
        """ PRIVATE
        Checks if the instance created has a valid session.
        :raise: NotLoggedOnError when __session_id not exists.
        """
        if not self.__session_id:
            raise NotLoggedOnError()

    def get_logged_session(self):
        """
        Method for return the host and session id of the logged session saved on the class

        :return: A dictionary containing host, user and session_id as keys
        :rtype: dict
        """

        logged_session = {
            u'host': self.__host,
            u'user': self.__user,
            u'session_id': self.__session_id
        }

        return logged_session

    def set_logged_session(self, host, user, session_id):
        """
        Method for set host, user and session_id, attributes of the class

        :param str host: Azkaban hostname
        :param str user: Azkaban username
        :param str session_id: session.id received from a login request
        """

        self.__host = host
        self.__user = user
        self.__session_id = session_id

    def logout(self):
        """Logout command, intended to clear the host, user and session_id attributes from the instance"""

        self.set_logged_session(None, None, None)

    def login(self, host, user, password):
        """
        Login command, intended to make the request to Azkaban and treat the response properly

        This method validate the host, make the request to Azkaban, and evaluate the response. If host, user or
        password is wrong or could not connect to host, it returns false and do not change the host and session_id
        attribute from the class. If everything is fine, saves the new session_id and corresponding host as attributes
        in the class and returns True

        :param str host: Azkaban hostname
        :param str user: Username to login
        :param str password: Password from user
        :raises LoginError: when Azkaban api returns error in response
        """

        valid_host = self.__validate_host(host)
        #print(self.__session, valid_host, user, password)
        response = login_request(self.__session, valid_host, user, password)
        self.__catch_response_error(response, LoginError)

        response_json = response.json()
        self.set_logged_session(valid_host, user, response_json['session.id'])
        #print(response_json)
        logging.info('Logged as %s' % user)

    def fetch_flows(self, project):
        """
        Fetch flows command, intended to make the request to Azkaban and treat the response properly.

        This method receives the project name, makes the fetch flows request to fetch the flows
        and evaluates the response.

        If project is wrong or there is no session_id, it returns false. If everything is fine, returns
        True.

        :param str project: project name on Azkaban
        :raises FetchFlowsError: when Azkaban api returns error in response
        """

        self.__check_if_logged()

        response = fetch_flows_request(
            self.__session,
            self.__host,
            self.__session_id,
            project
        )

        self.__catch_response_error(response, FetchFlowsError)

        response_json = response.json()
        logging.info('Project ID: %s' % (response_json[u'projectId']))
        return response_json

    def fetch_jobs_from_flow(self, project, flow):
        """
        Fetch jobs of a flow command, intended to make the request to Azkaban and return
        the response.

        This method receives the project name and flow id, makes the fetch jobs of a flow request
        to fetch the jobs of a flow and evaluates the response.

        Returns the json response from the request.

        :param str project: project name on Azkaban
        :param str flow: flow id on Azkaban
        :raises FetchJobsFromFlowError: when Azkaban api returns error in response
        """

        self.__check_if_logged()

        response = self.__fetch_jobs_from_flow_request(
            self.__session,
            self.__host,
            self.__session_id,
            project,
            flow
        )

        self.__catch_response_error(response, FetchJobsFromFlowError)

        return response.json()

    def fetch_schedule(self, project_id, flow):
        """
        Fetch schedule command, intended to make the request to Azkaban and treat the response properly.

        This method receives the project id, flow name and optional execution options, makes the
        fetch schedule request to fetch the schedule of the flow and evaluates the response.

        If project_id or flow is wrong or there is no session_id, it returns false. If everything is fine, returns
        True.

        :param str project_id: project id on Azkaban
        :param str flow: flow name on Azkaban
        :raises FetchScheduleError: when Azkaban api returns error in response
        """

        self.__check_if_logged()

        response = fetch_schedule_request(
            self.__session,
            self.__host,
            self.__session_id,
            project_id,
            flow
        )

        self.__catch_response_error(response, FetchScheduleError)

        response_json = response.json()
        logging.info('Schedule ID: %s' % (response_json[u'schedule'][u'scheduleId']))
        return response_json

    def __fetch_projects(self):
        """
        Fetch all projects command, intended to make the request to Azkaban and treat the response properly.
        This method makes the fetch projects request to fetch all the projects and evaluates the response.
        """

        self.__check_if_logged()

        response = fetch_all_projects_request(
            self.__session,
            self.__host,
            self.__session_id
        )

        # The fetch projects request returns an html content, so we only catch login errors
        self.__catch_login(response)

        return response.text

    def parse_projects(self, text, user):
        def get_text(div):
            return div.find_all("a")[0].text

        def get_user(div):
            return div.find_all("p", {"class": "project-last-modified"})[0].text.split(" ")[-1].strip()[:-1]

        try:
            soup = BeautifulSoup(text, "html.parser")
            all_projects = soup.find_all("div", {"class": "project-info"})

            all_projects_for_user = [get_text(div) for div in all_projects if get_user(div) == user]

            logging.info("Found %d projects for user %s:" % (len(all_projects_for_user), user))
            for project in all_projects_for_user:
                logging.info("- %s" % (project))
        except Exception:
            raise FetchProjectsError("Error parsing response")
        return all_projects_for_user

    def fetch_projects(self, user):
        try:
            text = self.__fetch_projects()
            return self.parse_projects(text, user)
        except FetchProjectsError as e:
            logging.error(str(e))


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    az_user_dict = [#{'url': 'xxx', 'user': 'azkaban', 'passwd': 'xxx'},
                    #{'url': 'xxx', 'user': 'etl', 'passwd': 'xxx'},
                    {'url': 'https://xxx', 'user': 'hdp-ads-audit', 'passwd': 'xxx'},
                    #{'url': 'http://xxx, 'user': 'azkaban', 'passwd': 'xxx'},
                    ]
    sp = SpyderAz()
    for conf in az_user_dict:
        url = conf['url']
        user = conf['user']
        passwd = conf['passwd']
        sp.login(url, user, passwd)

        for project in sp.fetch_projects(user):
            fetch_flows = sp.fetch_flows(project)
            project_id = fetch_flows['projectId']
            for flow in fetch_flows['flows']:
                flow_name = flow['flowId']

                try:
                    sp.fetch_schedule(project_id, flow_name)
                    schedule = 1
                except Exception:
                    schedule = 0
                rs = f'"{url}","{user}","{project}","{flow_name}","{schedule}"'

                with open('azkaban_cli/jobs.csv', 'a', encoding='utf-8') as f:
                    f.write(str(rs) + '\n')

    sp.logout()
