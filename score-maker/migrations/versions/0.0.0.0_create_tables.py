"""Создание таблиц

Revision ID: 0.0.0.0
Revises: 
Create Date: 2024-11-19 17:50:38.634738

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0.0.0.0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS news")
    op.create_table(
        'news_score',
        sa.Column(
            'news_id',
            sa.Text(),
            nullable=False,
            comment='Идентификатор новости'
        ),
        sa.Column(
            'score',
            sa.Integer(),
            nullable=True,
            comment='Оценка новости'
        ),
        sa.Column(
            'editable',
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
            comment='Возможность редактирования оценки'
        ),
        sa.CheckConstraint(
            'score <= 5 AND score >= 1',
            name='score_value_limit'
        ),
        sa.PrimaryKeyConstraint('news_id'),
        schema='news',
        comment='Оценки новостей'
    )


def downgrade() -> None:
    op.drop_table('news_score', schema='news')
    op.execute("DROP SCHEMA IF EXISTS news CASCADE;")
    op.execute("DROP FUNCTION IF EXISTS public.uuid_generate_v4();")
