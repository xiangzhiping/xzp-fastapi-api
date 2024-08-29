from colorama import Fore
import logging
from os import cpu_count

# 应用程序标题，用于标识和宣传
TITLE = 'xzp-fastapi-api'

# 应用程序版本号，用于版本管理
VERSION = '1.0'

# 服务器主机地址，设置为0.0.0.0表示监听所有可用网络接口
HOST = '0.0.0.0'

# 服务器端口，用于接收客户端请求
PORT = 8976

# 是否启用应用热重载，提高开发效率
APP_HOT_RELOAD = True

# 根据是否启用热重载决定工作进程数，热重载时只需1个，否则根据CPU数量增加
WORKERS = 1 if APP_HOT_RELOAD else cpu_count() // 2

# 日志记录级别，WARN用于警告级别的日志记录
LOG_LEVEL = logging.WARN

# 是否记录访问日志，关闭以减少日志量
ACCESS_LOG = False

# 热重载时的延迟时间，用于等待资源释放
RELOAD_DELAY = 0

# 默认的运行环境，用于区分开发、测试、生产环境
DEFAULT_RUN_DEV = 'dev'

# API的根路径前缀，用于构建API的URL
ROOT_PREFIX = '/xzp'

# 系统运行配置，用于存储和访问系统运行时的配置信息
SYS_RUN_CONFIG = {}

SNOWFLAKE_ID_GENERATORS = []

# 定义运行环境变量名，用于标识代码运行的环境配置
RUNNING_ENV = "RUNNINGENV"

# 定义数据ID的字符串，用于特定数据标识
NACOS_DATA_ID = ".configuration.set"

# 定义授权有效期，单位为天，用于规定授权令牌的有效时间
AUTHORIZATION_EFFECTIVE_DAYS = 15

# 定义时间格式字符串，用于匹配和验证日期时间的格式
DATETIME = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}, \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'

# 时间字段映射，用于将特定的时间关键字映射到对应的时间字段名
TIME_FIELD_MAP = {
    'login_time_start': 'login_time', 'login_time_end': 'login_time',
    'logout_time_start': 'logout_time', 'logout_time_end': 'logout_time',
    'create_time_start': 'create_time', 'create_time_end': 'create_time',
    'update_time_start': 'update_time', 'update_time_end': 'update_time',
    'delete_time_start': 'delete_time', 'delete_time_end': 'delete_time'
}

# 颜色映射用于将颜色名称映射到对应的颜色值
COLORS = {
    "red": Fore.LIGHTRED_EX,
    "green": Fore.LIGHTGREEN_EX,
    "blue": Fore.LIGHTBLUE_EX,
    "yellow": Fore.LIGHTYELLOW_EX,
    "cyan": Fore.LIGHTCYAN_EX,
    "magenta": Fore.LIGHTMAGENTA_EX,
    "black": Fore.LIGHTBLACK_EX,
    "white": Fore.LIGHTWHITE_EX
}

