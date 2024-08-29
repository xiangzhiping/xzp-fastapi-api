import inspect
import re

sysApiInfoArr = []


def sysApiInfoGet(app):
    global api_params, param
    api_info = []

    def process_response(responses, response_type):
        processed_responses = []
        if responses is None:
            return None
        if responses[0] == "file":
            return "file"
        if response_type == "failure":
            for response in responses:
                code_match = re.search(r"HTTP_(\d+)", response)
                msg_match = re.search(r',\s*"(.*?)",', response)  # 修改正则表达式
                data_match = re.search(r",\s*(\w+)\)", response)

                code = int(code_match.group(1)) if code_match else None
                msg = msg_match.group(1) if msg_match else None

                if data_match:
                    data = data_match.group(1)
                    if data == 'None':
                        data = None
                else:
                    data = None

                processed_responses.append({
                    "code": code,
                    "msg": msg,
                    "data": data
                })
        elif response_type == "error":
            code_match = re.search(r"HTTP_(\d+)", responses)
            # print(responses)
            msg_match = re.search(r',\s*"(.*?)",', responses)  # 修改正则表达式
            data_match = re.search(r",\s*(\w+)\)", responses)

            code = int(code_match.group(1)) if code_match else None
            msg = msg_match.group(1) if msg_match else None
            data = data_match.group(1) if data_match else "err msg"

            processed_responses = {
                "code": code,
                "msg": msg,
                "data": data
            }

        return processed_responses

    def get_route_tags(route):
        tags = route.__dict__.get('tags')
        return tags[0] if tags else None

    def extract_response(endpoint_source, response_type):
        if response_type == "success":
            patterns = [
                r"JsonResponse\(HTTP_200_OK[^)]*\)",
                r"StreamingResponse\((?:.|\n)*?\)",
                r"FileResponse\((?:.|\n)*?\)",
            ]
        elif response_type == "failure":
            patterns = [r"JsonResponse\(HTTP_(?!200)[^)]*\)"]
        elif response_type == "error":
            pattern = r"HttpException\(HTTP_500[^)]*\)"
            response_match = re.search(pattern, endpoint_source, re.DOTALL)
            return response_match.group() + ")" if response_match else None
        else:
            return None

        response_matches = []
        for pattern in patterns:
            matches = re.findall(pattern, endpoint_source, re.DOTALL)
            if matches and (pattern == r"StreamingResponse\((?:.|\n)*?\)" or pattern == r"FileResponse\((?:.|\n)*?\)"):
                response_matches.extend(["file"])
            else:
                response_matches.extend(matches)
        return list(set(response_matches)) if response_matches else None

    names = set()
    for route in filter(lambda r: hasattr(r.endpoint, '__call__'), app.routes):
        added = False

        # # 提取 View 类名
        view_class_name = re.findall(r'return await (\w+)', inspect.getsource(route.endpoint))[0] if re.findall(
            r'return await (\w+)', inspect.getsource(route.endpoint)) else None

        # 获取 View 类的引用
        if view_class_name:
            view_class = route.endpoint.__globals__[view_class_name]

            # 获取 View 类的源代码
            view_class_source = inspect.getsource(view_class)
        else:
            view_class_source = None
        # endpoint_source = inspect.getsource(route.endpoint)

        if view_class_source is not None:
            success_res = extract_response(view_class_source, "success")
            failure_res = extract_response(view_class_source, "failure")
            error_res = extract_response(view_class_source, "error")
        else:
            success_res = None
            failure_res = None
            error_res = None
        for param_name, param in inspect.signature(route.endpoint).parameters.items():
            if isinstance(param.annotation, str):
                continue

            for key, value in param.annotation.__annotations__.items():
                # 迭代的代码逻辑

                # rest of your code

                # if param_name != 'req' or param_name != "file":
                #     continue
                # print(param_name, type(param_name))

                added = True
                if param_name == "file":
                    api_params = "file"
                else:
                    api_params = {
                        key: (
                            value.__name__.replace("'", "") if hasattr(value, '__name__') else str(value).replace("'", ""))
                        for key, value in param.annotation.__annotations__.items()
                    }
                if api_params == {"_form": "Optional"} or api_params == {}:
                    api_params = None
                api_info.append({
                    "path": route.path,
                    "name": route.name,
                    "method": "GET" if list(route.methods)[0] == "HEAD" else list(route.methods)[0],
                    "tag": get_route_tags(route),
                    "params": api_params,
                    "req": param.annotation.__name__,
                    "controllers": route.endpoint.__name__,
                    "view": re.findall(r'return await (\w+)', inspect.getsource(route.endpoint))[0] if re.findall(
                        r'return await (\w+)', inspect.getsource(route.endpoint)) else None,
                    "successRes": None,
                    "failureRes": process_response(failure_res, "failure"),
                    "errorRes": process_response(error_res, "error"),
                    "loginAccess": True,
                })
                names.add(route.name)

            if not added:
                api_info.append({
                    "path": route.path,
                    "name": route.name,
                    "method": "GET" if list(route.methods)[0] == "HEAD" else list(route.methods)[0],
                    "tag": get_route_tags(route),
                    "params": api_params,
                    "successRes": None,
                    "failureRes": process_response(failure_res, "failure"),
                    "errorRes": process_response(error_res, "error"),
                    "req": param.annotation.__name__,
                    "controllers": route.endpoint.__name__,
                    "view": re.findall(r'return await (\w+)', inspect.getsource(route.endpoint))[0] if re.findall(
                        r'return await (\w+)', inspect.getsource(route.endpoint)) else None,
                    "loginAccess": True,
                })
                names.add(route.name)

    return api_info
