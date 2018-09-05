# encoding: utf-8
import requests

from ssrd import const
from ssrd.contrib import APIView, UnAuthView, V, ViewSet


base = const.MediaUrl


class Api(object):
    resource = base + "/api/resource/"
    users = base + "/api/users/"
    auth = base + "/api/auth/get"


class BaseFileBrowser(object):
    def create(self, path):
        return requests.post(f"{Api.resource}/{path}", headers=self.headers)

    def list(self, path):
        return requests.get(f"{Api.resource}/{path}", headers=self.headers)

    def auth(self, project=None, identify=None):
        if project:
            identify = {"username": project.name, "password": f"{project.id}"}
        return requests.get(f"{Api.auth}", json=identify).text

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
                "password": f"{project.id}",
                "rules": [],
                "filesystem": f"/srv/{project.name}",
                "username": f"{project.name}",
                "viewMode": "mosaic",
            },
        }
        return requests.post(
            f"{Api.users}", headers={"Authorization": token}, json=data
        )

    def createFile(self, project, type, file):
        directory = dict(const.DOCUMENTS).get(type, "")
        self.createDirectory(project, directory)
        with open(f"files/{project.name}/{directory}/{file.name}", "wb") as fd:
            fd.write(file.read())

    def createDirectory(self, project, name):
        token = self.auth(project)
        return requests.post(
            f"{Api.resource}/{name}",
            headers={"Authorization": token, "Content-Length": "0"},
        )

    def getFile(self, project, directory, attatchment):
        token = self.auth(project)
        directory = dict(const.DOCUMENTS).get(type, "")
        api = f"{Api.resource}/{project.name}/{directory}/{file.name}"
        resposne = requests.get(api, headers={"Authorization": token}).json()
        resposne["url"] = base + resposne["url"]
        return resposne


FileBrowser = BaseFileBrowser()
