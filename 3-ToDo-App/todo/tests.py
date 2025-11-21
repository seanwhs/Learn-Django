# todo/tests.py
from django.test import TestCase
from django.urls import reverse
from datetime import date, timedelta
from category.models import Category
from .models import Task
from .forms import TaskForm
from django.core.exceptions import ValidationError


# -------------------------
# Model Tests
# -------------------------
class TaskModelTests(TestCase):

    def setUp(self):
        # Create a category to assign to tasks
        self.category = Category.objects.create(title="Work")

    def test_create_valid_task(self):
        # Task with today or future due_date should be valid
        task = Task(category=self.category, title="Valid Task", due_date=date.today())
        task.full_clean()  # Should not raise ValidationError
        task.save()
        self.assertEqual(Task.objects.count(), 1)

    def test_due_date_in_past_raises_error(self):
        # Task with past due_date should fail validation
        task = Task(category=self.category, title="Invalid Task", due_date=date.today() - timedelta(days=1))
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_due_date_today_is_valid(self):
        # Task due today is valid
        task = Task(category=self.category, title="Today Task", due_date=date.today())
        task.full_clean()  # No error

    def test_string_representation(self):
        # str(task) returns title
        task = Task.objects.create(category=self.category, title="Test Title", due_date=date.today())
        self.assertEqual(str(task), "Test Title")


# -------------------------
# Form Tests
# -------------------------
class TaskFormTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title="Personal")

    def test_valid_form(self):
        # Valid form data passes validation
        form = TaskForm(data={
            "category": self.category.id,
            "title": "Test Task",
            "due_date": date.today(),
            "priority": "M",
            "is_done": False,
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_due_date(self):
        """
        Form is invalid if due_date is in the past because model.clean() enforces it.
        Non-field error (__all__) will contain the message.
        """
        form = TaskForm(data={
            "category": self.category.id,
            "title": "Task Title",
            "due_date": date.today() - timedelta(days=1),
            "priority": "M",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("Due date cannot be in the past.", form.non_field_errors())


# -------------------------
# View Tests
# -------------------------
class TaskViewTests(TestCase):

    def setUp(self):
        # Create category and a task for view tests
        self.category = Category.objects.create(title="Errands")
        self.task = Task.objects.create(
            category=self.category,
            title="Existing Task",
            due_date=date.today(),
        )

    def test_list_tasks_view(self):
        # List view renders and contains task
        url = reverse('list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Existing Task")

    def test_create_task_valid(self):
        # Creating a valid task redirects and increases count
        url = reverse('create')
        response = self.client.post(url, {
            "category": self.category.id,
            "title": "Created Task",
            "due_date": date.today(),
            "priority": "M",
            "is_done": False,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 2)

    def test_create_task_invalid_due_date(self):
        # Creating task with past due_date should re-render form with error
        url = reverse('create')
        response = self.client.post(url, {
            "category": self.category.id,
            "title": "Bad Task",
            "due_date": "1990-01-01",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cannot be in the past")

    def test_update_task(self):
        # Updating a task changes its attributes
        url = reverse('update', args=[self.task.id])
        response = self.client.post(url, {
            "category": self.category.id,
            "title": "Updated Task",
            "due_date": date.today(),
            "priority": "H",
            "is_done": True,
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")
        self.assertTrue(self.task.is_done)

    def test_delete_task(self):
        # Deleting a task removes it from the database
        url = reverse('delete', args=[self.task.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)
