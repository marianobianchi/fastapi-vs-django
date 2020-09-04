import json
import time
import random
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task(2)
    def book_detail(self):
        book_id = random.randint(1, 11000)
        self.client.get(f'/books/{book_id}/', name='/books/detail')

    @task(3)
    def book_list(self):
        for _ in range(10):
            offset = random.randint(1, 11000)
            self.client.get(
                f'/books/?offset={offset}&limit={30}',
                name='/books',
            )
            time.sleep(1)

    @task
    def book_update(self):
        book_id = random.randint(1, 11000)
        response = self.client.get(f'/books/{book_id}/', name='/books/detail')
        time.sleep(1)
        data = json.loads(response.text)
        num_pages = data['num_pages']
        self.client.patch(
            f'/books/{book_id}/',
            json={'num_pages': num_pages + 1},
            headers={'authorization': 'Bearer admin'},
            name='/books/patch',
        )

        time.sleep(1)
        self.client.patch(
            f'/books/{book_id}/',
            json={'num_pages': num_pages},
            headers={'authorization': 'Bearer admin'},
            name='/books/patch',
        )
