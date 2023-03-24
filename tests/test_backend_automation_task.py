"""
2. Backend  automation task:

Using the following URL, https://reqres.in/ create some automated API tests
for the following endpoints(positive and negative scenarios):
GET (Single and List of users)
POST (Create user)
"""
import allure
import cattrs
import jsonschema
import pytest
import requests
from assertpy import assert_that
from attr import define, field
from jsonschema import validate

from config import settings


@define
class BaseAttrs:

    def to_str(self):
        return str(cattrs.unstructure(self))


@define
class UserData(BaseAttrs):
    id: int = field(init=False)
    email: str = field(init=False)
    first_name: str = field(init=False)
    last_name: str = field(init=False)
    avatar: str = field(init=False)

    @classmethod
    def default(cls):
        default = cls()
        default.id = 2
        default.email = 'janet.weaver@reqres.in'
        default.first_name = 'Janet'
        default.last_name = 'Weaver'
        default.avatar = "https://reqres.in/img/faces/2-image.jpg"
        return default

    @classmethod
    def byron(cls):
        byron = cls()
        byron.id = 10
        byron.email = 'byron.fields@reqres.in'
        byron.first_name = 'Byron'
        byron.last_name = 'Fields'
        byron.avatar = "https://reqres.in/img/faces/10-image.jpg"
        return byron

    @classmethod
    def blabla(cls):
        blabla = cls()
        blabla.id = -1
        blabla.email = 'blabla.blabla@reqres.in'
        blabla.first_name = 'blabla'
        blabla.last_name = 'blabla'
        blabla.avatar = "https://reqres.in/img/faces/10-image.jpg"
        return blabla


@define
class SupportData(BaseAttrs):
    url: str = field(init=False)
    text: str = field(init=False)

    @classmethod
    def default(cls):
        default = cls()
        default.url = 'https://reqres.in/#support-heading'
        default.text = 'To keep ReqRes free, contributions towards server costs are appreciated!'
        return default


@define
class SingleUserResponse(BaseAttrs):
    data: UserData = field(init=False)
    support: SupportData = field(init=False)

    @classmethod
    def default(cls):
        default = cls()
        default.data = UserData.default()
        default.support = SupportData.default()
        return default


@define
class MultipleUserResponse(BaseAttrs):
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
class CreateUserRequest(BaseAttrs):
    name: str = field(init=False)
    job: str = field(init=False)

    @classmethod
    def default(cls):
        default = cls()
        default.name = 'vkurti'
        default.job = 'qa'
        return default


@define
class CreateUserResponse(BaseAttrs):
    name: str = field(init=False)
    job: str = field(init=False)
    id: str = field(init=False)
    createdAt: str = field(init=False)

    @classmethod
    def default(cls):
        default = cls()
        default.name = 'vkurti'
        default.job = 'qa'
        default.id = '777'
        default.createdAt = '2023-01-12T09:52:35.026Z'
        return default


@pytest.mark.api
@pytest.mark.component
class TestReqresinApi:

    @allure.step
    def get_api_call(self, url, status_code=200):
        response = requests.get(url, timeout=settings.DELAY)
        assert_that(response.status_code).is_equal_to(status_code)
        return response

    @allure.step
    def get_api_call_json_response(self, url, status_code=200):
        response = self.get_api_call(url=url, status_code=status_code)
        return response.json()

    @allure.step
    def validate_json(self, json_data, json_schema):
        try:
            validate(instance=json_data, schema=json_schema)
        except jsonschema.exceptions.ValidationError:
            return False
        return True

    @allure.step
    def post_api_call(self, url, status_code=200, data=None):
        dataset = str(cattrs.unstructure(data))
        response = requests.post(url, data=dataset, timeout=settings.DELAY)
        assert_that(response.status_code).is_equal_to(status_code)
        return response

    @allure.step
    def post_api_call_json_response(self, url, status_code=200, data=None):
        response = self.post_api_call(url=url, status_code=status_code, data=data)
        return response.json()

    @pytest.mark.smoke
    @pytest.mark.test_id("Smoke-1")
    def test_get_single_user_api_call(self):
        real_response = self.get_api_call_json_response(url=settings.GET_SINGLE_USER_API_CALL)
        expected_response = SingleUserResponse.default().to_str()
        assert_that(str(real_response)).is_equal_to(expected_response)

    @pytest.mark.negative
    @pytest.mark.test_id("Component-1")
    def test_get_single_user_api_call_negative(self):
        real_response = self.get_api_call_json_response(url=settings.GET_SINGLE_USER_API_CALL)
        assert_that(real_response['data']).contains('email')
        assert_that(real_response['data']).does_not_contain('bla')
        assert_that(real_response).does_not_contain_duplicates()

    @pytest.mark.test_id("Component-2")
    def test_get_single_user_not_found_api_call(self):
        real_response = self.get_api_call(
            url=settings.GET_SINGLE_USER_NOT_FOUND_API_CALL,
            status_code=404
        )
        assert_that(str(real_response.json())).is_equal_to('{}')

    @pytest.mark.negative
    @pytest.mark.test_id("Component-3")
    def test_get_single_user_not_found_api_call_negative(self):
        headers = {'Content-type': 'application/json'}
        response = requests.get(
            settings.GET_SINGLE_USER_NOT_FOUND_API_CALL,
            headers=headers,
            timeout=settings.DELAY
        )
        assert_that(response.status_code).is_not_equal_to(200)

    @pytest.mark.test_id("Component-4")
    def test_get_list_users_api_call(self):
        real_response = self.get_api_call_json_response(url=settings.GET_LIST_USERS_API_CALL)
        expected_response = MultipleUserResponse.default()
        assert_that(real_response['page']).is_equal_to(expected_response.page)
        assert_that(real_response['per_page']).is_equal_to(expected_response.per_page)
        assert_that(real_response['total']).is_equal_to(expected_response.total)
        assert_that(real_response['total_pages']).is_equal_to(expected_response.total_pages)
        assert_that(str(real_response['data'])).contains(UserData.byron().to_str())
        assert_that(str(real_response['support'])).is_equal_to(SupportData.default().to_str())

    @pytest.mark.negative
    @pytest.mark.test_id("Component-5")
    def test_get_list_users_api_call_negative(self):
        real_response = self.get_api_call_json_response(url=settings.GET_LIST_USERS_API_CALL)
        assert_that(real_response['data']).does_not_contain(UserData.blabla().to_str())
        assert_that(real_response).does_not_contain_duplicates()

    @pytest.mark.test_id("Component-6")
    def test_post_create_api_call(self):
        real_response = self.post_api_call_json_response(
            status_code=201,
            url=settings.POST_CREATE_API_CALL,
            data=CreateUserRequest.default().to_str()
        )
        # Describe what kind of json you expect.
        post_schema = {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "createdAt": {"type": "string"},
            },
        }
        assert_that(self.validate_json(json_data=real_response, json_schema=post_schema)).is_true()

    @pytest.mark.negative
    @pytest.mark.test_id("Component-7")
    def test_post_create_api_call_negative(self):
        real_response = self.post_api_call(
            status_code=201,
            url=settings.POST_CREATE_API_CALL
        )
        assert_that(str(real_response.json())).does_not_contain('fhfhfhfhfkh')

    @pytest.mark.negative
    @pytest.mark.test_id("Component-8")
    def test_call_wrong_api_call(self):
        self.get_api_call(url=settings.WRONG_API_CALL, status_code=404)
