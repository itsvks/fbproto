'use strict';

pfadmin.controller('LogoutCtrl', function ($scope, $rootScope, djangoAuth) {
  djangoAuth.logout($rootScope);
  $scope.setAuth(false);
});
