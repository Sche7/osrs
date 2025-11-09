from runescape.discord.webhook import generate_message
from runescape.utils.osrs import evaluate_hiscore_progress
from src.runescape.storage.json import JSONStorage


def test_generate_message():
    """Test the generate_message function."""
    json_storage = JSONStorage()
    stats = json_storage.load("tests/data/Zehahandsome.json")

    # Simply test that the function runs without errors
    progress = evaluate_hiscore_progress(stats)
    message = generate_message(progress)
    assert "Total level up from 973 -> 974" in message
