from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from schoolapp.models import UserProfile, Course, Lesson, Order
# Тестовый класс для проверки модели UserProfile
class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone='1234567890',
            gender='M',
            birth_date='1990-01-01',
            profile_picture='profile_picture.jpg'
        )
# Тест на создание профиля пользователя
    def test_user_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.phone, '1234567890')
        self.assertEqual(self.profile.gender, 'M')
        self.assertEqual(str(self.profile.birth_date), '1990-01-01')
        self.assertEqual(self.profile.profile_picture, 'profile_picture.jpg')
        self.assertEqual(str(self.profile), f'Profile for {self.user.username}')
# Тестовый класс для проверки модели Course
class CourseTestCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            description='This is a test course.',
            price=Decimal('99.99'),
            is_online=True
        )
# Тест на создание курса
    def test_course_creation(self):
        self.assertEqual(self.course.name, 'Test Course')
        self.assertEqual(self.course.description, 'This is a test course.')
        self.assertEqual(self.course.price, Decimal('99.99'))
        self.assertTrue(self.course.is_online)
# Тестовый класс для проверки модели Lesson
class LessonTestCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            description='This is a test course.',
            price=Decimal('99.99'),
            is_online=True
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            name='Test Lesson',
            description='This is a test lesson.',
            video_url='https://example.com/test-video.mp4',
            order=1
        )
# Тест на создание урока
    def test_lesson_creation(self):
        self.assertEqual(self.lesson.course, self.course)
        self.assertEqual(self.lesson.name, 'Test Lesson')
        self.assertEqual(self.lesson.description, 'This is a test lesson.')
        self.assertEqual(self.lesson.video_url, 'https://example.com/test-video.mp4')
        self.assertEqual(self.lesson.order, 1)
# Тестовый класс для проверки модели Order
class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.course1 = Course.objects.create(
            name='Test Course 1',
            description='This is test course 1.',
            price=Decimal('49.99'),
            is_online=True
        )
        self.course2 = Course.objects.create(
            name='Test Course 2',
            description='This is test course 2.',
            price=Decimal('59.99'),
            is_online=True
        )
        self.order = Order.objects.create(
            user=self.user,
            status='pending'
        )
        self.order.courses.add(self.course1, self.course2)
# Тест на создание заказа
    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.status, 'pending')
        self.assertIn(self.course1, self.order.courses.all())
        self.assertIn(self.course2, self.order.courses.all())
# Тест на расчет общей стоимости заказа
    def test_get_total_cost(self):
        total_cost = self.order.get_total_cost()
        self.assertEqual(total_cost, Decimal('49.99') + Decimal('59.99'))
