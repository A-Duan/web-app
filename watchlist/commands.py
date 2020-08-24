# 命令函数
import click

from watchlist import app,db
from watchlist.models import User,Movie

# 创建数据库
@app.cli.command()
@click.option('--drop',is_flag=True,help='Create after drop.')
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')



@app.cli.command()
def forge():
    db.create_all()
    name = 'ZhaoYuChen'
    movies = [
        {'title': 'My Neighbor Totoro','year': '1998'},
        {'title': 'Dead Poets Society','year': '1989'},
        {'title': 'Leon','year': '1994'},
        {'title': 'A Perfect World','year': '1993'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


# 设置用户认证
@app.cli.command()
@click.option('--username',prompt=True,help='The username used to login.')
@click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True,help='The password used to login.')
def admin(username,password):
    """Create user"""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user=User(username=username,name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')