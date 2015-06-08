'use strict';

pfadmin.controller('RegisterCtrl', function ($scope, $state, $stateParams, djangoAuth, $rootScope, ipCookie) {
	if($rootScope.token){
		console.log("logged in")
		$state.go('dashboard.profile');
	}

	$scope.model = {'first_name':'','last_name':'','email':'','password':''};
	$scope.complete = false;
	
	// Registration
	$scope.register = function(formData){
		$scope.errors = [];
		if(formData.$valid){
			djangoAuth.register($scope.model, $rootScope)
			.then(function(data){
				$scope.setAuth(true);
				$state.go('dashboard.profile');

				// profile
				djangoAuth.profile()
				.then(function(data){
					$rootScope.loggeddata = data;
				},function(data){
					$state.go('logout');
				});
				
			},function(data){
				// error case
				//$scope.errors = [];
				//for(var key in data){
				//	if(key != "status"){
				//		console.log(data[key][0]);
				//		$scope.errors.push(data[key][0]);
				//	}
				//}
				$scope.errors = data.user.email;
				//console.log($scope.errors);
			});
		}
	}

});