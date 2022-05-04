import io


def test_adding_recipe(client, auth):
    response1 = auth.register()
    response3 = auth.login()
    filename = "test.jpg"
    data = {'title': 'test title', 'description': 'test description', 'ingredients': 'test ingredients',
            'image': (io.BytesIO(b"random text"), filename)}
    response2 = client.post("/create", data=data)
    print(response2.data)
    assert response2.status_code == 302
    assert response2.headers["Location"] == "/recipes"