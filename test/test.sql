create table sys_api_tag
(
    tag_id      int auto_increment comment '��ǩid' primary key,
    tag_name    varchar(50)                               not null comment '��ǩ����',
    tag_path    varchar(50)                               not null comment '��ǩ·��',
    data_status enum ('0', '1') default '1'               not null comment '����״̬����Ч 1����Ч 0��',
    operator    bigint                                    not null comment '������',
    create_time datetime        default CURRENT_TIMESTAMP not null comment '����ʱ��',
    update_time datetime                                  null comment '����ʱ��',
    delete_time datetime                                  null comment 'ɾ��ʱ��'
)
    comment 'ϵͳ�ӿڱ�ǩ��';

create table login_logs
(
    login_id    int auto_increment comment '��¼��־id' primary key,
    login_ip    varchar(30)                               not null comment '��¼IP',
    login_res   enum ('0', '1') default '1'               not null comment '��¼������ɹ� 1��ʧ�� 0��',
    login_code  int(5)                                    not null comment '��¼״̬��',
    login_msg   varchar(255)                              not null comment '��¼��Ϣ',
    login_data  text                                      null comment '��¼����',
    data_status enum ('0', '1') default '1'               not null comment '����״̬����Ч 1����Ч 0��',
    operator    bigint                                    not null comment '������',
    create_time datetime        default CURRENT_TIMESTAMP not null comment '����ʱ��',
    update_time datetime                                  null comment '����ʱ��',
    delete_time datetime                                  null comment 'ɾ��ʱ��'
)
    comment '��¼��־��';

create table sys_api
(
    api_id      int auto_increment comment '�ӿ�id' primary key,
    api_path    varchar(50)                               not null comment '�ӿ�·��',
    api_name    varchar(50)                               not null comment '�ӿ�����',
    api_type    varchar(30)                               not null comment '�ӿ�����',
    req_method  enum ('GET', 'POST', 'PUT', 'DELETE')     null comment '����ʽ',
    tag_id      int                                       not null comment '��ǩid',
    auth_access enum ('0', '1') default '1'               not null comment '�����֤���ʣ���Ҫ 1������Ҫ 0��',
    data_status enum ('0', '1') default '1'               not null comment '����״̬����Ч 1����Ч 0��',
    operator    bigint                                    not null comment '������',
    create_time datetime        default CURRENT_TIMESTAMP not null comment '����ʱ��',
    update_time datetime                                  null comment '����ʱ��',
    delete_time datetime                                  null comment 'ɾ��ʱ��'
)
    comment 'ϵͳ�ӿڱ�';

create table user
(
    user_id        bigint                                    not null comment '�û�id'
        primary key,
    username       varchar(100)                              not null comment '�û���',
    password       varchar(100)                              not null comment '�û�����',
    phone          varchar(15)                               null comment '�绰',
    email          varchar(50)                               null comment '����',
    wechat         varchar(50)                               null comment '΢��',
    login_status   enum ('0', '1') default '1'               not null comment '��¼״̬������ 1������ 0��',
    account_status enum ('0', '1') default '1'               not null comment '�˺�״̬����Ч 1����Ч 0��',
    login_time     datetime                                  null comment '��¼ʱ��',
    logout_time    datetime                                  null comment '����ʱ��',
    data_status    enum ('0', '1') default '1'               not null comment '����״̬����Ч 1����Ч 0��',
    operator       bigint                                    not null comment '������',
    create_time    datetime        default CURRENT_TIMESTAMP not null comment '����ʱ��',
    update_time    datetime                                  null comment '����ʱ��',
    delete_time    datetime                                  null comment 'ɾ��ʱ��'
)
    comment '�û���';


create table user_permission
(
    user_id     bigint                                    not null comment '�û�id' primary key,
    role_id     int                                       not null comment '��ɫid',
    path_ids    json                                      null comment '�ӿ�·��id�б�',
    data_status enum ('0', '1') default '1'               not null comment '����״̬����Ч 1����Ч 0��',
    operator    bigint                                    not null comment '������',
    create_time datetime        default CURRENT_TIMESTAMP not null comment '����ʱ��',
    update_time datetime                                  null comment '����ʱ��',
    delete_time datetime                                  null comment 'ɾ��ʱ��'
)
    comment '�û�Ȩ�ޱ�';



create table user_role
(
    role_id     int auto_increment comment '��ɫid' primary key,
    role_name   varchar(50)                               not null comment '��ɫ����',
    role_level  tinyint(1)                                not null comment '��ɫ���𣨳�������Ա 1�� ��ͨ�û� 0�� רҵ����Ա [��������]��',
    path_ids    json                                      null comment '�ӿ�·��id�б�',
    data_status enum ('0', '1') default '1'               not null comment '����״̬����Ч 1����Ч 0��',
    operator    bigint                                    not null comment '������',
    create_time datetime        default CURRENT_TIMESTAMP not null comment '����ʱ��',
    update_time datetime                                  null comment '����ʱ��',
    delete_time datetime                                  null comment 'ɾ��ʱ��'
)
    comment '�û���ɫ��';


drop table user;
drop table user_permission;
drop table user_role;
drop table login_logs;
drop table sys_api;
drop table sys_api_tag;
