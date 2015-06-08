'use strict';
var pfadmin = angular.module('fbProto', ['ipCookie', 'ngResource', 'ngSanitize', 'ngAnimate', 'ui.router', 'ui.bootstrap','ngImgCrop','toastr']);
pfadmin.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{$');
	$interpolateProvider.endSymbol('$}');
});
pfadmin.config(function($stateProvider, $urlRouterProvider, $locationProvider) {
	$locationProvider.hashPrefix('!');
	$urlRouterProvider.otherwise('/');
	$stateProvider
		.state('login', {
			url: '/login',
			templateUrl: 'static/partials/login.html'
		})
		.state('logout', {
			url: '/logout',
			templateUrl: 'static/partials/logout.html'
		})
		.state('register', {
			url: '/register',
			templateUrl: 'static/partials/register.html'
		})

		//Dashboard
		.state('dashboard', {
			abstract: true,
			url: '/dashboard',
			templateUrl: 'static/partials/dashboard/dashboard.html',
			controller: 'dashboardCtrl'
   	})
		
		// Profile
		.state('dashboard.profile', {
			url: '/profile',
			templateUrl: 'static/partials/dashboard/profile.html',
			controller:'profileCtrl'
		})
		.state('dashboard.friendList', {
			url: '/friendlist',
			templateUrl: 'static/partials/dashboard/friendlist.html',
			controller:'friendListCtrl'
		})
		.state('dashboard.showFriendPub', {
			url: '/search/{name}',
			templateUrl: 'static/partials/dashboard/showfriendpub.html',
			controller:'showfriendpubCtrl'
		})
		.state('dashboard.requestReceived', {
			url: '/requestreceived',
			templateUrl: 'static/partials/dashboard/requestreceived.html',
			controller:'requestReceivedCtrl'
		})
		.state('dashboard.friendRequestSend', {
			url: '/requestsend',
			templateUrl: 'static/partials/dashboard/requestsend.html',
			controller:'requestSendCtrl'
		})
		;
});