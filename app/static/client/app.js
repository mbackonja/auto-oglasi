var app = angular.module("app", [], function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');     
});

app.controller("HelloController", function($scope) {
  $scope.message = "Hello, AngularJS";	
});