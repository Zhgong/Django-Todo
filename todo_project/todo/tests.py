from django.test import TestCase

# Create your tests here.
# todo/tests.py

from .models import ToDo
from .serializers import ToDoSerializer
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class ToDoModelTest(TestCase):
    def setUp(self):
        self.todo = ToDo.objects.create(
            title="测试待办事项",
            description="这是一个测试的待办事项",
            completed=False
        )

    def test_todo_creation(self):
        self.assertEqual(self.todo.title, "测试待办事项")
        self.assertEqual(self.todo.description, "这是一个测试的待办事项")
        self.assertFalse(self.todo.completed)
        self.assertIsNotNone(self.todo.created_at)

    def test_todo_str(self):
        self.assertEqual(str(self.todo), "测试待办事项")


class ToDoSerializerTest(TestCase):
    def setUp(self):
        self.todo_data = {
            'title': '序列化测试',
            'description': '测试序列化器',
            'completed': False
        }
        self.serializer = ToDoSerializer(data=self.todo_data)

    def test_serializer_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serializer_save(self):
        # 首先验证数据
        self.assertTrue(self.serializer.is_valid(), self.serializer.errors)

        # 然后保存
        todo = self.serializer.save()
        self.assertEqual(todo.title, self.todo_data['title'])
        self.assertEqual(todo.description, self.todo_data['description'])
        self.assertEqual(todo.completed, self.todo_data['completed'])


class ToDoAPITest(APITestCase):
    def setUp(self):
        self.todo_url = reverse('todo-list')
        self.todo_data = {
            'title': 'API测试待办事项',
            'description': '通过API创建的待办事项',
            'completed': False
        }
        self.todo = ToDo.objects.create(**self.todo_data)

    def test_get_todo_list(self):
        response = self.client.get(self.todo_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.todo_data['title'])

    def test_create_todo(self):
        data = {
            'title': '新创建的待办事项',
            'description': '这是通过API创建的',
            'completed': False
        }
        response = self.client.post(self.todo_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ToDo.objects.count(), 2)
        self.assertEqual(ToDo.objects.get(id=response.data['id']).title, data['title'])

    def test_update_todo(self):
        update_url = reverse('todo-detail', args=[self.todo.id])
        data = {
            'title': '更新后的待办事项',
            'description': '已更新',
            'completed': True
        }
        response = self.client.put(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, data['title'])
        self.assertTrue(self.todo.completed)

    def test_delete_todo(self):
        delete_url = reverse('todo-detail', args=[self.todo.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ToDo.objects.count(), 0)
