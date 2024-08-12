from django.test import TestCase, Client
from django.urls import reverse
from .models import Todo
from django.contrib.messages import get_messages

class TodoViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title="Test Todo", complete=False)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')        

    def test_add_todo_valid(self):
        response = self.client.post(reverse('add'), {'task_id': 'New Todo'})
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(Todo.objects.filter(title='New Todo').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Todo item added successfully!')

    def test_add_todo_invalid(self):
        response = self.client.post(reverse('add'), {'task_id': ''})
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(Todo.objects.filter(title='').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Value is required.')

    def test_update_todo(self):
        self.assertFalse(self.todo.complete)
        response = self.client.get(reverse('update', args=[self.todo.id]))
        self.assertRedirects(response, reverse('index'))
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.complete)

    def test_delete_todo_valid(self):
        response = self.client.get(reverse('delete', args=[self.todo.id]))
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(Todo.objects.filter(id=self.todo.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Task deleted!')

    def test_delete_todo_invalid(self):
        invalid_id = 9999
        response = self.client.get(reverse('delete', args=[invalid_id]))
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Task does not exist.')