# encoding: utf-8
import base64
import json
import logging

import requests

from ssrd import const

base = const.MediaUrl
logger = logging.getLogger("default")
default_type = "default"


def get_password(project):
    return base64.b64encode(f"{project.name}".encode("utf8")).decode("utf8")


def get_project(name):
    from ssrd.users.models import Project

    return Project(name=name)


def log_request(method, url, kwargs):
    logger.info("{:-^70}".format("Request begin"))
    logger.info("Request:")
    logger.info("{method} {url}".format(method=method.upper(), url=url))
    logger.info("kwargs: {kwargs}".format(kwargs=kwargs))


def log_response(response):
    logger.info("Response: %s" % response.text)
    logger.info("{:-^70}\n\n\n".format("Request done"))


class External(object):
    """
    请求外部api用的类
    """

    @staticmethod
    def get(url, **kwargs):
        return External.warpper("get", url, **kwargs)

    @staticmethod
    def post(url, **kwargs):
        return External.warpper("post", url, **kwargs)

    @staticmethod
    def warpper(method, url, **kwargs):
        # kwargs.update(verify=False)  # 不校验ssl证书
        try:
            response = result = getattr(requests, method)(url, **kwargs)
        except requests.exceptions.RequestException:
            from traceback import format_exc

            log_request(method, url, kwargs)
            logger.error("Request exception: \n%s" % format_exc())
            return dict()

        try:
            result = json.loads(response.text)
        except Exception:
            if response.status_code in (200, 403, 500):
                return response.text
            log_request(method, url, kwargs)
            from traceback import format_exc

            logger.error("Json error:%s" % format_exc())
            result = {}
        log_response(response)

        return result


class Api(object):
    resource = base + "/api/resource"
    users = base + "/api/users/"
    auth = base + "/api/auth/get"


class BaseFileBrowser(object):
    def create(self, path):
        return External.post(f"{Api.resource}/{path}", headers=self.headers)

    def list(self, path):
        return External.get(f"{Api.resource}/{path}", headers=self.headers)

    def auth(self, project=None, identify=None):
        if project:
            identify = {"username": project.name, "password": get_password(project)}
        return "Bearer " + External.get(f"{Api.auth}", json=identify)

    def deleteFile(self, path):
        pass

    def createUser(self, project):
        token = self.auth(identify=dict(username="admin", password="admin"))
        data = {
            "what": "user",
            "which": "new",
            "data": {
                "ID": 0,
                "admin": False,
                "allowCommands": True,
                "allowEdit": True,
                "allowNew": True,
                "allowPublish": True,
                "lockPassword": False,
                "commands": [""],
                "css": "",
                "locale": "",
                "password": get_password(project),
                "rules": [],
                "filesystem": f"/srv/{project.name}",
                "username": f"{project.name}",
                "viewMode": "mosaic",
            },
        }
        return External.post(f"{Api.users}", headers={"Authorization": token}, json=data)

    #  def createFile(self, project, type, file):
    #  token = self.auth(project)
    #  data = file.read()
    #  length = len(data)
    #  return requests.post(
    #  f"{Api.resource}/{type}/{file.name}", data=data,
    #  headers={"Authorization": token, "Content-Length": f"{length}"},
    #  )
    def downloadFile(self, name):
        pass

    def getFileUrl(self, name):
        pass

    def getFileMeta(self, name):
        return self.getFile(name)

    def createFile(self, name, content):
        from ssrd.users.models import Project

        type = default_type
        project = get_project(name)
        token = self.auth(project)
        External.post(f"{Api.resource}/{type}/", headers={"Authorization": token})
        return External.post(f"{Api.resource}/{type}/{name}", data=content.file, headers={"Authorization": token})

    def createDirectory(self, project, name):
        token = self.auth(project)
        return External.post(f"{Api.resource}/{name}", headers={"Authorization": token, "Content-Length": "0"})

    #  def getFile(self, project, directory, attatchment):
    #  token = self.auth(project)
    #  directory = dict(const.DOCUMENTS).get(type, "")
    #  api = f"{Api.resource}/{project.name}/{directory}/{file.name}"
    #  resposne = requests.get(api, headers={"Authorization": token}).json()
    #  resposne["url"] = base + resposne["url"]
    #  return resposne
    def getFile(self, name):
        name = name.split("/")[-1]  # /Users/mum5/Documents/repo/ssrd/asd -> asd
        from ssrd.users.models import Project

        project = get_project(name)
        self.createUser(project)
        token = self.auth(project)
        directory = dict(const.DOCUMENTS).get(type, default_type)
        api = f"{Api.resource}/{directory}/{name}"
        response = External.get(api, headers={"Authorization": token})
        if response.get("url"):
            response["url"] = base + response["url"]
            return response
        return


FileBrowser = BaseFileBrowser()
