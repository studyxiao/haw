"""empty message

Revision ID: 439b6160a2a1
Revises: 
Create Date: 2020-06-04 09:45:32.405813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '439b6160a2a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth',
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.Column('delete_time', sa.DateTime(), nullable=True, comment='删除时间，软删除时赋值，表示删除'),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False, comment='所属权限组id'),
    sa.Column('auth', sa.String(length=60), nullable=True, comment='权限字段'),
    sa.Column('module', sa.String(length=50), nullable=True, comment='权限所属模块'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('file',
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.Column('delete_time', sa.DateTime(), nullable=True, comment='删除时间，软删除时赋值，表示删除'),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=500), nullable=False, comment='路径'),
    sa.Column('type', sa.SmallInteger(), nullable=True, comment='1 local，其他表示其他地方'),
    sa.Column('name', sa.String(length=100), nullable=False, comment='名称'),
    sa.Column('extension', sa.String(length=50), nullable=False, comment='后缀'),
    sa.Column('size', sa.Integer(), nullable=True, comment='大小'),
    sa.Column('md5', sa.String(length=40), nullable=True, comment='md5值，防止上传重复图片'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('md5')
    )
    op.create_table('group',
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.Column('delete_time', sa.DateTime(), nullable=True, comment='删除时间，软删除时赋值，表示删除'),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True, comment='权限组名称'),
    sa.Column('info', sa.String(length=255), nullable=True, comment='权限组描述'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.Column('delete_time', sa.DateTime(), nullable=True, comment='删除时间，软删除时赋值，表示删除'),
    sa.Column('email', sa.String(length=100), nullable=False, comment='邮箱'),
    sa.Column('mobile', sa.String(length=20), nullable=True, comment='手机号'),
    sa.Column('name', sa.String(length=24), nullable=False, comment='用户名'),
    sa.Column('password', sa.String(length=100), nullable=True, comment='密码'),
    sa.Column('avatar', sa.String(length=255), nullable=True, comment='头像'),
    sa.Column('background', sa.String(length=255), nullable=True, comment='主页背景图'),
    sa.Column('sign', sa.String(length=255), nullable=True, comment='简介'),
    sa.Column('birthday', sa.DateTime(), nullable=True, comment='出生日期'),
    sa.Column('gender', sa.SmallInteger(), nullable=True, comment='性别，0-保密，1-女，2-男'),
    sa.Column('location', sa.String(length=255), nullable=True, comment='住址'),
    sa.Column('is_valid', sa.Boolean(), nullable=True, comment='当前用户是否为激活状态'),
    sa.Column('group_id', sa.Integer(), nullable=True, comment='用户所属权限组id, 0-超级管理员，1-管理员，2-普通用户'),
    sa.Column('is_vip', sa.Integer(), nullable=True, comment='是否为VIP, 0-普通1-7等级'),
    sa.Column('status', sa.SmallInteger(), nullable=True, comment='当前用户状态，0-正常，1-禁言，2-拉黑'),
    sa.Column('open_id', sa.String(length=200), nullable=True, comment='微信openid'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('group')
    op.drop_table('file')
    op.drop_table('auth')
    # ### end Alembic commands ###