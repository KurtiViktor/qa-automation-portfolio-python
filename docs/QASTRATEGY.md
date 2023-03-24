<!-- TOC -->
* [This is Testing Strategy](#this-is-testing-strategy)
  * [Requirements Testing](#requirements-testing)
  * [Functional Testing](#functional-testing)
    * [Smoke](#smoke)
    * [Regression](#regression)
      * [Component](#component)
  * [Defects](#defects)
<!-- TOC -->

# This is Testing Strategy

Hi,

A Test Strategy is a plan for defining an approach to the Software Testing Life Cycle (STLC).
It guides QA teams to define Test Coverage and testing scope.
It helps testers get a clear picture of the project at any instance.
The possibility of missing any test activity is very low when there is a proper test strategy in place.

## Requirements Testing
[5-key-attributes-requirements-testing-know-you-code](https://techbeacon.com/app-dev-testing/5-key-attributes-requirements-testing-know-you-code)

Requirements testing is done to clarify whether project requirements are feasible or not in terms of time,
resources and budget. Many bugs emerge in software because of incompleteness, inaccuracy and ambiguities
in functional requirements. That’s why it is highly important to test requirements and eliminate ambiguities
before you start to develop a project.

## Functional Testing

### Smoke

| testcase_id | name                          |
|-------------|-------------------------------|
| Smoke-1     | test_get_single_user_api_call |


### Regression

#### Component

| testcase_id  | name                                             |
|--------------|--------------------------------------------------|
| Component-1  | test_get_single_user_api_call_negative           |
| Component-2  | test_get_single_user_not_found_api_call          |
| Component-3  | test_get_single_user_not_found_api_call_negative |
| Component-4  | test_get_list_users_api_call                     |
| Component-5  | test_get_list_users_api_call_negative            |
| Component-6  | test_post_create_api_call                        |
| Component-7  | test_post_create_api_call_negative               |
| Component-8  | test_call_wrong_api_call                         |
| Component-9  | test_standard_user                               |
| Component-10 | test_locked_out_user                             |

## Defects

| Bug ID | Bug Description                                | Testcase ID |
|--------|------------------------------------------------|-------------|
| bug_1  | locked_out_user has no access to saucedemo.com | case_1      |
