from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import text
from code.conf.config import settings
import asyncio
engine:AsyncEngine|None=None
session_factory:async_sessionmaker[AsyncSession]|None=None

def create_db_engine():
    global engine,session_factory
    engine=create_async_engine(settings.database_url)
    session_factory=async_sessionmaker(engine,expire_on_commit=False)
    #这里的expire_on_commit的解释：
    # from sqlalchemy.orm import Session
    #
    # with Session(engine) as session:
    #     spongebob = User(
    #         name="spongebob",
    #         fullname="Spongebob Squarepants",
    #         addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    #     )
    #     sandy = User(
    #         name="sandy",
    #         fullname="Sandy Cheeks",
    #         addresses=[
    #             Address(email_address="sandy@sqlalchemy.org"),
    #             Address(email_address="sandy@squirrelpower.org"),
    #         ],
    #     )
    #     patrick = User(name="patrick", fullname="Patrick Star")
    #     session.add_all([spongebob, sandy, patrick])
    #     session.commit()
    #这里的add_all，还没有将数据提交到数据库里面，在commit后才会提交，如果expire_on_commit设置为
    #true到时候，如果commit后需要再访问对象里面的数据的时候，就访问不了原来的数据了，
    #比如写print(sandy.name) 因为可能其他的地方也会执行对sandy的数据库里面的操作，那么有可能里面的
    #数据就会被改变，那么如果不设置为true，也就是对象不过期，那么拿到的数据就有可能为老的数据
    #数据就不对了，正确的应该是在数据库中直接读最新的数据，那么这里如果设置true，也是可以直接print(sandy.name)
    #的，只不过数据不是在对象里面拿，而是会直接隐藏生成一条sql语句，从数据库中查询最新的数据，在返回
    #但是上面是在同步的时候，如果是异步的话，那么必须设置为false，因为如果为true，语法中不支持 await print(sand.name)
    #也就是不可以await访问对象里面的属性，因为必须加await，因为要从数据库里面拿数据，如果为false 就可以直接
    # print(sandy.name)因为不需要从数据库里面访问，直接从对象里面的属性里面拿到数据，但是拿到的数据就有可能不是
    # 最新的，但是如果确实需要提交后再拿到数据，并且要拿到最新的，那么就可以直接自己写sql语句，再查询拿到结果


    #返回的是一个async_sessionmaker对象，里面有__call__魔术方法，当调用session_factory()的
    #时候，就会调用创建asyncsession的方法，创建这么一个session ，当结束后就自动释放链接
async def close_db_engine():
     await engine.dispose()

if __name__ == '__main__':
    async def test():
        create_db_engine()
        async with session_factory() as session:
            result=await session.execute(text("select 1"))
            x=result.fetchall()
            print(x)
            print(type(x))
            print(type(x[0]))
        await close_db_engine()

    asyncio.run(test())
