from .test_setup import TestSetUp
from ..models import User

class TestViews(TestSetUp):
    def test_register_user_without_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code,400)

    def test_register_user_with_data(self):
        res = self.client.post(self.register_url,self.user_data,format="json")
        self.assertEqual(res.data['email'],self.user_data['email'])
        self.assertEqual(res.status_code,201)

    def test_login_user_with_data(self):
        response = self.client.post(self.register_url,self.user_data,format="json")
        res = self.client.post(self.login_url,self.user_data,format="json")
        self.assertEqual(res.status_code,200)