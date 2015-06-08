'use strict';
pfadmin.controller('LoginCtrl', function ($scope, $rootScope, $state , djangoAuth) {
	if($rootScope.token){
		$state.go('dashboard.profile');
	}
	else {
		$scope.model = {'email': '', 'password': '', 'staySign': false};
		$scope.complete = false;
		$scope.login = function (formData) {
			$scope.submitted = true;
			if (formData.password.$error.minlength) {
				$scope.minlength = true;
				$scope.model.password = "";
			}
			if (formData.email.$error.pattern) {
				$scope.pattern = true;
			}
			if (formData.$valid) {
				djangoAuth.login($scope.model, $rootScope)
					.then(function (data) {
						// success case
						$scope.complete = true;
						$scope.setAuth(true);
						$state.go('dashboard.profile');
					}, function (data) {
						// error case
						$scope.error = data.error;
					});
			}
		}
	}
});