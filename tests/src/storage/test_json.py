from src.storage.json import JSONStorage


def test_save_and_load(tmp_path):
    json_storage = JSONStorage()

    filepath = tmp_path / "test.json"

    data = {"test": "test"}

    json_storage.save(data, filepath)

    loaded_data = json_storage.load(filepath)

    assert data == loaded_data
