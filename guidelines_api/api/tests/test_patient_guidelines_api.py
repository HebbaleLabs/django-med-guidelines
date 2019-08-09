from django.test import LiveServerTestCase
from rest_framework.test import RequestsClient


class PatientGuidelineTest(LiveServerTestCase):

    serialized_rollback = True

    def test_get_all_patient_recommendations(self):
        client = RequestsClient()
        response = client.get('%s%s' % (self.live_server_url, '/patientguidelines/'))
        self.assertEquals(response.status_code, 200)

        json = response.json()
        self.assertEquals(json['count'], 1000)

    def test_get_single_patient_recommendations(self):
        client = RequestsClient()
        response = client.get('%s%s' % (self.live_server_url, '/patientguidelines/'))
        self.assertEquals(response.status_code, 200)

        json = response.json()
        self.assertEquals(json['count'], 1000)
        first_patient_recommendation = json['results'][0]
        patient_guideline_id = first_patient_recommendation['id']

        url = '%s%s%s/' % (self.live_server_url, '/patientguidelines/', patient_guideline_id)
        response = client.get(url)
        self.assertEquals(response.status_code, 200)

        json = response.json()
        self.assertIsNotNone(json['patient'])
        self.assertIsNotNone(json['recommendations'])

    def test_get_patient_recommendations_by_name(self):
        client = RequestsClient()
        name = 'Tandie Shapero'
        response = client.get('%s%s%s' % (self.live_server_url, '/patientguidelines?name=', name))
        json = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json['count'], 1)

        matching_patient = json['results'][0]
        self.assertIsNotNone(matching_patient['patient'])
        self.assertIsNotNone(matching_patient['recommendations'])
        self.assertEqual(len(matching_patient['recommendations']), 5)
