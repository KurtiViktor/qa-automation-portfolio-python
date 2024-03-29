"""
2. Backend  automation task:

Using the following URL, https://reqres.in/ create some automated API tests
for the following endpoints(positive and negative scenarios):
GET (Single and List of users)
POST (Create user)
"""

import allure
import pytest
import requests
from assertpy import assert_that
from attrs import asdict, define, field
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from config import settings


@define
class UserData:
    id: int = field(init=False)
    email: str = field(init=False)
    first_name: str = field(init=False)
    last_name: str = field(init=False)
    avatar: str = field(init=False)

    @classmethod
    def default(cls):
        default = cls()
        default.id = 2
        default.email = "janet.weaver@reqres.in"
        default.first_name = "Janet"
        default.last_name = "Weaver"
        default.avatar = "https://reqres.in/img/faces/2-image.jpg"
        return default

    @classmethod
    def byron(cls):
        byron = cls()
        byron.id = 10
        byron.email = "byron.fields@reqres.in"
        byron.first_name = "Byron"
        byron.last_name = "Fields"
        byron.avatar = "https://reqres.in/img/faces/10-image.jpg"
        return byron

    @classmethod
    def blabla(cls):
        blabla = cls()
        blabla.id = -1
        blabla.email = "blabla.blabla@reqres.in"
        blabla.first_name = "blabla"
        blabla.last_name = "blabla"
        blabla.avatar = "https://reqres.in/img/faces/10-image.jpg"
        return blabla


@define
class SupportData:
    url: str = field(init=False)
    text: str = field(init=False)

    @classmethod
    def default(cls):
        default = cls()
        default.url = "https://reqres.in/#support-heading"
        default.text = (
            "To keep ReqRes free, contributions towards server costs are appreciated!"
        )
        return default


@define
class SingleUserResponse:
    data: UserData = field(init=False)
    support: SupportData = field(init=False)

    @classmethod
    def default(cls):
        default = cls()
        default.data = UserData.default()
        default.support = SupportData.default()
        return default


@define
class MultipleUserResponse:
    page: int = field(init=False)
    per_page: int = field(init=False)
    total: int = field(init=False)
    total_pages: int = field(init=False)
    data: list = field(factory=list)
    support: SupportData = field(init=False)

    @classmethod
    def default(cls):
        default = cls()
        default.page = 2
        default.per_page = 6
        default.total = 12
        default.total_pages = 2
        default.data = []
        default.support = SupportData.default()
        return default


@define
class CreateUserRequest:
    name: str = field(init=False)
    job: str = field(init=False)

    @classmethod
    def default(cls):
        default = cls()
        default.name = "vkurti"
        default.job = "qa"
        return default


@define
class CreateUserResponse:
    name: str = field(init=False)
    job: str = field(init=False)
    id: str = field(init=False)
    createdAt: str = field(init=False)

    @classmethod
    def default(cls):
        default = cls()
        default.name = "vkurti"
        default.job = "qa"
        default.id = "777"
        default.createdAt = "2023-01-12T09:52:35.026Z"
        return default


@pytest.mark.api
@pytest.mark.component
class TestBackend:
    @allure.step
    def get(self, url, code=200):
        response = requests.get(url, timeout=settings.DELAY)
        assert_that(response.status_code).is_equal_to(code)
        return response

    @allure.step
    def validate(self, json, schema):
        try:
            validate(instance=json, schema=schema)
        except ValidationError:
            return False
        return True

    @allure.step
    def post(self, url, code=200, data=None):
        response = requests.post(url, data=data, timeout=settings.DELAY)
        assert_that(response.status_code).is_equal_to(code)
        return response

    @pytest.mark.smoke
    @pytest.mark.testid("Smoke-1")
    def test_get_single_user(self):
        real = self.get(url=settings.GET_SINGLE_USER)
        expected = SingleUserResponse.default()
        assert_that(real.json()).is_equal_to(asdict(expected))

    @pytest.mark.negative
    @pytest.mark.testid("Component-1")
    def test_get_single_user_negative(self):
        real = self.get(url=settings.GET_SINGLE_USER).json()
        assert_that(real["data"]).contains("email")
        assert_that(real["data"]).does_not_contain("bla")
        assert_that(real).does_not_contain_duplicates()

    @pytest.mark.testid("Component-2")
    def test_get_single_user_not_found(self):
        real = self.get(url=settings.GET_SINGLE_USER_NOT_FOUND, code=404)
        assert_that(str(real.json())).is_equal_to("{}")

    @pytest.mark.negative
    @pytest.mark.testid("Component-3")
    def test_get_single_user_not_found_negative(self):
        headers = {"Content-type": "application/json"}
        real = requests.get(
            url=settings.GET_SINGLE_USER_NOT_FOUND,
            headers=headers,
            timeout=settings.DELAY,
        )
        assert_that(real.status_code).is_not_equal_to(200)

    @pytest.mark.testid("Component-4")
    def test_get_list_users(self):
        real = self.get(url=settings.GET_LIST_USERS).json()
        expected = MultipleUserResponse.default()
        assert_that(real["page"]).is_equal_to(expected.page)
        assert_that(real["per_page"]).is_equal_to(expected.per_page)
        assert_that(real["total"]).is_equal_to(expected.total)
        assert_that(real["total_pages"]).is_equal_to(expected.total_pages)
        assert_that(real["data"]).contains(asdict(UserData.byron()))
        assert_that(real["support"]).is_equal_to(asdict(SupportData.default()))

    @pytest.mark.negative
    @pytest.mark.testid("Component-5")
    def test_get_list_users_negative(self):
        real = self.get(url=settings.GET_LIST_USERS).json()
        assert_that(real["data"]).does_not_contain(asdict(UserData.blabla()))
        assert_that(real).does_not_contain_duplicates()

    @pytest.mark.testid("Component-6")
    def test_post_create(self):
        real = self.post(
            code=201, url=settings.POST_CREATE, data=asdict(CreateUserRequest.default())
        )
        # Describe what kind of json you expect.
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "createdAt": {"type": "string"},
            },
        }
        assert_that(self.validate(real.json(), schema)).is_true()

    @pytest.mark.negative
    @pytest.mark.testid("Component-7")
    def test_post_create_negative(self):
        real = self.post(code=201, url=settings.POST_CREATE)
        assert_that(real.json()).does_not_contain("fhfhfhfhfkh")

    @pytest.mark.negative
    @pytest.mark.testid("Component-8")
    def test_wrong(self):
        self.get(url=settings.WRONG, code=404)