# HTTP状态码含义映射，用于将HTTP状态码转换为对应的描述性信息
HTTP_STATUS_CODE_MEAN_MAP = {
    100: '客户端应继续其请求',
    101: '服务器根据客户端的请求切换协议',
    200: '请求成功!',
    201: '请求已成功，并且服务器已创建了新的资源',
    202: '服务器已接受请求，但尚未处理',
    203: '服务器成功处理了请求，但返回的信息可能来自另一来源',
    204: '服务器成功处理了请求，但没有返回任何内容',
    205: '服务器成功处理了请求，但没有返回任何内容，并要求请求者重置文档视图',
    206: '服务器已经成功处理了部分GET请求',
    300: '针对请求，服务器可执行多种操作，服务器可根据请求者选择一项操作',
    301: '请求的URL已永久移动到新位置',
    302: '请求的URL临时从不同位置响应',
    303: '请求者应当对不同的位置使用单独的GET请求来检索响应',
    304: '自从上次请求后，请求的URL未修改过',
    305: '请求者只能使用代理访问请求的URL',
    307: '请求的资源临时从不同位置响应，但请求者应继续使用原有位置来进行以后的请求',
    400: '服务器无法理解请求的格式，客户端不应当尝试再次使用相同的内容发起请求',
    401: '请求要求身份验证',
    402: '请求要求进行付款',
    403: '请求未携带身份凭证[authorization]!',
    404: '服务器找不到请求的URL',
    405: '请求方式错误!',
    406: '无法使用请求的内容特性响应请求的URL',
    407: '需要代理服务器的身份验证',
    408: '服务器等候请求时发生超时',
    409: '服务器在完成请求时发生冲突',
    410: '请求的资源已永久删除',
    411: '服务器拒绝不含有效内容长度标头字段的请求',
    412: '服务器未满足请求者在请求中设置的其中一个前提条件',
    413: '服务器拒绝处理请求，因为请求实体过大',
    414: '请求的URI过长，服务器无法处理',
    415: '请求的格式不受请求页面的支持',
    416: '请求范围不符合要求',
    417: '服务器未满足期望请求标头字段的要求',
    500: '服务器内部错误，无法完成请求',
    501: '服务器不具备完成请求的功能，例如无法识别请求方法',
    502: '服务器作为网关或代理，从上游服务器收到无效响应',
    503: '服务器目前无法使用，通常是因为过载或停机维护',
    504: '服务器作为网关或代理，未及时从上游服务器接收请求',
    505: '服务器不支持请求中所用的HTTP协议版本',
}

# 全局存储，用于存储全局变量，如用户信息、角色信息、API信息等
GLOBAL_STORE = {
    'NO_AUTHORIZATION_ACCESSIBLE_PATHS': [],
    'SWAGGER_UI_PATHS': ["/openapi.json", "/docs", "/redoc"],
    'ROUTERS_MAP': {},
    'USER': {},
    "user": {},
    "role": {},
    "api": {}
}

# 定义Snowflake ID生成器所需的常量，64位ID结构的位划分。
# Snowflake ID结构:
#   - 1 bit 不使用（总是为0，可以在实际应用中忽略，这里未定义）
#   - DATACENTER_ID_BITS bits 数据中心ID
#   - WORKER_ID_BITS bits 机器ID（或进程ID）
#   - SEQUENCE_BITS bits 序列号，用于同一毫秒内生成多个ID

# 机器ID位数
WORKER_ID_BITS = 5  # 允许每个数据中心有最多 2^5 - 1 = 31 个工作机器或进程
# 数据中心ID位数
DATACENTER_ID_BITS = 5  # 允许最多 2^5 - 1 = 31 个数据中心
# 序列号位数，用于记录同毫秒内产生的ID序列
SEQUENCE_BITS = 12  # 每毫秒可以生成 2^12 = 4096 个ID

# 计算各个部分的最大值
# 使用位运算计算最大值，避免直接使用数学运算，提高效率
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 计算机器ID的最大值
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)  # 计算数据中心ID的最大值

# 计算时间戳、数据中心ID、机器ID的位移量
# 这些位移量用于将各个部分按位拼接成最终的ID
WORKER_ID_SHIFT = SEQUENCE_BITS  # 机器ID左移位数
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS  # 数据中心ID左移位数
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS  # 时间戳左移位数

# 生成序列号的掩码，用于确保序列号不超过最大值
# 通过位运算得到序列号的最大值对应的掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# 定义Snowflake ID计算中的起始时间戳，Twitter的Snowflake算法通常以某个固定时间点为基准
# 这里的时间戳为1288834974657，对应于2010-11-04 15:02:53 UTC
FIRST_YEAR_TIMESTAMP = 1288834974657
MAX_PROCESS_ID = 127  # 假设最大进程ID为127
MAX_SEQUENCE = 0x3FF  # 序列号的最大长度为10位
