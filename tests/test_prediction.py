# Test Cases for Predictions
import pytest
from flask import json

# Consistency Test + GET API Test for Predictions
@pytest.mark.parametrize("predConsistencyList",
    [
        [['Highend Price', 'std', 168.8, 2548, 111, 88.6, 'sedan', 'rwd', 'dohc', 64.1, 130, 3.47, 'four', 23.7],
         ['Highend Price', 'std', 168.8, 2548, 111, 88.6, 'sedan', 'rwd', 'dohc', 64.1, 130, 3.47, 'four', 23.7],
         ['Highend Price', 'std', 168.8, 2548, 111, 88.6, 'sedan', 'rwd', 'dohc', 64.1, 130, 3.47, 'four', 23.7]],
        [['Medium Price', 'turbo', 150, 2000, 100, 90, 'convertible', 'fwd', 'rotor', 60, 100, 2.50, 'two', 20],
         ['Medium Price', 'turbo', 150, 2000, 100, 90, 'convertible', 'fwd', 'rotor', 60, 100, 2.50, 'two', 20],
         ['Medium Price', 'turbo', 150, 2000, 100, 90, 'convertible', 'fwd', 'rotor', 60, 100, 2.50, 'two', 20]],
        [['Budget Price', 'std', 200, 3000, 200, 120, 'sedan', '4wd', 'rotor', 70, 200, 4, 'six', 30],
         ['Budget Price', 'std', 200, 3000, 200, 120, 'sedan', '4wd', 'rotor', 70, 200, 4, 'six', 30],
         ['Budget Price', 'std', 200, 3000, 200, 120, 'sedan', '4wd', 'rotor', 70, 200, 4, 'six', 30]]     
    ]
)
def test_predict_GET_API(client, predConsistencyList, capsys):
    with capsys.disabled():
        predictedOutput = []
        for predictions in predConsistencyList:
            data = {
            'carsprice_range' : predictions[0],
            'aspiration' : predictions[1],
            'carlength' : predictions[2],
            'curbweight' : predictions[3],
            'horsepower' : predictions[4],
            'wheelbase' :predictions[5],
            'carbody' : predictions[6],
            'drivewheel' : predictions[7],
            'enginetype' : predictions[8],
            'carwidth' : predictions[9],
            'enginesize' : predictions[10],
            'boreratio' : predictions[11],
            'cylindernumber' : predictions[12],
            'fueleconomy' : predictions[13]
            }
            response = client.get('/api/predict', data=json.dumps(data), content_type='application/json')
            response_body = response.json

            # Check if the response is valid
            assert response.status_code == 200
            assert response_body['prediction']
            predictedOutput.append(response_body['prediction'])

            # Check if the prediction is consistent
            assert len(set(predictedOutput)) == 1

            # Make sure all the predictions are the same
            assert all(x == predictedOutput[0] for x in predictedOutput)

# Expected Failure Test
@pytest.mark.xfail(reason="arguments <= 0")
@pytest.mark.parametrize("entryList", [
    ['high', 'std', 0, -1, 0, -1, 'sedan', 'rwd', 'dohc', 0, -1, 0, 'four', -1, 0, -1],
    ['high', 'std', -1, 0, -1, 0, 'sedan', 'rwd', 'dohc', -1, 0, -1, 'four', 0, -1, 0],
    ['high', 'std', 0, 0, -1, 0, 'sedan', 'rwd', 'dohc', -1, 0, -1, 'four', 0, -1, 0]
])
def test_ExpectedFail(client,entryList, capsys):
    test_predict_GET_API(client, entryList, capsys)


# Validity Test + POST API Test for Predictions
@pytest.mark.parametrize("predValidityList",
    [
        ['Highend Price', 'std', 190, 3000, 250, 200, 'hardtop', '4wd', 'l', 70, 150, 2.5, 'two', 36.75, 22170.85],
        ['Medium Price', 'turbo', 174.04, 2555, 152, 102.4, 'sedan', 'fwd', 'ohc', 65.5, 120, 3.19, 'six', 26.7, 12648.39],
        ['Budget Price', 'std', 180, 3000, 120, 280, 'wagon', 'rwd', 'rotor', 65.5, 200, 3.8, 'five', 48, 26441.84]    
    ]
)
def test_predict_POST_API(client, predValidityList, capsys):
    with capsys.disabled():
        data = {
        'carsprice_range' : predValidityList[0],
        'aspiration' : predValidityList[1],
        'carlength' : predValidityList[2],
        'curbweight' : predValidityList[3],
        'horsepower' : predValidityList[4],
        'wheelbase' :predValidityList[5],
        'carbody' : predValidityList[6],
        'drivewheel' : predValidityList[7],
        'enginetype' : predValidityList[8],
        'carwidth' : predValidityList[9],
        'enginesize' : predValidityList[10],
        'boreratio' : predValidityList[11],
        'cylindernumber' : predValidityList[12],
        'fueleconomy' : predValidityList[13]
        }
        response = client.post('/api/predict', data=json.dumps(data), content_type='application/json')
        response_body = response.json

        # Check if the response is valid
        assert response.status_code == 200
        assert response_body['prediction'] == predValidityList[-1]

