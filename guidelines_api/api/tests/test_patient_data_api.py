from django.test import LiveServerTestCase
from rest_framework.test import RequestsClient


class PatientGuidelineTest(LiveServerTestCase):

    serialized_rollback = True

    def test_get_all_patient_data(self):
        client = RequestsClient()
        response = client.get('%s%s' % (self.live_server_url, '/patientdata/'))
        json = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json['count'], 50)

    def test_get_single_patient_data(self):
        client = RequestsClient()
        response = client.get('%s%s' % (self.live_server_url, '/patientdata/'))
        json = response.json()
        first_patient = json['results'][0]
        patient_data_id = first_patient['id']
        print('%s:%s' % ('Patient Data Id', patient_data_id))

        url = '%s%s%s/' % (self.live_server_url, '/patientdata/', patient_data_id)
        response = client.get(url)
        json = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(json['name'])
        self.assertIsNotNone(json['date'])
        self.assertIsNotNone(json['gender'])
        self.assertIsNotNone(json['systolic_BP'])
        self.assertIsNotNone(json['diastolic_BP'])
        self.assertIsNotNone(json['smoking_years'])
        self.assertIsNotNone(json['no_of_packs'])
        self.assertIsNotNone(json['fasting_blood_sugar'])
        self.assertIsNotNone(json['hypothyroid'])
        self.assertIsNotNone(json['obese'])
        self.assertIsNotNone(json['intravenous_drug_abuse'])

    def test_get_patient_data_by_name(self):
        client = RequestsClient()
        name = 'Tandie Shapero'
        response = client.get('%s%s%s' % (self.live_server_url, '/patientdata?name=', name))
        json = response.json()
        self.assertEquals(response.status_code, 200)

        matching_patient = json['results'][0]
        self.assertEquals(json['count'], 1)

        self.assertEquals(matching_patient['name'], 'Tandie Shapero')
        self.assertEquals(matching_patient['gender'], 'Female')
        self.assertEquals(matching_patient['systolic_BP'], 274)
        self.assertEquals(matching_patient['diastolic_BP'], 96)
        self.assertEquals(matching_patient['smoking_years'], 49)
        self.assertEquals(matching_patient['no_of_packs'], 4)
        self.assertEquals(matching_patient['fasting_blood_sugar'], 195)
        self.assertEquals(matching_patient['hypothyroid'], True)
        self.assertEquals(matching_patient['obese'], True)
        self.assertEquals(matching_patient['intravenous_drug_abuse'], False)
