import os
import sys
import pytest
from unittest import mock
from airflow.models import Variable, Connection,DagBag

@pytest.fixture
def api_key():
    with mock.patch.dict("os.environ", AIRFLOW_VAR_API_KEY="NEW_MOCK_KEY"):
        yield Variable.get("API_KEY")


@pytest.fixture
def channel_handle():
    with mock.patch.dict("os.environ", AIRFLOW_VAR_CHANNEL_HANDLER="VanillaImpact"):
        yield Variable.get("CHANNEL_HANDLER")



@pytest.fixture
def mock_postgres_conn_vars():
    conn = Connection(
        login="mock_username",
        password="mock_password",
        host="mock_host",
        port=1234,
        schema="mock_db_name"
    )
    conn_uri = conn.get_uri()

    with mock.patch.dict("os.environ", AIRFLOW_CONN_POSTGRES_CONN_USERNAME=conn_uri):
        yield Connection.get_connection_from_secrets(conn_id="POSTGRES_CONN_USERNAME")



@pytest.fixture
def dagbag():
    dags_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dags'))
    if dags_path not in sys.path:
        sys.path.insert(0, dags_path)
    yield DagBag()