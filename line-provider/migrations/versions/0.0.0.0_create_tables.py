"""Создание таблиц

Revision ID: 0.0.0.0
Revises: 
Create Date: 2024-11-12 19:32:00.788618

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = '0.0.0.0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION public.uuid_generate_v4()
        RETURNS uuid
        LANGUAGE 'c'
            COST 1
            VOLATILE STRICT PARALLEL SAFE 
            AS '$libdir/uuid-ossp', 'uuid_generate_v4'
        ;
        """
    )
    op.execute("CREATE SCHEMA IF NOT EXISTS news")
    op.create_table(
        'news',
        sa.Column('pk',
                  sa.Text(),
                  server_default=sa.text('public.uuid_generate_v4()'),
                  nullable=False),
        sa.Column('description',
                  sa.Text(),
                  nullable=False,
                  comment='Описание новости'),
        sa.Column('deadline',
                  sa.DateTime(timezone=True),
                  nullable=False,
                  comment='Дедлайн для оценки новости'),
        sa.Column('status',
                  sa.Enum('SCORED_GOOD', 'SCORED_BAD', 'NOT_SCORED', name='newsstatus'),
                  nullable=False,
                  comment='Статус новости'),
        sa.PrimaryKeyConstraint('pk'),
        schema='news',
        comment='Новости'
    )


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS news CASCADE;")
    op.execute("DROP TYPE IF EXISTS newsstatus;")
    op.execute("DROP FUNCTION IF EXISTS public.uuid_generate_v4();")
