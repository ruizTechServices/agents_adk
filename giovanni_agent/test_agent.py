import unittest
import requests
from unittest.mock import patch, MagicMock
from giovanni_agent.agent import get_website_text, ask_openai_agent

class TestAgent(unittest.TestCase):

    @patch('giovanni_agent.agent.requests.get')
    def test_get_website_text_success(self, mock_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><p>Hello World</p></body></html>'
        mock_get.return_value = mock_response

        # Call the function
        result = get_website_text('http://example.com')

        # Assert the result
        self.assertEqual(result['status'], 'success')
        self.assertIn('Hello World', result['report'])

    @patch('giovanni_agent.agent.requests.get')
    def test_get_website_text_failure(self, mock_get):
        # Mock a network error
        mock_get.side_effect = requests.exceptions.RequestException('Network error')

        # Call the function
        result = get_website_text('http://example.com')

        # Assert the result
        self.assertEqual(result['status'], 'error')
        self.assertIn('Network error', result['error_message'])

    @patch('giovanni_agent.agent.get_openai_response')
    def test_ask_openai_agent_success(self, mock_get_openai_response):
        # Mock the response from the OpenAI service
        mock_get_openai_response.return_value = {
            'status': 'success',
            'response': 'This is a test response.'
        }

        # Call the function
        result = ask_openai_agent('What is a test?')

        # Assert the result
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['response'], 'This is a test response.')

    @patch('giovanni_agent.agent.get_openai_response')
    def test_ask_openai_agent_failure(self, mock_get_openai_response):
        # Mock an error from the OpenAI service
        mock_get_openai_response.side_effect = Exception('API error')

        # Call the function
        result = ask_openai_agent('What is a test?')

        # Assert the result
        self.assertEqual(result['status'], 'error')
        self.assertIn('An unexpected error occurred: API error', result['error_message'])

if __name__ == '__main__':
    unittest.main()
