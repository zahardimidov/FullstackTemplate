from fastapi.testclient import TestClient
from logging import Logger

def test_root(client: TestClient):
    response = client.get("/ping")

    assert response.status_code == 200


def test_signup(client: TestClient, logger: Logger):
    data = dict(
        name = 'Захар',
        email = 'zahardimidov@mail.ru',
        password = '02032007AA!!aa',
        password_repeat = '02032007AA!!aa'
    )

    response = client.post('/api/user/auth/sign-up', json=data)

    logger.info(response.json())

    assert response.status_code == 200

