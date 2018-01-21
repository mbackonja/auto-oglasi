var app = angular.module('clientApp', ['ngRoute'], function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');     
});

app.config(function($routeProvider) {
  $routeProvider
  .when('/', {
      templateUrl : "static/partials/client/main.html"
  })
  .when('/test', {
    templateUrl : "static/partials/client/test.html"
  });
});