from src.controllers import personal, sys_api, sys, user_permission, user_role, user

routers = (
    user.router,
    user_role.router,
    user_permission.router,
    sys.router,
    sys_api.router,
    personal.router
)
