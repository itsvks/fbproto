'use strict';
pfadmin.service('djangoAuth', function djangoAuth($q, $http, $state, ipCookie) {
	var service = {
		'authenticated': null,
		'request': function(args) {
			if(ipCookie('token')){
				$http.defaults.headers.common.Authorization = 'Token ' + ipCookie('token');
			}
			params = args.params || {};
			args = args || {};
			var deferred = $q.defer(),
				url = this.API_URL + args.url,
				method = args.method || "GET",
				params = params,
				data = args.data || {},
				transform = args.transform;;
			// Fire the request, as configured.
			if(transform == "angular.identity"){
				$http({
					url: url,
					method: method.toUpperCase(),
					data: data,
					transformRequest: angular.identity,
					headers: {'Content-Type': undefined,'X-CSRFToken': ipCookie('csrftoken')}
				})
					.success(angular.bind(this,function(data, status, headers, config) {
						deferred.resolve(data, status);
					}))
					.error(angular.bind(this,function(data, status, headers, config) {
						console.log("error syncing with: " + url);
						// Set request status
						if(data){
							data.status = status;
						}
						if(status == 0){
							if(data == ""){
								data = {};
								data['status'] = 0;
								data['non_field_errors'] = ["Could not connect. Please try again."];
							}
							// or if the data is null, then there was a timeout.
							if(data == null){
								// Inject a non field error alerting the user
								// that there's been a timeout error.
								data = {};
								data['status'] = 0;
								data['non_field_errors'] = ["Server timed out. Please try again."];
							}
						}
						deferred.reject(data, status, headers, config);
					}));
				return deferred.promise;
			}
			else{
				$http({
					url: url,
					withCredentials: this.use_session,
					method: method.toUpperCase(),
					headers: {'X-CSRFToken': ipCookie('csrftoken')},
					params: params,
					data: data
				})
					.success(angular.bind(this,function(data, status, headers, config) {
						deferred.resolve(data, status);
					}))
					.error(angular.bind(this,function(data, status, headers, config) {
						console.log("error syncing with: " + url);
						// Set request status
						if(data){
							data.status = status;
						}
						if(status == 0){
							if(data == ""){
								data = {};
								data['status'] = 0;
								data['non_field_errors'] = ["Could not connect. Please try again."];
							}
							// or if the data is null, then there was a timeout.
							if(data == null){
								// Inject a non field error alerting the user
								// that there's been a timeout error.
								data = {};
								data['status'] = 0;
								data['non_field_errors'] = ["Server timed out. Please try again."];
							}
						}
						deferred.reject(data, status, headers, config);
					}));
				return deferred.promise;
			}
		},
		'register': function(args, rootScope){
			return this.request({
				'method': "POST",
				'url': "/register/",
				'data': args
			}).then(function(data){
				if(!djangoAuth.use_session){
					$http.defaults.headers.common.Authorization = 'Token ' + data.token;
					ipCookie('token',data.token, {expires: 4, expirationUnit: 'hours'});
				}
				rootScope.token = ipCookie('token');
			});
		},
		'login': function(args,rootScope){
			return this.request({
				'method': "POST",
				'url': "/login/",
				'data':{
					'email':args.email,
					'password':args.password
				}
			}).then(function(data){
				if(!djangoAuth.use_session){
					$http.defaults.headers.common.Authorization = 'Token ' + data.token;
					if(args.staysign){
						ipCookie('token',data.token, {expires: 4, expirationUnit: 'days'});
					}
					else{
						ipCookie('token',data.token, {expires: 4, expirationUnit: 'hours'});
					}
				}
				rootScope.token = ipCookie('token');
			});
		},
		'logout': function(rootScope){
			return this.request({
				'method': "GET",
				'url': "/logout/"
			}).then(function(data){
				delete $http.defaults.headers.common.Authorization;
				ipCookie.remove('token');
				rootScope.token = '';
				sessionStorage.clear();
				$state.go('login');
			},function(data){
				delete $http.defaults.headers.common.Authorization;
				ipCookie.remove('token');
				rootScope.token = '';
				sessionStorage.clear();
				$state.go('login');
			});
		},
		'profile': function(){
			return this.request({
				'method': "GET",
				'url': "/profile/"
			});
		},
		'updateprofile': function(args){
			return this.request({
				'method': "POST",
				'url': "/profile/",
				'data':args
			});
		},
		'updateprofilepic': function(args){
			return this.request({
				'method': "POST",
				'url': "/profile-image/",
				'data': args,
				'transform': 'angular.identity'
			});
		},
		'getprofilepic':function(){
			return this.request({
				'method': "GET",
				'url': "/profile-image/"
			});
		},
		'getfriendlist':function(){
			return this.request({
				'method': "GET",
				'url': "/friend-list/"
			});
		},
		'getfrienddetails':function(id){
			return this.request({
				'method': "GET",
				'url': "/user-detail/"+id+"/"
			});
		},
		'searchfriend':function(q){
			return this.request({
				'method':"GET",
				'url':"/search-friend/"+q+"/"
			});
		},
		'addfriend':function(id){
			return this.request({
				'method':"POST",
				'url':'/add-friend/',
				'data':{'friend_request':id}
			});
		},
		'acceptfriend':function(id){
			return this.request({
				'method':"POST",
				'url':'/friend-request-accept/',
				'data':{'friend_request':id}
			});
		},
		'unfriend':function(id){
			return this.request({
				'method':"DELETE",
				'url':'/un-friend/'+id+'/'
			});
		},
		'getrequestreceive':function(){
			return this.request({
				'method': "GET",
				'url': "/friend-request-received/"
			});
		},
		'getrequestsend':function(){
			return this.request({
				'method': "GET",
				'url': "/friend-request-sent/"
			});
		},
		'initialize': function(url, sessions, scope, rootScope){
			this.API_URL = url;
			this.use_session = sessions;
			if(scope){
				scope.authenticated = null;
				if(this.authenticated == null){
					if(ipCookie('token')){
						djangoAuth.authenticated = true;
						scope.authenticated = true;
						rootScope.token = ipCookie('token');
					}
					else{
						djangoAuth.authenticated = false;
						scope.authenticated = false;
					}
				}else{
					scope.authenticated = this.authenticated;
				}
				scope.setAuth = function(auth){
					scope.authenticated = auth;
				}
			}
		}
	};
	return service;
});
