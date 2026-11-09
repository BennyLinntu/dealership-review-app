from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from djangoapp.models import Dealer, Review
from vehicles.models import CarMake, CarModel


class DealershipTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="reviewer",
            email="reviewer@example.com",
            password="StrongPass123!",
            first_name="Riley",
            last_name="Chen",
        )
        cls.token = Token.objects.create(user=cls.user)

        cls.dealer = Dealer.objects.create(
            business_name="Downtown Toyota",
            full_name="John Thompson",
            email="john@example.com",
            phone="555-123-4567",
            address="123 Main Street",
            city="New York",
            state="NY",
            zip_code="10001",
            latitude=40.7128,
            longitude=-74.0060,
        )
        cls.other_dealer = Dealer.objects.create(
            business_name="Sunshine Ford",
            full_name="Michael Johnson",
            email="michael@example.com",
            phone="555-987-6543",
            address="789 Beach Road",
            city="Miami",
            state="FL",
            zip_code="33101",
        )
        cls.review = Review.objects.create(
            dealer=cls.dealer,
            user=cls.user,
            rating=5,
            review_text="Fantastic service and a very friendly team.",
            sentiment="positive",
            sentiment_score=0.8,
            car_make="Toyota",
            car_model="Camry",
            car_year=2022,
        )
        cls.make = CarMake.objects.create(name="Toyota")
        cls.model = CarModel.objects.create(
            make=cls.make, name="Camry", year=2022)

    def setUp(self):
        self.client = APIClient()

    def test_dealer_list_includes_rating_summary(self):
        response = self.client.get("/api/dealers/")
        self.assertEqual(response.status_code, 200)
        results = response.json()["results"]
        dealer = next(item for item in results if item["id"] == self.dealer.id)
        self.assertEqual(dealer["review_count"], 1)
        self.assertEqual(dealer["average_rating"], 5.0)
        self.assertEqual(dealer["state_name"], "New York")

    def test_dealer_detail_includes_reviews(self):
        response = self.client.get(f"/api/dealers/{self.dealer.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["reviews"]), 1)

    def test_review_api_computes_sentiment_and_saves_car(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        payload = {
            "dealer": self.dealer.id,
            "rating": 4,
            "review_text": "I love this place, the staff were amazing!",
            "car_make": "Toyota",
            "car_model": "RAV4",
            "car_year": 2023,
            "purchase": True,
        }
        response = self.client.post("/api/reviews/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["sentiment"], "positive")
        self.assertEqual(body["user"]["username"], "reviewer")
        self.assertEqual(body["car_model"], "RAV4")

    def test_review_api_rejects_short_text(self):
        payload = {
            "dealer": self.dealer.id,
            "rating": 4,
            "review_text": "Too short",
        }
        response = self.client.post("/api/reviews/", payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("review_text", response.json())

    def test_sentiment_api(self):
        response = self.client.post(
            "/api/sentiment/",
            {"text": "This was a terrible and disappointing experience."},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["sentiment"], "negative")

    def test_token_login(self):
        response = self.client.post(
            "/api/login/",
            {"username": "reviewer", "password": "StrongPass123!"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "reviewer")
        self.assertEqual(response.json()["token"], self.token.key)

    def test_search_and_state_filter(self):
        response = self.client.get("/", {"q": "Toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["dealers"]), [self.dealer])

        response = self.client.get("/", {"state": "Florida"})
        self.assertEqual(list(response.context["dealers"]), [self.other_dealer])

    def test_dealer_detail_page_shows_review(self):
        response = self.client.get(f"/dealer/{self.dealer.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fantastic service")
        self.assertContains(response, "Downtown Toyota")

    def test_html_review_requires_login(self):
        response = self.client.get(f"/dealer/{self.dealer.id}/add_review/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_html_review_post_creates_review(self):
        self.client.force_login(self.user)
        response = self.client.post(
            f"/dealer/{self.dealer.id}/add_review/",
            {
                "review": "Great people and a smooth buying experience.",
                "rating": "5",
                "car_make": "Toyota",
                "car_model": "Camry",
                "car_year": "2024",
                "purchase": "1",
            },
        )
        self.assertEqual(response.status_code, 302)
        review = Review.objects.filter(user=self.user).latest("created_at")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.car_year, 2024)
        self.assertEqual(review.sentiment, "positive")

    def test_html_review_rejects_invalid_rating(self):
        self.client.force_login(self.user)
        response = self.client.post(
            f"/dealer/{self.dealer.id}/add_review/",
            {"review": "A valid length review text.", "rating": "9"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Choose a rating", status_code=400)

    def test_registration_page_creates_account(self):
        response = self.client.post(
            "/register/",
            {
                "username": "newuser",
                "first_name": "New",
                "last_name": "User",
                "email": "new@example.com",
                "password1": "AnotherStrongPass123!",
                "password2": "AnotherStrongPass123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_fetch_reviews_uses_saved_car_fields(self):
        response = self.client.get(f"/fetchReviews/dealer/{self.dealer.id}")
        self.assertEqual(response.status_code, 200)
        review = response.json()["reviews"][0]
        self.assertEqual(review["car_make"], "Toyota")
        self.assertEqual(review["car_year"], 2022)
        self.assertTrue(review["purchase"])

    def test_cars_endpoint(self):
        response = self.client.get("/djangoapp/get_cars")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["CarModels"][0],
            {"CarMake": "Toyota", "CarModel": "Camry"},
        )
