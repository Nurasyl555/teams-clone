"""
Management command to generate fake assignments and submissions.

Usage:
    python manage.py generate_assignments
    python manage.py generate_assignments --assignments 20 --submissions 10
    python manage.py generate_assignments --clear
"""

import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.team.models import Team
from apps.users.models import CustomUser
from apps.assigments.models import Assignments, Assignment_Submissions


ASSIGNMENT_TITLES = [
    "Introduction to Algorithms",
    "Data Structures Homework",
    "Database Design Project",
    "REST API Implementation",
    "Unit Testing Workshop",
    "UI/UX Prototype",
    "System Architecture Review",
    "Code Refactoring Task",
    "Security Audit Report",
    "Performance Optimization",
    "Docker & CI/CD Setup",
    "Machine Learning Model",
    "Frontend Dashboard",
    "Backend Microservice",
    "API Documentation",
    "Load Testing Analysis",
    "Mobile App Prototype",
    "GraphQL Integration",
    "Authentication Module",
    "Data Migration Script",
]

ASSIGNMENT_DESCRIPTIONS = [
    "Complete the implementation according to the provided specifications and submit a working solution.",
    "Research and document best practices, then apply them to the existing codebase.",
    "Design and build a fully functional module with tests covering at least 80% of the code.",
    "Analyze the current implementation, identify issues, and propose improvements with examples.",
    "Collaborate with your team to deliver a working prototype by the due date.",
    "Write a detailed report including diagrams, code snippets, and a summary of findings.",
    "Implement the feature end-to-end, from database schema to API endpoint to frontend component.",
    "Review the legacy code, refactor it following clean code principles, and document changes.",
]

STATUSES = ['upcoming', 'overdue', 'completed', 'completed_late']
STATUS_WEIGHTS = [0.3, 0.2, 0.35, 0.15]


class Command(BaseCommand):
    help = "Generate fake assignments and submissions for development/testing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--assignments",
            type=int,
            default=10,
            help="Number of assignments to create (default: 10)",
        )
        parser.add_argument(
            "--submissions",
            type=int,
            default=5,
            help="Max number of submissions per assignment (default: 5)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing assignments and submissions before generating",
        )

    def handle(self, *args, **options):
        num_assignments = options["assignments"]
        max_submissions = options["submissions"]
        clear = options["clear"]

        if clear:
            self._clear_data()

        teams = list(Team.objects.all())
        users = list(CustomUser.objects.all())

        if not teams:
            self.stderr.write(self.style.ERROR(
                "No teams found. Run `generate_teams` first."
            ))
            return

        if not users:
            self.stderr.write(self.style.ERROR(
                "No users found. Please create users first."
            ))
            return

        self.stdout.write(
            f"Found {len(teams)} team(s) and {len(users)} user(s). "
            f"Generating {num_assignments} assignment(s)..."
        )

        created_assignments = 0
        created_submissions = 0
        now = timezone.now()

        with transaction.atomic():
            for i in range(num_assignments):
                team = random.choice(teams)
                title = self._get_unique_title(i)
                description = random.choice(ASSIGNMENT_DESCRIPTIONS)
                max_points = random.choice([10, 20, 25, 50, 100])

                # due date: somewhere between -30 and +30 days from today
                due_offset = random.randint(-30, 30)
                due_date = (now + timedelta(days=due_offset)).date()

                assignment = Assignments.objects.create(
                    team=team,
                    title=title,
                    description=description,
                    due_data=due_date,
                    max_points=max_points,
                )
                created_assignments += 1

                # Generate random submissions
                num_submissions = min(random.randint(1, max_submissions), len(users))
                chosen_users = random.sample(users, num_submissions)

                for user in chosen_users:
                    status = random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
                    submitted = status in ('completed', 'completed_late')
                    submitted_at = None

                    if submitted:
                        if status == 'completed':
                            # submitted before due date
                            days_before = random.randint(0, max(1, due_offset))
                            submitted_at = now - timedelta(days=days_before)
                        else:
                            # submitted after due date
                            submitted_at = now - timedelta(days=random.randint(0, 5))

                    points = (
                        round(random.uniform(0, max_points), 1)
                        if submitted else 0.0
                    )

                    Assignment_Submissions.objects.create(
                        assignment=assignment,
                        student=user,
                        status=status,
                        points_awarded=points,
                        submitted=submitted,
                        submitted_at=submitted_at,
                    )
                    created_submissions += 1

                self.stdout.write(
                    f"  [{i + 1}/{num_assignments}] '{assignment.title}' "
                    f"| team: {team.name} "
                    f"| due: {due_date} "
                    f"| {num_submissions} submission(s)"
                )

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Created {created_assignments} assignment(s) "
            f"and {created_submissions} submission(s)."
        ))

    def _get_unique_title(self, index: int) -> str:
        if index < len(ASSIGNMENT_TITLES):
            base = ASSIGNMENT_TITLES[index]
        else:
            base = f"Assignment #{index + 1}"

        title = base
        counter = 1
        while Assignments.objects.filter(title=title).exists():
            title = f"{base} ({counter})"
            counter += 1
        return title

    def _clear_data(self):
        subs_deleted, _ = Assignment_Submissions.objects.all().delete()
        assignments_deleted, _ = Assignments.objects.all().delete()
        self.stdout.write(self.style.WARNING(
            f"Cleared {assignments_deleted} assignment(s) "
            f"and {subs_deleted} submission(s)."
        ))