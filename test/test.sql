create table sys_api_tag
(
    tag_id      int auto_increment comment '标签id' primary key,
    tag_name    varchar(50)                               not null comment '标签名称',
    tag_path    varchar(50)                               not null comment '标签路径',
    data_status enum ('0', '1') default '1'               not null comment '数据状态（有效 1，无效 0）',
    operator    bigint                                    not null comment '操作者',
    create_time datetime        default CURRENT_TIMESTAMP not null comment '创建时间',
    update_time datetime                                  null comment '更新时间',
    delete_time datetime                                  null comment '删除时间'
)
    comment '系统接口标签表';

create table login_logs
(
    login_id    int auto_increment comment '登录日志id' primary key,
    login_ip    varchar(30)                               not null comment '登录IP',
    login_res   enum ('0', '1') default '1'               not null comment '登录结果（成功 1，失败 0）',
    login_code  int(5)                                    not null comment '登录状态码',
    login_msg   varchar(255)                              not null comment '登录消息',
    login_data  text                                      null comment '登录数据',
    data_status enum ('0', '1') default '1'               not null comment '数据状态（有效 1，无效 0）',
    operator    bigint                                    not null comment '操作者',
    create_time datetime        default CURRENT_TIMESTAMP not null comment '创建时间',
    update_time datetime                                  null comment '更新时间',
    delete_time datetime                                  null comment '删除时间'
)
    comment '登录日志表';

create table sys_api
(
    api_id      int auto_increment comment '接口id' primary key,
    api_path    varchar(50)                               not null comment '接口路径',
    api_name    varchar(50)                               not null comment '接口名称',
    api_type    varchar(30)                               not null comment '接口类型',
    req_method  enum ('GET', 'POST', 'PUT', 'DELETE')     null comment '请求方式',
    tag_id      int                                       not null comment '标签id',
    auth_access enum ('0', '1') default '1'               not null comment '身份验证访问（需要 1，不需要 0）',
    data_status enum ('0', '1') default '1'               not null comment '数据状态（有效 1，无效 0）',
    operator    bigint                                    not null comment '操作者',
    create_time datetime        default CURRENT_TIMESTAMP not null comment '创建时间',
    update_time datetime                                  null comment '更新时间',
    delete_time datetime                                  null comment '删除时间'
)
    comment '系统接口表';

create table user
(
    user_id        bigint                                    not null comment '用户id'
        primary key,
    username       varchar(100)                              not null comment '用户名',
    password       varchar(100)                              not null comment '用户密码',
    phone          varchar(15)                               null comment '电话',
    email          varchar(50)                               null comment '邮箱',
    wechat         varchar(50)                               null comment '微信',
    login_status   enum ('0', '1') default '1'               not null comment '登录状态（在线 1，离线 0）',
    account_status enum ('0', '1') default '1'               not null comment '账号状态（有效 1，无效 0）',
    login_time     datetime                                  null comment '登录时间',
    logout_time    datetime                                  null comment '离线时间',
    data_status    enum ('0', '1') default '1'               not null comment '数据状态（有效 1，无效 0）',
    operator       bigint                                    not null comment '操作者',
    create_time    datetime        default CURRENT_TIMESTAMP not null comment '创建时间',
    update_time    datetime                                  null comment '更新时间',
    delete_time    datetime                                  null comment '删除时间'
)
    comment '用户表';


create table user_permission
(
    user_id     bigint                                    not null comment '用户id' primary key,
    role_id     int                                       not null comment '角色id',
    path_ids    json                                      null comment '接口路径id列表',
    data_status enum ('0', '1') default '1'               not null comment '数据状态（有效 1，无效 0）',
    operator    bigint                                    not null comment '操作者',
    create_time datetime        default CURRENT_TIMESTAMP not null comment '创建时间',
    update_time datetime                                  null comment '更新时间',
    delete_time datetime                                  null comment '删除时间'
)
    comment '用户权限表';



create table user_role
(
    role_id     int auto_increment comment '角色id' primary key,
    role_name   varchar(50)                               not null comment '角色名称',
    role_level  tinyint(1)                                not null comment '角色级别（超级管理员 1， 普通用户 0， 专业管理员 [其他数字]）',
    path_ids    json                                      null comment '接口路径id列表',
    data_status enum ('0', '1') default '1'               not null comment '数据状态（有效 1，无效 0）',
    operator    bigint                                    not null comment '操作者',
    create_time datetime        default CURRENT_TIMESTAMP not null comment '创建时间',
    update_time datetime                                  null comment '更新时间',
    delete_time datetime                                  null comment '删除时间'
)
    comment '用户角色表';


drop table user;
drop table user_permission;
drop table user_role;
drop table login_logs;
drop table sys_api;
drop table sys_api_tag;
