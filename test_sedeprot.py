import pytest

from sedeprot import *


def test_empty_votes():
    dp = DecisionProcess(participants=["a", "b"])
    assert dp.check_consent() == (0, None, None)


def test_already_voted():
    dp = DecisionProcess(participants=["a", "b"])
    dp.add_vote("a", "foo")
    with pytest.raises(AlreadyVotedError):
        dp.add_vote("a", "bar")


def test_duplicate_vote():
    dp = DecisionProcess(participants=["a", "b"])
    dp.add_vote("a", "foo")
    dp.add_vote("b", "bar")
    assert dp.check_consent() == (1, None, None)
    with pytest.raises(DuplicateError):
        dp.add_vote("a", "foo")


def test_invalid_name():
    dp = DecisionProcess(participants=["a", "b"])
    with pytest.raises(KeyError):
        dp.add_vote("c", "foo")


def test_invalid_value():
    dp = DecisionProcess(participants=["a", "b"], valid_answers=["foo", "bar"])
    dp.add_vote("a", "foo")
    dp.add_vote("b", "bar")
    assert dp.check_consent() == (1, None, None)
    with pytest.raises(ValueError):
        dp.add_vote("a", "baz")


def test_simple_consent():
    dp = DecisionProcess(participants=["a", "b"])
    dp.add_vote("a", "foo")
    assert dp.check_consent() == (0, None, None)
    dp.add_vote("b", "foo")
    assert dp.check_consent() == (0, 0, ["foo"])


def test_complex_consent():
    dp = DecisionProcess(participants=["a", "b", "c"])
    dp.add_vote("a", "a")
    dp.add_vote("b", "p")
    dp.add_vote("c", "x")
    assert dp.check_consent() == (1, None, None)
    dp.add_vote("a", "x")
    dp.add_vote("b", "a")
    dp.add_vote("c", "y")
    assert dp.check_consent() == (2, None, None)
    dp.add_vote("a", "b")
    dp.add_vote("b", "q")
    dp.add_vote("c", "b")
    assert dp.check_consent() == (3, None, None)
    dp.add_vote("a", "y")
    dp.add_vote("b", "b")
    dp.add_vote("c", "a")
    assert dp.check_consent() == (3, 4, ["a"])


def test_multi_consent():
    dp = DecisionProcess(participants=["a", "b"])
    dp.add_vote("a", "foo")
    dp.add_vote("b", "bar")
    assert dp.check_consent() == (1, None, None)
    dp.add_vote("a", "bar")
    dp.add_vote("b", "foo")
    round, score, value = dp.check_consent()
    assert round == 1
    assert score == 1
    assert set(value) == {"foo", "bar"}


def test_get_votes_all():
    dp = DecisionProcess(participants=["a", "b"])
    dp.add_vote("a", "foo")
    dp.add_vote("b", "bar")
    assert dp.check_consent() == (1, None, None)
    dp.add_vote("a", "bar")
    dp.add_vote("b", "foo")
    assert dp.get_votes() == {"a": ["foo", "bar"], "b": ["bar", "foo"]}


def test_get_votes_single():
    dp = DecisionProcess(participants=["a", "b"])
    dp.add_vote("a", "foo")
    dp.add_vote("b", "bar")
    assert dp.check_consent() == (1, None, None)
    dp.add_vote("a", "bar")
    dp.add_vote("b", "foo")
    assert dp.get_votes("a") == {"a": ["foo", "bar"]}


def test_get_votes_empty_all():
    dp = DecisionProcess(participants=["a", "b"])
    assert dp.get_votes() == {"a": [], "b": []}


def test_get_votes_empty_single():
    dp = DecisionProcess(participants=["a", "b"])
    assert dp.get_votes("a") == {"a": []}


def test_get_votes_invalid_value():
    dp = DecisionProcess(participants=["a", "b"])
    with pytest.raises(KeyError):
        dp.get_votes("c")


def test_duplicate_participants():
    dp = DecisionProcess(participants=["a", "a"])
    assert dp.get_votes() == {"a": []}
