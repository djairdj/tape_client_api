import json
import requests
class GetURL:
    """Class to manage URL operations using a token and an app ID."""

    def __init__(self, token: str, app_id: int):
      self._token: str = token
      self._app_id: int = app_id
      self._url_base_tape: str = 'https://api.tapeapp.com/v1/'
      self._headers: dict = {'Authorization': f'Bearer {self._token}'}
      self._org_url: str = self._get_org_url()
      self._workspace_external_id, self._workspace_id = self._set_workspace_external_id_workspace_id()
      self._workspace_slug: str = self._get_workspace_slug()

    def _call_api(self, sufix: str) -> dict:
      url = f'{self._url_base_tape}{sufix}'
      response = requests.get(url, headers=self._headers)
      response.raise_for_status()
      if response.status_code != 200:
        print(f"Deu ruim:\n{json.dumps(response.json())}")
      data: dict = response.json()
      return data

    def _get_org_url(self) -> str:
      data: dict = self._call_api(sufix='org')
      org_url: str = data.get('url', '')
      return org_url

    def _set_workspace_external_id_workspace_id(self) -> tuple[str, str]:
      data = self._call_api(sufix= f'app/{self._app_id}')

      workspace_external_id: str = data.get('external_id', '') # O nome do workspace filho
      workspace_id: str = data.get('workspace_id', '')
      return workspace_external_id, workspace_id

    def _get_workspace_slug(self) -> str:
      data: dict = self._call_api(sufix=f'workspace/{self._workspace_id}')
      workspace_slug: str = data.get('slug', '')
      return workspace_slug

    def get_url(self) -> str:
      result: str = f"{self._org_url}/workspaces/{self._workspace_slug}/apps/{self._workspace_external_id}"
      return result

if __name__ == '__main__':
    token = "user___token"
    app_id = 55
    if any(v for v in [token, app_id] if v == None):
      token = input("Digite o Token: ")
      app_id = int(input("Digite o App ID: "))

    url = GetURL(token, app_id).get_url()
    print(f'Segure ctrl e click em cima da url abaixo:\n{url}\n{"-" * len(url)}')

