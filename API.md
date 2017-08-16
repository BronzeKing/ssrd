# API文档

本文档主要描述接口请求范例与接口返回范例

### 权限验证

API访问权限控制基于token，token为一段加密的字符串，首次获取根据用户邮箱和密码请求获取，之后的接口访问带上请求头部HEADER信息：identify：token。


	1.  请求API获得token
	    POST /token/
	    BODY:
	    email: demo@chinavivaki.com
	    password: 123456

	    RESPONSE:
	    {'token': 'asdsfdsfadsfsdfasdfsdaf'}

	2.  请求示例
	    GET /user/1/
	    HEADER:
	    {'identify': 'asdsfdsfadsfsdfasdfsdaf'}
	    RESPONSE:
	    {
	        'username': 'demo',
	        'status': 'ACTIVE'
	        }
	    }


## 参数和权限验证
请求接口时需要登录，则重定向到登录页面或者其他情况需要重定向时返回HTTP Response Code 返回302

    Example
    GET /user

    RESPONSE
    Status Code 302
        {"msg": "/#/login"}    //假设/#/login是登录界面

参数验证失败时 HTTP Response Code 返回400.

    Example
    GET /user/0

    RESPONSE
    Status Code 400
        {
      "msg": "Validation Error",
      "errors": [
        {
          "name": "user",
          "value": "用户不存在或已停用"
        }
      ]
    }

权限验证失败时 HTTP Response Code 返回403

    Example
    GET /user/100/profile

    RESPONSE
    Status Code 403
        {
      "msg": "The request is understood, but it has been refused or access is not allowed"
    }
