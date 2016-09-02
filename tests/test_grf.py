import json
import pytest
from pygrf import open_grf


class TestHeader:

    def test_header_has_correct_data(self, data_files):
        with open(data_files['grf_info.json']) as info_file:
            file_info = json.load(info_file)

        for name, info in file_info.items():
            with open_grf(data_files[name]) as grf_file:
                header = grf_file.header
            assert header.allow_encryption == info['allow_encryption']
            assert header.index_offset == info['index_offset']
            assert header.file_count == info['file_count']
            assert header.version == info['version']

    @pytest.mark.parametrize('filename', (
        'invalid_watermark.grf', 'invalid_encryption.grf',
        'invalid_version.grf', 'invalid_filecount.grf'
    ))
    def test_raise_value_error_bad_header(self, data_files, filename):
        with pytest.raises(ValueError):
            open_grf(data_files[filename])


class TestIndex:

    @pytest.mark.parametrize('filename', ('a.grf', 'ab.grf'))
    def test_index_has_correct_count(self, data_files, filename):
        with open_grf(data_files[filename]) as grf_file:
            assert len(grf_file.index) == grf_file.header.file_count

    @pytest.mark.parametrize('filename, files', (
        ('a.grf', ['data\\a.txt']), ('ab.grf', ['data\\a.txt', 'data\\b.dat'])
    ))
    def test_index_get_file(self, data_files, filename, files):
        with open_grf(data_files[filename]) as grf_file:
            for f in files:
                assert f in grf_file.index


class TestFileHeader:

    def test_header_has_correct_data(self, data_files):
        with open(data_files['file_info.json']) as info_file:
            file_info = json.load(info_file)
        with open_grf(data_files['ab.grf']) as grf_file:
            for name, size_info in file_info.items():
                info = file_info[name]
                f = grf_file.get(name)

        assert f.header.archived_size == info['archived']
        assert f.header.archived_size == info['archived']
        assert f.header.compressed_size == info['compressed']
        assert f.header.real_size == info['real']
        assert f.header.position == info['position']
        assert f.header.flag == info['flag']
