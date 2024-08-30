-- 登录日志表
CREATE TABLE login_log
(
    login_id        INT AUTO_INCREMENT COMMENT '登录日志id'
        PRIMARY KEY,
    login_ip        VARCHAR(30)                          NOT NULL COMMENT '登录IP',
    login_res       TINYINT(1) DEFAULT 1                 NOT NULL COMMENT '登录结果（成功 1，失败 0）',
    login_code      INT(5)                               NOT NULL COMMENT '登录状态码',
    login_msg       VARCHAR(255)                         NOT NULL COMMENT '登录消息',
    login_data      TEXT                                 NULL COMMENT '登录数据',
    log_status      TINYINT(1) DEFAULT 1                 NOT NULL COMMENT '日志状态（有效 1，无效 0）',
    operator_id     BIGINT                               NOT NULL COMMENT '操作者个人ID',
    create_datetime DATETIME   DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建日期时间',
    update_datetime DATETIME                             NULL COMMENT '更新日期时间',
    delete_datetime DATETIME                             NULL COMMENT '删除日期时间'
) COMMENT '登录日志表';

CREATE INDEX login_log_create_datetime_index ON login_log (create_datetime);
CREATE INDEX login_log_login_ip_index ON login_log (login_ip);
CREATE INDEX login_log_login_msg_index ON login_log (login_msg);

ALTER TABLE login_log
    ENGINE = InnoDB;

-- 系统接口表
CREATE TABLE sys_api
(
    api_id          INT AUTO_INCREMENT COMMENT '接口id'
        PRIMARY KEY,
    api_name        VARCHAR(50)                                    NOT NULL COMMENT '接口名称',
    api_path        VARCHAR(50)                                    NOT NULL COMMENT '接口路径',
    api_type        VARCHAR(30)                                    NOT NULL COMMENT '接口类型',
    req_method      ENUM ('get', 'post', 'put', 'delete', 'patch') NULL COMMENT '请求方式',
    tag_name        VARCHAR(30)                                    NULL COMMENT '标签名称',
    tag_path        VARCHAR(50)                                    NULL COMMENT '标签路径',
    auth_access     TINYINT(1) DEFAULT 1                           NOT NULL COMMENT '身份验证访问（需要 1，不需要 0）',
    api_status      TINYINT(1) DEFAULT 1                           NOT NULL COMMENT '接口状态（有效 1，无效 0）',
    operator_id     BIGINT                                         NOT NULL COMMENT '操作者个人ID',
    create_datetime DATETIME   DEFAULT CURRENT_TIMESTAMP           NOT NULL COMMENT '创建日期时间',
    update_datetime DATETIME                                       NULL COMMENT '更新日期时间',
    delete_datetime DATETIME                                       NULL COMMENT '删除日期时间',
    CONSTRAINT sys_api_pk UNIQUE (api_name),
    CONSTRAINT sys_api_pk_2 UNIQUE (api_path)
) COMMENT '系统接口表';

CREATE INDEX sys_api_create_datetime_index ON sys_api (create_datetime);
CREATE INDEX sys_api_update_datetime_index ON sys_api (update_datetime);

ALTER TABLE sys_api
    ENGINE = InnoDB;

