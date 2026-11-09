"""test_api.py

Unit tests for FastAPI app and routes.
"""

from contextlib import contextmanager

from pydantic import TypeAdapter
import pytest
from fastapi.testclient import TestClient

from morpheus_python_api.api.main import app
from morpheus_python_api.models import CrunchOptions
from morpheus_python_api.types import (
    POS,
    Case,
    Deriv,
    Gender,
    Language,
    Mood,
    MorphParse,
    Num,
    Person,
    StemType,
    Tense,
    WordParse,
    Voice,
)


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def simple_opts():
    return CrunchOptions(language=Language.GREEK)


def test_crunch_text(client: TestClient, simple_opts: CrunchOptions):
    type_adapter = TypeAdapter(WordParse)
    # test unparsable input
    result = client.get(
        "/crunch_text/",
        params={
            "text": "abcd",
            "raise_on_failure": True,
            **simple_opts.model_dump(mode="json"),
        },
    )
    assert result.status_code == 422

    result = client.get(
        "/crunch_text/", params={"text": "abcd", "raise_on_failure": False}
    )
    assert result.status_code == 200

    # test for error on multiple inputs
    input_str = "lo/gos\nlu/w"
    result = client.get(
        "/crunch_text/",
        params={
            "text": input_str,
            "raise_on_failure": False,
            **simple_opts.model_dump(mode="json"),
        },
    )
    assert result.status_code == 422

    input_str = "lo/gos"
    result = client.get(
        "/crunch_text/",
        params={
            "text": input_str,
            "raise_on_failure": True,
            **simple_opts.model_dump(mode="json"),
        },
    )
    assert result.status_code == 200
    word_result = type_adapter.validate_python(result.json())
    parses = [
        MorphParse(
            language=Language.GREEK,
            pos=POS.NOUN,
            dict_forms=["λόγος"],
            case=frozenset((Case.NOM,)),
            num=frozenset((Num.SG,)),
            gender=frozenset((Gender.MASC,)),
            stem_type=StemType.OS_OU,
        )
    ]
    assert word_result == WordParse(lemma="λόγος", parses=parses)


@contextmanager
def _crunch_ws(client: TestClient, opts: CrunchOptions):
    with client.websocket_connect("/ws/crunch") as ws:
        ws.send_json(opts.model_dump(mode="json"))
        yield ws


def test_ws_crunch(client: TestClient, simple_opts: CrunchOptions):
    type_adapter = TypeAdapter(WordParse)
    words = ["lo/gos", "dei/knumi"]
    with _crunch_ws(client, simple_opts) as ws:
        for word in words:
            ws.send_text(word)
        msgs = [ws.receive_json() for _ in words]
        parses_logos = [
            MorphParse(
                language=Language.GREEK,
                pos=POS.NOUN,
                dict_forms=["λόγος"],
                case=frozenset((Case.NOM,)),
                num=frozenset((Num.SG,)),
                gender=frozenset((Gender.MASC,)),
                stem_type=StemType.OS_OU,
            ),
        ]
        parses_deiknumi = [
            MorphParse(
                language=Language.GREEK,
                pos=POS.VERB,
                dict_forms=["δείκνυ—μι", "δείκνυμι"],
                num=frozenset((Num.SG,)),
                tense=frozenset((Tense.PRES,)),
                mood=frozenset((Mood.IND,)),
                voice=frozenset((Voice.ACT,)),
                person=frozenset((Person.FIRST,)),
                stem_type=StemType.UMI_PR,
                deriv=Deriv.NUMI,
            ),
        ]
        assert [m["type"] for m in msgs] == ["structured", "structured"]
        assert [m["word"] for m in msgs] == words
        logos_results = type_adapter.validate_python(msgs[0]["parse"])
        assert logos_results == WordParse(lemma="λόγος", parses=parses_logos)
        deiknumi_results = type_adapter.validate_python(msgs[1]["parse"])
        assert deiknumi_results == WordParse(
            lemma="δείκνυμι", parses=parses_deiknumi
        )
