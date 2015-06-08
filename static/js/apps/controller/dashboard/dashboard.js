'use strict';
pfadmin.controller('dashboardCtrl', function DashboardCtrl($scope, $rootScope, $state, $stateParams, djangoAuth) {
	if ($rootScope.token){
		$scope.loggedIn = true;
		$scope.loading = false;

		var name = $state.current.name.split('.')[1];
		if(name=="profile"){
			$scope.profile = true;
			$scope.friendList = false;
		} else if(name=="friendList"){
			$scope.profile = false;
			$scope.friendList = true;
		}else{
			$state.go('dashboard.profile')
		}

		// Search Friend
		$scope.search = {q:''};
		$scope.getFriend = function(val) {
			return djangoAuth.searchfriend(val)
			.then(function(data){
					console.log(data);
				return data;
			});
		};
		$scope.onSelectFriend = function(a, b) {
			//console.log(a,b);
			$scope.friendPub = a;
			$stateParams.name = b.trim();
			$state.go('dashboard.showFriendPub',$stateParams)
		}

	} else {
		$state.go('login');
	}
});

pfadmin.controller('friendListCtrl', function friendListCtrl($scope, $state, djangoAuth){
	//Get Friend list
	djangoAuth.getfriendlist()
		.then(function(data) {
			$scope.lists = data;
			if($scope.lists == ''){
				$scope.nofriend = true;
			}
			else{
				$scope.nofriend = false;
			}
		}, function(data) {
			$state.go('logout');
		});

	// Get Friend details
	$scope.friendDetail = function(id){
		djangoAuth.getfrienddetails(id)
			.then(function(data){
				$scope.details = data;
			});
	};
	// UnFriend Request
	$scope.unFriend = function(id){
		djangoAuth.unfriend(id)
			.then(function(data){
				$state.go("dashboard.profile");
				//console.log(data);
			},function(data){
				$state.go("dashboard.profile");
				//console.log(data);
			});
	};
});

pfadmin.controller('showfriendpubCtrl', function showfriendpubCtrl($scope, $state, $stateParams, djangoAuth, toastr){
	// Get Friend Details
	if($scope.friendPub !== undefined) {
		djangoAuth.getfrienddetails($scope.friendPub.id)
			.then(function (data) {
				$scope.pubFriendProfile = data;
				if($scope.pubFriendProfile.is_owner){
					$state.go('dashboard.profile');
				}
			}, function (data) {
				$state.go('dashboard.profile');
			});
	}
	// Send Friend Request
	$scope.addFriend = function(id){
		djangoAuth.addfriend(id)
			.then(function(data){
				//console.log(data);
				toastr.success('Wait for acceptance', 'Friend Request Send');
				$state.go("dashboard.friendRequestSend");
			},function(data){
				//console.log(data);
				$state.go('dashboard.profile');
			});
	};
	// Accept Friend Request
	$scope.acceptFriend = function(id){
		djangoAuth.acceptfriend(id)
			.then(function(data){
				//console.log(data);
				$state.go('dashboard.friendList');
				toastr.success('Thanks you!', 'Friend Request Accepted');
			},function(data){
				//console.log(data);
				$state.go('dashboard.profile');
			});
	};
	// UnFriend Request
	$scope.unFriend = function(id){
		djangoAuth.unfriend(id)
			.then(function(data){
				//console.log(data);
				$state.go('dashboard.profile');
				toastr.warning('You have unfriend you buddy!', 'Unfriend');
			},function(data){
				//console.log(data);
				$state.go('dashboard.profile');
			});
	};
});

pfadmin.controller('requestReceivedCtrl', function requestReceivedCtrl($scope, $state, djangoAuth){
	//Get Friend Request received
	djangoAuth.getrequestreceive()
		.then(function(data){
			$scope.lists = data;
			if($scope.lists == ''){
				$scope.norequest = true;
			}
			else{
				$scope.norequest = false;
			}
		});

	// Get Friend details
	$scope.friendDetail = function(id){
		djangoAuth.getfrienddetails(id)
			.then(function(data){
				//console.log(data);
				$scope.details = data;
			});
	};
	// Accept Friend Request
	$scope.acceptFriend = function(id){
		djangoAuth.acceptfriend(id)
			.then(function(data){
				$state.go('dashboard.friendList');
				//console.log(data);
			},function(data){
				//console.log(data);
				$state.go('dashboard.profile');
			});
	};
});

pfadmin.controller('requestSendCtrl', function requestSendCtrl($scope, $state, djangoAuth){
	//Get Friend Request received
	djangoAuth.getrequestsend()
		.then(function(data){
			$scope.lists = data;
			if($scope.lists == ''){
				$scope.norequest = true;
			}
			else{
				$scope.norequest = false;
			}
		});

	// Get Friend details
	$scope.friendDetail = function(id){
		djangoAuth.getfrienddetails(id)
			.then(function(data){
				//console.log(data);
				$scope.details = data;
			});
	};
	// Accept Friend Request
	$scope.acceptFriend = function(id){
		djangoAuth.acceptfriend(id)
			.then(function(data){
				$state.go('dashboard.friendList');
				//console.log(data);
			},function(data){
				//console.log(data);
				$state.go('dashboard.profile');
			});
	};
});