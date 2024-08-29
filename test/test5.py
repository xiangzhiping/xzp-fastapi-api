import pymysql
import random
import asyncio
from utils.snowflake_id_generator import SnowflakeIdGenerator
from datetime import datetime, timedelta
from utils.pure_digital_uuid_generator import PureDigitalUuidGenerator

sig = SnowflakeIdGenerator(*(26, 4, 3124))

# 连接数据库
connection = pymysql.connect(
    host='localhost',
    user='xzp_dev_mysql_username1',
    password='xzp_dev_mysql_password',
    database='xzp_dev_mysql',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


def generate_chinese_nickname(length_range=(2, 10)):
    # 汉字的 Unicode 范围
    start_code_point = 0x4E00  # CJK Unified Ideographs
    end_code_point = 0x9FA5  # CJK Unified Ideographs
    length = random.randint(*length_range)
    return ''.join(chr(random.randint(start_code_point, end_code_point)) for _ in range(length))


async def main():
    try:
        with connection.cursor() as cursor:
            for i in range(100000):
                try:
                    user_id = await sig.nextid()
                    nickname = generate_chinese_nickname()
                    phone = f'{random.randint(10000000000, 99999999999)}'
                    email = f'{random.randint(1000000000, 9999999999)}@qq.com'
                    password = '$2b$12$M2wR6ftyEtO6ha4g8HSEcOXqcRq7xzPQnpTV6o7TRa8flRfE3T1iG'
                    avatar_key = f'avatars/{await PureDigitalUuidGenerator()}.png'
                    login_status = random.choice([0, 1])
                    account_status = 1
                    login_datetime = datetime.now() - timedelta(days=random.randint(0, 365))
                    logout_datetime = None if login_status == 1 else login_datetime - timedelta(
                        hours=random.randint(1, 24))
                    user_status = 1
                    operator = 7225449773631762432
                    create_datetime = datetime.now()
                    update_datetime = datetime.now() if random.choice([0, 1]) == 1 else None
                    delete_datetime = None

                    print(
                        f"user_id: {user_id},nickname: {nickname}, phone: {phone}, email: {email}, password: {password}, avatar_key: {avatar_key}, login_status: {login_status}, account_status: {account_status}, login_datetime: {login_datetime}, logout_datetime: {logout_datetime}, user_status: {user_status}, operator: {operator}")

                    # 插入单条数据
                    sql = """
                    INSERT INTO user (user_id, nickname, phone, email, password, avatar_key, login_status, account_status, login_datetime, logout_datetime, user_status, operator_id, create_datetime, update_datetime, delete_datetime)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    cursor.execute(sql, (
                        user_id, nickname, phone, email, password, avatar_key, login_status, account_status,
                        login_datetime,
                        logout_datetime, user_status, operator, create_datetime, update_datetime, delete_datetime))
                    connection.commit()

                except pymysql.err.IntegrityError as e:
                    print(f"Integrity error occurred: {e}. Skipping this entry.")
                    continue
    finally:
        print("数据已插入完成")
        connection.close()


asyncio.run(main())
