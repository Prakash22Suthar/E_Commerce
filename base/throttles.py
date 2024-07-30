from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

count = 0
class CustomAnonRateThrottle(AnonRateThrottle):
    def allow_request(self, request, view):
        """ created custom throttle class for except 5 request by anonymous user"""
        global count
        count+=1
        if count>=5:
            # count = 0 # this will set count=0 to unable user to make new request .
            return False
        return True

class CustomUserRateThrottle(UserRateThrottle):
     scope = 'my_custom_scope'
     def allow_request(self, request, view):
         if request.method == 'GET':
            self.scope = 'get_scope'
            self.rate = '10/hour'
            return True
         return super().allow_request(request, view)