import unittest
from unittest.mock import patch
from main import app


class TestMain(unittest.TestCase):

  def test_tvl_endpoint(self):
    with app.test_client() as client:
      resp = client.get('/tvl')
      self.assertEqual(resp.status_code, 200)

  def test_firm_endpoint(self):
    with app.test_client() as client:
      resp = client.get('/firm')
      self.assertEqual(resp.status_code, 200)

  def test_positions_endpoint(self):
    with app.test_client() as client:
      resp = client.get('/positions')
      self.assertEqual(resp.status_code, 200)

  def test_dbr_price_endpoint(self):
    with app.test_client() as client:
      resp = client.get('/dbr_price')
      self.assertEqual(resp.status_code, 200)

  def test_dbr_policy_endpoint(self):
    with app.test_client() as client:
      resp = client.get('/dbr_policy')
      self.assertEqual(resp.status_code, 200)

  def test_tvl_firm_endpoint(self):
    with app.test_client() as client:
      resp = client.get('/tvl_firm')
      self.assertEqual(resp.status_code, 200)

  def test_dbr_issue_endpoint(self):
    with app.test_client() as client:
      resp = client.get('/dbr_issue')
      self.assertEqual(resp.status_code, 200)

  def test_inv_stake_endpoint(self):
    with app.test_client() as client:
      resp = client.get('/inv_stake')
      self.assertEqual(resp.status_code, 200)

  def test_dbr_inv_endpoint(self):
    with app.test_client() as client:
      resp = client.get('/dbr_inv')
      self.assertEqual(resp.status_code, 500)


if __name__ == '__main__':
  unittest.main()
