import os
import requests
from typing import Dict, Any, Tuple


class TapeAPIClient:
    """Cliente HTTP dedicado para interagir com a API do Tape."""

    BASE_URL = "https://api.tapeapp.com/v1/"

    def __init__(self, token: str):
        self._headers = {"Authorization": f"Bearer {token}"}

    def call_api(self, suffix: str) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{suffix}"
        response = requests.get(url, headers=self._headers)
        response.raise_for_status()  # Lança exceção em caso de erro HTTP (4xx ou 5xx)
        return response.json()


class TapeURLResolver:
    """Classe responsável por resolver a URL final do app no Tape."""

    def __init__(self, org_url: str, workspace_slug: str, app_external_id: str):
        self.org_url = org_url
        self.workspace_slug = workspace_slug
        self.app_external_id = app_external_id

    @classmethod
    def from_api(cls, token: str, app_id: int) -> "TapeURLResolver":
        """Método Fábrica: busca os dados necessários da API e retorna a instância limpa."""
        client = TapeAPIClient(token)

        # 1. Busca URL da Org
        org_data = client.call_api("org")
        org_url = org_data.get("url", "")

        # 2. Busca dados do App para obter o workspace_id e o external_id
        app_data = client.call_api(f"app/{app_id}")
        app_external_id = app_data.get("external_id", "")
        workspace_id = app_data.get("workspace_id")

        if not workspace_id:
            raise ValueError(f"Workspace ID não encontrado para o app {app_id}")

        # 3. Busca dados do Workspace para obter o slug
        workspace_data = client.call_api(f"workspace/{workspace_id}")
        workspace_slug = workspace_data.get("slug", "")

        return cls(org_url, workspace_slug, app_external_id)

    def get_url(self) -> str:
        """Monta a URL formatada."""
        return f"{self.org_url}/workspaces/{self.workspace_slug}/apps/{self.app_external_id}"


if __name__ == "__main__":
    # Usando variável de ambiente ou solicitando input caso não exista
    token = os.getenv("TAPE_TOKEN") or input("Digite o Token: ")
    try:
        app_id = int(os.getenv("TAPE_APP_ID") or input("Digite o App ID: "))
    except ValueError:
        print("Erro: App ID deve ser um número inteiro.")
        exit(1)

    try:
        resolver = TapeURLResolver.from_api(token, app_id)
        url = resolver.get_url()
        print(f"\nSegure ctrl e clique no link abaixo:\n{url}")
        print("-" * len(url))
    except requests.RequestException as e:
        print(f"Erro na comunicação com a API: {e}")
