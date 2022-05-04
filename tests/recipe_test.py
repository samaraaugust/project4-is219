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

def test_viewing_recipe(client, auth):
    response1 = auth.register()
    response3 = auth.login()
    filename = "test.jpg"
    data = {'title': 'test title', 'description': 'test description', 'ingredients': 'test ingredients',
            'image': (io.BytesIO(b"random text"), filename)}
    response2 = client.post("/create", data=data)
    response4 = client.get("/recipes/1")
    print(response4.data)
    assert response4.status_code == 200
    assert b"test title" in response4.data

