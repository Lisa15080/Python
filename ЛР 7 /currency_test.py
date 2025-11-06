import unittest
import io
import requests

from get_currency import get_currencies
from decorators import trace


class TestTraceStream(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_count = 0

    def setUp(self):
        self.stream_buffer = io.StringIO()
        self.traced_func = trace(get_currencies, handle=self.stream_buffer)

    def test_stream_output_on_error(self):
        with self.assertRaises(requests.exceptions.RequestException):
            self.traced_func(['USD'], url="https://")

        # сюда программа попадёт только после исключения
        self.error_count += 1

        self.assertEqual(
            self.stream_buffer.getvalue().count("Ошибка при запросе к API: "),
            self.error_count
        )

    def tearDown(self):
        # освобождаем ресурсы
        self.stream_buffer.close()
        del self.stream_buffer
