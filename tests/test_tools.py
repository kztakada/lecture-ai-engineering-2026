"""ツールのテスト（LLMもAPIキーも使わない）。"""

import json

from app import tools


def test_glossary_ids_are_unique_and_related_links_exist():
    terms = tools.load_glossary()
    ids = [t["id"] for t in terms]
    assert len(ids) == len(set(ids))
    for t in terms:
        for r in t["related"]:
            assert r in ids, f"{t['id']} の related に存在しない id: {r}"


def test_search_finds_term_by_name_and_alias():
    for query in ["LoRA", "lora", "Low-Rank Adaptation"]:
        hits = json.loads(tools.search_glossary(query))
        assert hits[0]["term"] == "LoRA", query


def test_search_finds_course_specific_term():
    hits = json.loads(tools.search_glossary("lecNN-start"))
    assert hits[0]["term"] == "lecNN-start タグ"


def test_search_limits_number_of_results():
    hits = json.loads(tools.search_glossary("エージェント"))
    assert 1 <= len(hits) <= tools.MAX_RESULTS


def test_search_reports_not_found():
    assert "見つかりませんでした" in tools.search_glossary("存在しない用語xyz")


def test_lecture_summary():
    assert "エージェント" in tools.get_lecture_summary(3)
    assert "まだありません" in tools.get_lecture_summary(99)


def test_default_question_of_lecture1_is_answerable_from_glossary():
    """第1回の既定の質問（app.ask）は、第3回のエージェントが用語集で正しく答えられること。"""
    from app.ask import DEFAULT_QUESTION

    assert "3レベル" in DEFAULT_QUESTION
    hits = json.loads(tools.search_glossary("3レベル"))
    assert hits[0]["term"] == "宿題の3レベル"


def test_quiz_is_generated_for_lecture2():
    """第2回の確認問題が生成されること。"""
    quiz = json.loads(tools.make_quiz(2))
    lecture_terms = [term for term in tools.load_glossary() if term["lecture"] == 2]

    assert set(quiz) == {"question", "answer"}
    assert quiz["question"].startswith("「")
    assert quiz["question"].endswith("」の意味は？")
    selected_term = quiz["question"][1:-6]
    expected = next(term for term in lecture_terms if term["term"] == selected_term)
    assert quiz["answer"] == expected["definition"]


def test_learning_log_is_saved(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "LEARNING_LOG_DIR", tmp_path)

    result = tools.save_learning_log("今日の学び")

    logs = list(tmp_path.glob("*.md"))
    assert len(logs) == 1
    assert logs[0].read_text(encoding="utf-8") == "今日の学び"
    assert str(logs[0]) in result


def test_all_tools_handle_dummy_arguments_without_api_key():
    """全ツールがAPIキーなしで、存在しない回や空の入力を処理できること。"""
    assert "検索語が空です" in tools.search_glossary("")
    assert "まだありません" in tools.get_lecture_summary(0)
    assert "用語が見つかりません" in tools.make_quiz(0)