-- 用户表
CREATE TABLE user
(
    user_id         BIGINT UNSIGNED                      NOT NULL COMMENT '用户id'
        PRIMARY KEY,
    nickname        varchar(15)                          null comment '昵称',
    phone           VARCHAR(15)                          NULL COMMENT '电话',
    email           VARCHAR(50)                          NULL COMMENT '邮箱',
    password        VARCHAR(60)                          NOT NULL COMMENT '用户密码',
    avatar_key      VARCHAR(100)                         NULL COMMENT '头像（个人头像唯一key）',
    login_status    TINYINT(1) DEFAULT 0                 NOT NULL COMMENT '登录状态（在线 1，离线 0）',
    account_status  TINYINT(1) DEFAULT 1                 NOT NULL COMMENT '账号状态（有效 1，无效 0）',
    login_datetime  DATETIME                             NULL COMMENT '登录日期时间',
    logout_datetime DATETIME                             NULL COMMENT '登出日期时间',
    user_status     TINYINT(1) DEFAULT 1                 NOT NULL COMMENT '用户状态（有效 1，无效 0）',
    operator_id     BIGINT                               NOT NULL COMMENT '操作者个人ID',
    create_datetime DATETIME   DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建日期时间',
    update_datetime DATETIME                             NULL COMMENT '更新日期时间',
    delete_datetime DATETIME                             NULL COMMENT '删除日期时间',
    CONSTRAINT user_pk UNIQUE (phone),
    CONSTRAINT user_pk_2 UNIQUE (email),
    CONSTRAINT user_pk_3 UNIQUE (avatar_key)
) COMMENT '用户表';
CREATE INDEX user_login_datetime_index ON user (create_datetime);
ALTER TABLE user
    ENGINE = InnoDB;

insert into xzp_dev_mysql.user (user_id, nickname, phone, email, password, avatar_key, login_status, account_status,
                                login_datetime, logout_datetime, user_status, operator_id, create_datetime,
                                update_datetime, delete_datetime)
values (7235163934879406592, '系统默认超级管理员', '17820512394', '3264633124@qq.com',
        '$2b$12$M2wR6ftyEtO6ha4g8HSEcOXqcRq7xzPQnpTV6o7TRa8flRfE3T1iG', 'avatars/3833739814745750935736639922512.png',
        0, 1, '2024-04-19 13:58:25', '2024-04-19 06:58:25', 1, 7235163934879406592, '2024-08-30 13:58:25',
        '2024-08-30 13:58:25', null);

-- 用户权限表
CREATE TABLE user_permission
(
    user_id           BIGINT                               NOT NULL COMMENT '用户ID'
        PRIMARY KEY,
    role_id           INT                                  NOT NULL COMMENT '角色ID',
    paths             JSON                                 NULL COMMENT '接口路径ID列表',
    permission_status TINYINT(1) DEFAULT 1                 NOT NULL COMMENT '权限状态（有效 1，无效 0）',
    operator_id       BIGINT                               NOT NULL COMMENT '操作者个人ID',
    create_datetime   DATETIME   DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建日期时间',
    update_datetime   DATETIME                             NULL COMMENT '更新日期时间',
    delete_datetime   DATETIME                             NULL COMMENT '删除日期时间'
) COMMENT '用户权限表';

CREATE INDEX user_permission_create_datetime_index ON user_permission (create_datetime);
CREATE INDEX user_permission_delete_datetime_index ON user_permission (delete_datetime);
CREATE INDEX user_permission_update_datetime_index ON user_permission (update_datetime);

ALTER TABLE user_permission
    ENGINE = InnoDB;

-- 用户角色表
CREATE TABLE user_role
(
    role_id         INT AUTO_INCREMENT COMMENT '角色id'
        PRIMARY KEY,
    role_name       VARCHAR(50)                          NOT NULL COMMENT '角色名称',
    role_level      TINYINT(1)                           NOT NULL COMMENT '角色级别（超级管理员 1， 普通用户 0， 专业管理员 [其他数字]）',
    paths           JSON                                 NULL COMMENT '接口路径id列表',
    role_status     TINYINT(1) DEFAULT 1                 NOT NULL COMMENT '角色状态（有效 1，无效 0）',
    operator_id     BIGINT                               NOT NULL COMMENT '操作者个人ID',
    create_datetime DATETIME   DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建日期时间',
    update_datetime DATETIME                             NULL COMMENT '更新日期时间',
    delete_datetime DATETIME                             NULL COMMENT '删除日期时间',
    CONSTRAINT user_role_pk UNIQUE (role_name)
) COMMENT '用户角色表';

CREATE INDEX user_role_create_datetime_index ON user_role (create_datetime);
CREATE INDEX user_role_delete_datetime_index ON user_role (delete_datetime);
CREATE INDEX user_role_update_datetime_index ON user_role (update_datetime);

ALTER TABLE user_role
    ENGINE = InnoDB;
