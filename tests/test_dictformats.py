from vocabsieve.dictformats import dictinfo


def test_dictinfo_kaikki_jsonl():
    info = dictinfo("testdata/kaikki/kaikki.org-dictionary-English-by-pos-postp.jsonl")

    assert info == {
        "basename": "kaikki.org-dictionary-English-by-pos-postp",
        "path": "testdata/kaikki/kaikki.org-dictionary-English-by-pos-postp.jsonl",
        "type": "wiktdump",
    }

def test_dictinfo_kaikki_jsonl_gz():
    info = dictinfo("testdata/kaikki/kaikki.org-dictionary-English-by-pos-postp.jsonl.gz")

    assert info == {
        "basename": "kaikki.org-dictionary-English-by-pos-postp",
        "path": "testdata/kaikki/kaikki.org-dictionary-English-by-pos-postp.jsonl.gz",
        "type": "wiktdump",
    }
