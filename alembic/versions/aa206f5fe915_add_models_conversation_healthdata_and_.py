"""Add models Conversation, HealthData and User

Revision ID: aa206f5fe915
Revises:
Create Date: 2020-11-27 18:08:36.064456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa206f5fe915'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('hashed_password', sa.String(length=200), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('conversations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_msg', sa.String(length=200), nullable=False),
    sa.Column('bot_msg', sa.String(length=200), nullable=False),
    sa.Column('intent', sa.String(length=50), nullable=True),
    sa.Column('display_type', sa.Enum('default', 'five_stars', name='displaytype'), nullable=True),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversations_bot_msg'), 'conversations', ['bot_msg'], unique=False)
    op.create_index(op.f('ix_conversations_id'), 'conversations', ['id'], unique=False)
    op.create_index(op.f('ix_conversations_intent'), 'conversations', ['intent'], unique=False)
    op.create_index(op.f('ix_conversations_user_msg'), 'conversations', ['user_msg'], unique=False)
    op.create_table('health-data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('energy', sa.Integer(), nullable=True),
    sa.Column('restful_sleep', sa.Integer(), nullable=True),
    sa.Column('fall_asleep_easily', sa.Integer(), nullable=True),
    sa.Column('deep_sleep', sa.Integer(), nullable=True),
    sa.Column('enough_sleep', sa.Integer(), nullable=True),
    sa.Column('energy_morning', sa.Integer(), nullable=True),
    sa.Column('uniform_mood', sa.Integer(), nullable=True),
    sa.Column('memory', sa.Integer(), nullable=True),
    sa.Column('concentration', sa.Integer(), nullable=True),
    sa.Column('creativity', sa.Integer(), nullable=True),
    sa.Column('stress', sa.Integer(), nullable=True),
    sa.Column('cramps', sa.Integer(), nullable=True),
    sa.Column('dagger', sa.Integer(), nullable=True),
    sa.Column('pump_strokes', sa.Integer(), nullable=True),
    sa.Column('uplifts', sa.Integer(), nullable=True),
    sa.Column('swollen_belly', sa.Integer(), nullable=True),
    sa.Column('gases', sa.Integer(), nullable=True),
    sa.Column('bowel_movement', sa.Integer(), nullable=True),
    sa.Column('sheet_wipe', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('valid', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_health-data_id'), 'health-data', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_health-data_id'), table_name='health-data')
    op.drop_table('health-data')
    op.drop_index(op.f('ix_conversations_user_msg'), table_name='conversations')
    op.drop_index(op.f('ix_conversations_intent'), table_name='conversations')
    op.drop_index(op.f('ix_conversations_id'), table_name='conversations')
    op.drop_index(op.f('ix_conversations_bot_msg'), table_name='conversations')
    op.drop_table('conversations')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