# Test Add Entry API
# Uses the email added by the registerAPI
@pytest.mark.parametrize("entryList",
    [
        ['Highend Price', 'std', 190, 3000, 250, 200, 'hardtop', '4wd', 'l', 70, 150, 2.5, 'two', 36.75, 22170.85, "testuser1@gmail.com"],
        ['Medium Price', 'turbo', 174.04, 2555, 152, 102.4, 'sedan', 'fwd', 'ohc', 65.5, 120, 3.19, 'six', 26.7, 12648.39, "testuser2@gmail.com"],
        ['Budget Price', 'std', 180, 3000, 120, 280, 'wagon', 'rwd', 'rotor', 65.5, 200, 3.8, 'five', 48, 26441.84, "testuser3@gmail.com"]    
    ]
)
def test_addEntry_API(client, entryList, capsys):
    with capsys.disabled():
        data1 = {
            'carsprice_range' : entryList[0],
            'aspiration' : entryList[1],
            'carlength' : entryList[2],
            'curbweight' : entryList[3],
            'horsepower' : entryList[4],
            'wheelbase' : entryList[5],
            'carbody' : entryList[6],
            'drivewheel' : entryList[7],
            'enginetype' : entryList[8],
            'carwidth' : entryList[9],
            'enginesize' : entryList[10],
            'boreratio' : entryList[11],
            'cylindernumber' : entryList[12],
            'fueleconomy' : entryList[13],
            'prediction' : entryList[14],
            'email': entryList[15]
        }
        response = client.post('/api/add_entry', data=json.dumps(data1), content_type='application/json')
        # Check if the response is valid
        assert response.status_code == 200
        assert response.headers["Content-Type"] == 'application/json'
        response_body = json.loads(response.get_data(as_text=True))

        # Check if the response added to the correct user
        assert response_body["email"] == entryList[15]

# Test Get Entries API
# based on specific emails tested previously
@pytest.mark.parametrize("getEntriesList",
    [
        [22170.85, "testuser1@gmail.com"],
        [12648.39, "testuser2@gmail.com"],
        [26441.84, "testuser3@gmail.com"]  
    ]
)
def test_getEntries_API(client, getEntriesList, capsys):
    with capsys.disabled():
        data1 = {
            'user_email': getEntriesList[1]
        }
        response = client.get('/api/get_entries', data=json.dumps(data1), content_type = 'application/json')
        # Check if the response is valid
        assert response.status_code == 200
        assert response.headers["Content-Type"] == 'application/json'
        response_body = json.loads(response.get_data(as_text=True))
        for entry in response_body["entries"]:
            # Check if the response retrieved from the correct user and correct entries are being obtained
            assert entry["prediction"] == getEntriesList[0]
            assert entry["user_email"] == getEntriesList[1]

# Test Delete Entry API
# based on specific entries keyed in previously and match the prediction values to find the correct entry id
@pytest.mark.parametrize('deleteEntryList',
    [
        [22170.85, "testuser1@gmail.com"],
        [12648.39, "testuser2@gmail.com"],
        [26441.84, "testuser3@gmail.com"]    
    ]             
)
def test_deleteEntry_API(client, deleteEntryList, capsys):
    with capsys.disabled():
        data1 = {
            'user_email': deleteEntryList[-1]
        }
        response = client.get('/api/get_entries', data=json.dumps(data1), content_type='application/json')
        # Check if the response is valid
        response_body = json.loads(response.get_data(as_text=True))

        # Checks for the entry id 
        for entry in response_body["entries"]:
            if entry["prediction"] == deleteEntryList[-2]:
                entry_id = entry["entry_id"]
                assert entry_id
                response2 = client.get(f'/api/remove_entry/{entry_id}')

                # Checks if the response are valid
                assert response2.status_code == 200
                assert response2.headers["Content-Type"] == "application/json"

                response2_body = json.loads(response2.get_data(as_text =True))
                assert response2_body["status"] == "success"
                assert int(response2_body["entry_id"]) == entry_id
                assert response2_body["message"] == "Entry is removed successfully."
