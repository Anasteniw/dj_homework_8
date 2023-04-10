
import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from django.urls import reverse


from students.models import Course
from students.models import Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


# 1.
@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    course = course_factory(_quantity=1)
    course_id = course[0].id
    url = reverse('courses-detail', args=(course_id,))
    response = client.get(url)
    data = response.json()
    assert data['name'] == course[0].name

# 2
@pytest.mark.django_db
def test_create_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url)
    data = response.json()
    assert len(data) == len(courses)

# 3
@pytest.mark.django_db
def test_filter_id_courses(client, course_factory):
    courses = course_factory(_quantity=5)
    course_id = courses[2].id
    url = reverse('courses-detail', args=(course_id,))
    response = client.get(url)
    data = response.json()
    assert data['name'] == courses[2].name

# 4
@pytest.mark.django_db
def test_filter_name_courses(client, course_factory):
    courses = course_factory(_quantity=5)
    url = reverse('courses-list')
    response = client.get(url, {'name': courses[3].name})
    data = response.json()
    assert data[0]['name'] == courses[3].name

# 5
@pytest.mark.django_db
def test_create_course_succses(client):
    count = Course.objects.count()
    url = reverse('courses-list')
    response = client.post(url, data={'name': 'Python'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

#6
@pytest.mark.django_db
def test_patch_course(client, course_factory):
    courses = course_factory(_quantity=5)
    course_id = courses[3].id
    url = reverse('courses-detail', args=(course_id,))
    response = client.patch(url, data={'name': 'Java'})
    data = response.json()
    assert data['name'] == 'Java'

#7
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=20)
    course_id = courses[7].id
    count = Course.objects.count()
    url = reverse('courses-detail', args=(course_id,))
    response = client.delete(url)
    assert response.status_code == 204
    assert Course.objects.count() == count - 1



    
   
